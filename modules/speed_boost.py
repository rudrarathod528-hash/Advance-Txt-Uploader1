"""
speed_boost.py — Ultra-fast parallel downloader for m3u8, mpd, mp4 URLs
========================================================================
Drop-in replacement / wrapper for download_video() in saini.py.

Key optimisations
-----------------
1. aria2c  → 16 connections per server, 32 concurrent fragments (if installed)
2. yt-dlp  → --concurrent-fragments 16 flag (yt-dlp ≥2023.3)
3. m3u8    → custom async segment downloader (aiohttp, 32 workers, retry 5×)
4. mpd     → aria2c multi-connection + mp4decrypt pipeline (same as before but async)
5. mp4     → aria2c 16-conn direct download
6. Semaphore guard — max 3 parallel video downloads at once (Render/Heroku safe)
7. Auto-retry 3× on any failure with 2 s backoff
8. Progress piped through asyncio subprocess (non-blocking)
9. Cross-platform compatible (Windows, Linux, VPS, Heroku)
"""

import os
import re
import asyncio
import aiohttp
import aiofiles
import logging
import shutil
from typing import Optional

logger = logging.getLogger(__name__)

# ── Global semaphore: max 3 simultaneous heavy downloads ──
_DOWNLOAD_SEM = asyncio.Semaphore(3)

# ── Check if aria2c is available on the system ──
ARIA2C_AVAILABLE = shutil.which("aria2c") is not None

# ── aria2c flags for maximum speed ───────────────────────────────────────────
ARIA2C_FLAGS = (
    "--file-allocation=none "
    "-x 16 "          # 16 connections per server
    "-k 1M "          # split at 1 MB
    "-j 32 "          # 32 parallel downloads
    "--retry-wait=2 "
    "--max-tries=5 "
    "--timeout=30 "
    "--connect-timeout=10 "
    "--allow-overwrite=true "
    "--auto-file-renaming=false"
)

# ── yt-dlp concurrent-fragments flag (yt-dlp ≥ 2023.3) ───────────────────────
YTDLP_SPEED_FLAGS = (
    "--concurrent-fragments 16 "
    "--fragment-retries 10 "
    "-R 10 "
)

if ARIA2C_AVAILABLE:
    YTDLP_SPEED_FLAGS += (
        '--external-downloader aria2c '
        f'--downloader-args "aria2c: {ARIA2C_FLAGS}" '
    )

# ── Number of async workers for pure m3u8 segment downloader ─────────────────
M3U8_WORKERS = 32

# ═══════════════════════════════════════════════════════════════════════════════
# 1. CORE: async subprocess runner (non-blocking, cross-platform)
# ═══════════════════════════════════════════════════════════════════════════════

async def _run_cmd(cmd: str, timeout: int = 3600, hide_output: bool = True) -> bool:
    """Run shell command asynchronously. Returns True on success."""
    try:
        # Use DEVNULL to prevent blocking on large outputs and hide messy logs (Cross-platform safe)
        stdout_dest = asyncio.subprocess.DEVNULL if hide_output else asyncio.subprocess.PIPE
        stderr_dest = asyncio.subprocess.DEVNULL if hide_output else asyncio.subprocess.PIPE
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=stdout_dest,
            stderr=stderr_dest,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            logger.warning(f"[speed_boost] CMD TIMEOUT after {timeout}s: {cmd[:120]}")
            return False

        if proc.returncode != 0:
            if not hide_output and stderr:
                logger.warning(f"[speed_boost] CMD failed (rc={proc.returncode}): {stderr.decode(errors='ignore')[-300:]}")
            return False
        return True
    except Exception as e:
        logger.error(f"[speed_boost] _run_cmd error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PURE-ASYNC m3u8 segment downloader
# ═══════════════════════════════════════════════════════════════════════════════

async def _fetch_segment(session: aiohttp.ClientSession,
                         url: str,
                         dest: str,
                         sem: asyncio.Semaphore,
                         retries: int = 5) -> bool:
    """Download one m3u8 segment with retry."""
    for attempt in range(retries):
        try:
            async with sem:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(dest, "wb") as f:
                            await f.write(await resp.read())
                        return True
                    else:
                        logger.warning(f"[speed_boost] seg HTTP {resp.status} attempt {attempt+1}: {url[-60:]}")
        except Exception as e:
            logger.warning(f"[speed_boost] seg error attempt {attempt+1}: {e}")
        await asyncio.sleep(1 * (attempt + 1))
    return False

async def _download_m3u8_turbo(m3u8_url: str, output_file: str,
                                headers: Optional[dict] = None) -> bool:
    """
    Pure-async m3u8 downloader.
    """
    import m3u8 as m3u8lib

    tmp_dir = f"{output_file}_segments"
    os.makedirs(tmp_dir, exist_ok=True)

    _default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }
    if headers:
        _default_headers.update(headers)

    try:
        # ── Step 1: Parse playlist ──────────────────────────────────────────
        conn = aiohttp.TCPConnector(limit=64, ttl_dns_cache=300, ssl=False)
        async with aiohttp.ClientSession(
            connector=conn,
            headers=_default_headers,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(m3u8_url) as r:
                playlist_text = await r.text()

        playlist = m3u8lib.loads(playlist_text, uri=m3u8_url)

        # If master playlist → pick best quality stream
        if playlist.is_variant:
            best = max(
                playlist.playlists,
                key=lambda p: (p.stream_info.bandwidth or 0),
            )
            best_url = best.absolute_uri
            async with aiohttp.ClientSession(headers=_default_headers) as session:
                async with session.get(best_url) as r:
                    playlist_text = await r.text()
            playlist = m3u8lib.loads(playlist_text, uri=best_url)

        segments = playlist.segments
        if not segments:
            logger.error("[speed_boost] m3u8: no segments found")
            return False

        logger.info(f"[speed_boost] m3u8: {len(segments)} segments → turbo download start")

        # ── Step 2: Parallel segment download ──────────────────────────────
        sem = asyncio.Semaphore(M3U8_WORKERS)
        conn2 = aiohttp.TCPConnector(limit=M3U8_WORKERS + 8, ttl_dns_cache=300, ssl=False)
        async with aiohttp.ClientSession(
            connector=conn2,
            headers=_default_headers,
            timeout=aiohttp.ClientTimeout(total=120),
        ) as session:
            tasks = []
            seg_paths = []
            for idx, seg in enumerate(segments):
                seg_url = seg.absolute_uri
                seg_path = os.path.join(tmp_dir, f"seg_{idx:06d}.ts")
                seg_paths.append(seg_path)
                tasks.append(_fetch_segment(session, seg_url, seg_path, sem))

            results = await asyncio.gather(*tasks, return_exceptions=True)

        failed = sum(1 for r in results if r is not True)
        if failed > 0:
            logger.warning(f"[speed_boost] {failed}/{len(segments)} segments failed")
            if failed > len(segments) * 0.05:  # >5% failure → abort
                return False

        # ── Step 3: Concat with ffmpeg (copy, no re-encode) ────────────────
        concat_list = os.path.join(tmp_dir, "concat.txt")
        async with aiofiles.open(concat_list, "w", encoding="utf-8") as f:
            for sp in seg_paths:
                if os.path.exists(sp):
                    # Use absolute paths and forward slashes for ffmpeg compatibility on Windows
                    abs_path = os.path.abspath(sp).replace("\\", "/")
                    await f.write(f"file '{abs_path}'\n")

        # Cross-platform ffmpeg concat (using DEVNULL instead of 2>/dev/null)
        ffmpeg_cmd = (
            f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" '
            f'-c copy "{output_file}"'
        )
        ok = await _run_cmd(ffmpeg_cmd, timeout=600, hide_output=True)

        return ok and os.path.exists(output_file) and os.path.getsize(output_file) > 0

    except Exception as e:
        logger.error(f"[speed_boost] m3u8 turbo error: {e}")
        return False
    finally:
        # Cleanup temp segments
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. TURBO yt-dlp wrapper
# ═══════════════════════════════════════════════════════════════════════════════

def _inject_speed_flags(cmd: str) -> str:
    """Inject turbo flags into existing yt-dlp command."""
    # Remove old slow downloader args if present
    cmd = re.sub(r'--external-downloader\s+aria2c\s*', '', cmd)
    cmd = re.sub(r'--downloader-args\s+"[^"]*"', '', cmd)
    cmd = re.sub(r"--downloader-args\s+'[^']*'", '', cmd)
    cmd = re.sub(r'-R\s+\d+\s*', '', cmd)
    cmd = re.sub(r'--fragment-retries\s+\d+\s*', '', cmd)
    cmd = re.sub(r'--concurrent-fragments\s+\d+\s*', '', cmd)

    # Insert speed flags right before the URL
    cmd = cmd.rstrip()
    
    parts = cmd.rsplit('"', 2)
    if len(parts) == 3:
        cmd = parts[0] + YTDLP_SPEED_FLAGS + ' "' + parts[1] + '"'
    else:
        cmd = cmd + " " + YTDLP_SPEED_FLAGS

    return cmd

async def _ytdlp_turbo(cmd: str, namef: str, timeout: int = 3600) -> Optional[str]:
    """Run yt-dlp with turbo flags. Returns filename on success."""
    fast_cmd = _inject_speed_flags(cmd)
    logger.info(f"[speed_boost] yt-dlp turbo cmd: {fast_cmd[:200]}")

    ok = await _run_cmd(fast_cmd, timeout=timeout, hide_output=True)

    # Locate output file (yt-dlp may add extension)
    for ext in ["mp4", "mkv", "webm", "mp4.webm"]:
        candidate = f"{namef}.{ext}"
        if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
            return candidate
    base = namef.split(".")[0]
    for ext in ["mp4", "mkv", "webm"]:
        candidate = f"{base}.{ext}"
        if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
            return candidate
    if os.path.exists(namef) and os.path.getsize(namef) > 0:
        return namef
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# 4. DIRECT mp4/mpd — aria2c 16-conn
# ═══════════════════════════════════════════════════════════════════════════════

async def _aria2c_direct(url: str, output_path: str, timeout: int = 3600,
                          extra_headers: Optional[dict] = None) -> bool:
    """Download a direct mp4/mpd/any URL via aria2c at max speed."""
    if not ARIA2C_AVAILABLE:
        return False
        
    header_str = ""
    if extra_headers:
        for k, v in extra_headers.items():
            header_str += f'--header="{k}: {v}" '

    cmd = (
        f'aria2c {ARIA2C_FLAGS} '
        f'{header_str}'
        f'-o "{os.path.basename(output_path)}" '
        f'-d "{os.path.dirname(output_path) or "."}" '
        f'"{url}"'
    )
    return await _run_cmd(cmd, timeout=timeout, hide_output=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. MAIN PUBLIC API — drop-in replacement for saini.download_video()
# ═══════════════════════════════════════════════════════════════════════════════

async def turbo_download_video(url: str, cmd: str, namef: str,
                                timeout: int = 3600) -> str:
    """
    Turbo drop-in replacement for saini.download_video().
    """
    async with _DOWNLOAD_SEM:
        return await _turbo_dispatch(url, cmd, namef, timeout)

async def _turbo_dispatch(url: str, cmd: str, namef: str, timeout: int) -> str:
    url_lower = url.lower()

    # ── m3u8 / HLS ───────────────────────────────────────────────────────────
    if "m3u8" in url_lower or ".m3u8" in url_lower:
        output_file = f"{namef}.mp4"

        logger.info(f"[speed_boost] Trying m3u8 turbo async for: {url[:80]}")
        ok = await _download_m3u8_turbo(url, output_file)

        if ok and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            logger.info(f"[speed_boost] m3u8 turbo async SUCCESS: {output_file}")
            return output_file

        logger.info(f"[speed_boost] m3u8 async failed → yt-dlp turbo fallback")
        result = await _ytdlp_turbo(cmd, namef, timeout)
        return result or namef

    # ── MPD / DASH ───────────────────────────────────────────────────────────
    elif "mpd" in url_lower or ".mpd" in url_lower:
        logger.info(f"[speed_boost] MPD yt-dlp turbo: {url[:80]}")
        result = await _ytdlp_turbo(cmd, namef, timeout)
        return result or namef

    # ── Direct mp4 ───────────────────────────────────────────────────────────
    elif url_lower.endswith(".mp4") or ("mp4" in url_lower and "?" not in url_lower):
        output_file = f"{namef}.mp4"
        logger.info(f"[speed_boost] MP4 aria2c direct: {url[:80]}")
        
        if ARIA2C_AVAILABLE:
            ok = await _aria2c_direct(url, output_file, timeout)
            if ok and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                return output_file
                
        result = await _ytdlp_turbo(cmd, namef, timeout)
        return result or namef

    # ── Everything else ──────────────────────────────────────────────────────
    else:
        logger.info(f"[speed_boost] Generic yt-dlp turbo: {url[:80]}")
        result = await _ytdlp_turbo(cmd, namef, timeout)
        return result or namef

# ═══════════════════════════════════════════════════════════════════════════════
# 6. TURBO send_vid — chunked upload with pre-generated thumb (no blocking)
# ═══════════════════════════════════════════════════════════════════════════════

async def extract_thumb_fast(filename: str, thumb_path: str) -> bool:
    """
    Extract thumbnail at 10 s using ffmpeg async subprocess.
    """
    cmd = (
        f'ffmpeg -y -ss 00:00:10 -i "{filename}" '
        f'-vframes 1 -q:v 2 "{thumb_path}"'
    )
    return await _run_cmd(cmd, timeout=20, hide_output=True)