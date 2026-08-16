import os
import requests
import subprocess
from vars import CREDIT
from pyrogram import Client, filters
from pyrogram.types import Message

#==================================================================================================================================

# Function to extract names and URLs from the text file
def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            name, url = line.split(":", 1)
            data.append((name.strip(), url.strip()))
    return data

#==================================================================================================================================

# Function to categorize URLs
def categorize_urls(urls):
    videos = []
    pdfs = []
    others = []

    for name, url in urls:
        new_url = url
        if ("akamaized.net/" in url or "1942403233.rsc.cdn77.org/" in url) and ".pdf" not in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://www.khanglobalstudies.com/player?src={url}"
            videos.append((name, new_url))

        elif "youtu" in url:
            if "youtube.com/embed" in url:
                yt_id = url.split("/")[-1]
                new_url = f"https://www.youtube.com/watch?v={yt_id}"
            videos.append((name, url))
            
        elif ".m3u8" in url:
            videos.append((name, url))
        elif ".mp4" in url:
            videos.append((name, url))
        elif "pdf" in url:
            pdfs.append((name, url))
        else:
            others.append((name, url))

    return videos, pdfs, others

#=================================================================================================================================

# Function to generate HTML file with Video.js player
def generate_html(file_name, videos, pdfs, others):
    file_name_without_extension = os.path.splitext(file_name)[0]

    # Build video items with serial numbers
    video_items_html = ""
    for i, (name, url) in enumerate(videos, 1):
        if "youtu" in url:
            icon = "fab fa-youtube"
            icon_color = "#ff0000"
            badge = "YouTube"
            badge_class = "badge-yt"
        elif ".m3u8" in url:
            icon = "fas fa-film"
            icon_color = "#00b4d8"
            badge = "HLS"
            badge_class = "badge-hls"
        elif "khanglobal" in url or "player?src" in url:
            icon = "fas fa-play-circle"
            icon_color = "#7b2ff7"
            badge = "KGS"
            badge_class = "badge-kgs"
        else:
            icon = "fas fa-video"
            icon_color = "#007bff"
            badge = "MP4"
            badge_class = "badge-mp4"

        escaped_url = url.replace("'", "\\'").replace("\\", "\\\\")
        video_items_html += f"""
        <div class="media-item" data-search="{name.lower()}">
            <div class="item-number">{i:02d}</div>
            <div class="item-icon" style="color:{icon_color}"><i class="{icon}"></i></div>
            <div class="item-info">
                <div class="item-title">{name}</div>
                <span class="item-badge {badge_class}">{badge}</span>
            </div>
            <div class="item-actions">
                <button class="btn-play" onclick="playVideo('{escaped_url}', this)" title="Play in Player">
                    <i class="fas fa-play"></i> Play
                </button>
                <button class="btn-open" onclick="window.open('{escaped_url}','_blank')" title="Open in Chrome">
                    <i class="fas fa-external-link-alt"></i> Open
                </button>
            </div>
        </div>"""

    # Build PDF items
    pdf_items_html = ""
    for i, (name, url) in enumerate(pdfs, 1):
        escaped_url = url.replace("'", "\\'")
        pdf_items_html += f"""
        <div class="media-item" data-search="{name.lower()}">
            <div class="item-number">{i:02d}</div>
            <div class="item-icon" style="color:#e63946"><i class="fas fa-file-pdf"></i></div>
            <div class="item-info">
                <div class="item-title">{name}</div>
                <span class="item-badge badge-pdf">PDF</span>
            </div>
            <div class="item-actions">
                <button class="btn-pdf-view" onclick="openPdf('{escaped_url}')" title="View PDF in Chrome">
                    <i class="fas fa-eye"></i> View
                </button>
                <button class="btn-open" onclick="window.open('{escaped_url}','_blank')" title="Open PDF">
                    <i class="fas fa-external-link-alt"></i> Open
                </button>
            </div>
        </div>"""

    # Build others items
    other_items_html = ""
    for i, (name, url) in enumerate(others, 1):
        escaped_url = url.replace("'", "\\'")
        other_items_html += f"""
        <div class="media-item" data-search="{name.lower()}">
            <div class="item-number">{i:02d}</div>
            <div class="item-icon" style="color:#6c757d"><i class="fas fa-link"></i></div>
            <div class="item-info">
                <div class="item-title">{name}</div>
                <span class="item-badge badge-other">Link</span>
            </div>
            <div class="item-actions">
                <button class="btn-open" onclick="window.open('{escaped_url}','_blank')" title="Open Link">
                    <i class="fas fa-external-link-alt"></i> Open
                </button>
            </div>
        </div>"""

    total_videos = len(videos)
    total_pdfs = len(pdfs)
    total_others = len(others)
    total_all = total_videos + total_pdfs + total_others

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_name_without_extension}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        :root {{
            --primary: #6c63ff;
            --primary-dark: #4a42d6;
            --accent: #ff6584;
            --success: #43d9ad;
            --warning: #ffd166;
            --danger: #e63946;
            --dark: #0f0f1a;
            --dark2: #1a1a2e;
            --dark3: #16213e;
            --card-bg: #1e1e30;
            --card-border: #2d2d4a;
            --text: #e0e0f0;
            --text-muted: #8888aa;
            --glass: rgba(255,255,255,0.05);
            --glass-border: rgba(255,255,255,0.1);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: var(--dark);
            color: var(--text);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            min-height: 100vh;
            background-image:
                radial-gradient(ellipse at 20% 50%, rgba(108,99,255,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(255,101,132,0.06) 0%, transparent 40%);
        }}

        /* HEADER */
        .header {{
            background: linear-gradient(135deg, var(--dark2) 0%, var(--dark3) 100%);
            border-bottom: 1px solid var(--glass-border);
            padding: 24px 20px 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}
        .header-title {{
            font-size: clamp(18px, 4vw, 28px);
            font-weight: 800;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header-sub {{ font-size: 13px; color: var(--text-muted); margin-top: 6px; }}
        .header-sub b {{ color: var(--warning); }}
        .stats-row {{ display: flex; justify-content: center; gap: 16px; margin-top: 14px; flex-wrap: wrap; }}
        .stat-chip {{
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 12px;
            color: var(--text-muted);
        }}
        .stat-chip span {{ font-weight: 700; color: var(--primary); }}

        /* PLAYER */
        .player-wrapper {{
            margin: 24px auto;
            width: 92%;
            max-width: 860px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            display: none;
        }}
        .player-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: var(--dark2);
            border-bottom: 1px solid var(--card-border);
        }}
        .player-title-now {{ font-size: 13px; color: var(--text-muted); max-width: 70%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .player-title-now b {{ color: var(--text); }}
        .btn-close-player {{
            background: rgba(255,101,132,0.15);
            color: var(--accent);
            border: 1px solid rgba(255,101,132,0.3);
            border-radius: 6px;
            padding: 5px 12px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-close-player:hover {{ background: var(--accent); color: white; }}
        #engineer-babu-player {{ width: 100%; }}

        /* PDF VIEWER */
        .pdf-wrapper {{
            margin: 0 auto 20px;
            width: 92%;
            max-width: 860px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            display: none;
        }}
        .pdf-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: var(--dark2);
            border-bottom: 1px solid var(--card-border);
        }}
        .pdf-header-title {{ font-size: 13px; color: var(--text-muted); max-width: 70%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .btn-close-pdf {{
            background: rgba(230,57,70,0.15);
            color: var(--danger);
            border: 1px solid rgba(230,57,70,0.3);
            border-radius: 6px;
            padding: 5px 12px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-close-pdf:hover {{ background: var(--danger); color: white; }}
        #pdf-frame {{ width: 100%; height: 540px; border: none; background: #fff; }}

        /* CUSTOM URL */
        .custom-url-bar {{
            margin: 0 auto 20px;
            width: 92%;
            max-width: 860px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 16px;
            display: none;
        }}
        .custom-url-bar .input-row {{ display: flex; gap: 10px; }}
        .custom-url-bar input {{
            flex: 1;
            padding: 10px 14px;
            background: var(--dark2);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            color: var(--text);
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .custom-url-bar input:focus {{ border-color: var(--primary); }}
        .custom-url-bar button {{
            padding: 10px 20px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            white-space: nowrap;
        }}
        .custom-url-bar button:hover {{ background: var(--primary-dark); }}

        /* SEARCH */
        .search-wrap {{ margin: 0 auto 20px; width: 92%; max-width: 860px; }}
        .search-input-wrap {{ position: relative; }}
        .search-input-wrap i {{ position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 15px; }}
        .search-wrap input {{
            width: 100%;
            padding: 12px 14px 12px 42px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            color: var(--text);
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .search-wrap input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(108,99,255,0.15); }}
        .search-wrap input::placeholder {{ color: var(--text-muted); }}

        /* TOOLBAR */
        .toolbar {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 0 auto 20px; width: 92%; max-width: 860px; }}
        .tab-btn {{
            flex: 1;
            min-width: 100px;
            padding: 12px 10px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s;
            text-align: center;
        }}
        .tab-btn .tab-count {{
            display: inline-block;
            background: var(--dark2);
            border-radius: 10px;
            padding: 1px 8px;
            font-size: 11px;
            margin-left: 6px;
            transition: all 0.25s;
        }}
        .tab-btn:hover, .tab-btn.active {{
            border-color: var(--primary);
            color: white;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            box-shadow: 0 4px 15px rgba(108,99,255,0.3);
            transform: translateY(-2px);
        }}
        .tab-btn:hover .tab-count, .tab-btn.active .tab-count {{ background: rgba(255,255,255,0.2); }}
        .btn-custom-url {{
            padding: 12px 18px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s;
            white-space: nowrap;
        }}
        .btn-custom-url:hover {{ border-color: var(--success); color: var(--success); }}

        /* CONTENT PANEL */
        .content-panel {{ display: none; margin: 0 auto 30px; width: 92%; max-width: 860px; }}
        .content-panel.active {{ display: block; }}
        .panel-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding: 0 4px; }}
        .panel-heading {{ font-size: 16px; font-weight: 700; color: var(--text); display: flex; align-items: center; gap: 8px; }}
        .panel-heading i {{ color: var(--primary); }}
        .panel-count {{
            font-size: 12px;
            color: var(--text-muted);
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 3px 12px;
        }}

        /* MEDIA ITEM */
        .media-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 8px;
            transition: all 0.2s;
        }}
        .media-item:hover {{
            border-color: var(--primary);
            background: rgba(108,99,255,0.05);
            transform: translateX(4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        }}
        .item-number {{ font-size: 11px; color: var(--text-muted); min-width: 26px; font-weight: 700; font-variant-numeric: tabular-nums; }}
        .item-icon {{ font-size: 20px; min-width: 28px; text-align: center; }}
        .item-info {{ flex: 1; min-width: 0; }}
        .item-title {{ font-size: 13.5px; font-weight: 600; color: var(--text); line-height: 1.4; word-break: break-word; }}
        .item-badge {{
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            border-radius: 4px;
            padding: 1px 7px;
            margin-top: 4px;
            letter-spacing: 0.5px;
        }}
        .badge-yt    {{ background: rgba(255,0,0,0.15);     color: #ff4444; }}
        .badge-hls   {{ background: rgba(0,180,216,0.15);   color: #00b4d8; }}
        .badge-kgs   {{ background: rgba(123,47,247,0.15);  color: #9b72ff; }}
        .badge-mp4   {{ background: rgba(0,123,255,0.15);   color: #4da3ff; }}
        .badge-pdf   {{ background: rgba(230,57,70,0.15);   color: #ff6b6b; }}
        .badge-other {{ background: rgba(108,117,125,0.15); color: #8888aa; }}

        .item-actions {{ display: flex; gap: 6px; flex-shrink: 0; }}
        .btn-play {{
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            border: none;
            border-radius: 8px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .btn-play:hover {{ transform: scale(1.05); box-shadow: 0 4px 12px rgba(108,99,255,0.4); }}
        .btn-play.active-playing {{
            background: linear-gradient(135deg, var(--success), #2dc89a);
            animation: pulse-glow 1.5s infinite;
        }}
        @keyframes pulse-glow {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(67,217,173,0.4); }}
            50% {{ box-shadow: 0 0 0 6px rgba(67,217,173,0); }}
        }}
        .btn-open {{
            background: var(--glass);
            color: var(--text-muted);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
            padding: 7px 12px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .btn-open:hover {{ background: rgba(255,255,255,0.1); color: var(--text); }}
        .btn-pdf-view {{
            background: linear-gradient(135deg, var(--danger), #c1121f);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .btn-pdf-view:hover {{ transform: scale(1.05); box-shadow: 0 4px 12px rgba(230,57,70,0.4); }}

        /* NO RESULTS / EMPTY */
        .no-results {{ text-align: center; padding: 40px 20px; color: var(--text-muted); display: none; }}
        .no-results i {{ font-size: 36px; margin-bottom: 12px; opacity: 0.4; }}
        .empty-state {{ text-align: center; padding: 40px 20px; color: var(--text-muted); }}
        .empty-state i {{ font-size: 40px; margin-bottom: 12px; opacity: 0.3; }}

        /* FOOTER */
        .footer {{
            text-align: center;
            padding: 24px 20px;
            background: var(--dark2);
            border-top: 1px solid var(--glass-border);
            color: var(--text-muted);
            font-size: 13px;
        }}
        .footer b {{ color: var(--warning); }}

        @media (max-width: 540px) {{
            .item-actions {{ flex-direction: column; gap: 4px; }}
            .btn-play, .btn-open, .btn-pdf-view {{ padding: 6px 10px; font-size: 11px; }}
            .media-item {{ flex-wrap: wrap; }}
        }}
    </style>
</head>
<body>

    <div class="header">
        <div class="header-title">{file_name_without_extension}</div>
        <div class="header-sub">📥 Extracted By : <b>{CREDIT}</b></div>
        <div class="stats-row">
            <div class="stat-chip">Total <span>{total_all}</span></div>
            <div class="stat-chip">🎬 Videos <span>{total_videos}</span></div>
            <div class="stat-chip">📄 PDFs <span>{total_pdfs}</span></div>
            <div class="stat-chip">🔗 Others <span>{total_others}</span></div>
        </div>
    </div>

    <div class="player-wrapper" id="player-wrapper">
        <div class="player-header">
            <div class="player-title-now">▶ Now Playing: <b id="now-playing-title">—</b></div>
            <button class="btn-close-player" onclick="closePlayer()">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
        <video id="engineer-babu-player" class="video-js vjs-default-skin vjs-big-play-centered"
            controls preload="auto" width="100%">
            <p class="vjs-no-js">
                To view this video please enable JavaScript, and consider upgrading to a web browser that
                <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
            </p>
        </video>
    </div>

    <div class="pdf-wrapper" id="pdf-wrapper">
        <div class="pdf-header">
            <div class="pdf-header-title">📄 Viewing: <b id="pdf-title">—</b></div>
            <button class="btn-close-pdf" onclick="closePdfViewer()">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
        <iframe id="pdf-frame" src="" allowfullscreen></iframe>
    </div>

    <div class="custom-url-bar" id="custom-url-bar">
        <div class="input-row">
            <input type="text" id="url-input" placeholder="Paste any video / HLS / mp4 URL here...">
            <button onclick="playCustomUrl()"><i class="fas fa-play"></i> Play</button>
        </div>
    </div>

    <div class="search-wrap">
        <div class="search-input-wrap">
            <i class="fas fa-search"></i>
            <input type="text" id="searchInput"
                placeholder="Search videos, PDFs, lectures..." oninput="filterContent()">
        </div>
    </div>

    <div class="toolbar">
        <button class="tab-btn active" id="tab-videos" onclick="showContent('videos')">
            <i class="fas fa-play-circle"></i> Videos
            <span class="tab-count">{total_videos}</span>
        </button>
        <button class="tab-btn" id="tab-pdfs" onclick="showContent('pdfs')">
            <i class="fas fa-file-pdf"></i> PDFs
            <span class="tab-count">{total_pdfs}</span>
        </button>
        <button class="tab-btn" id="tab-others" onclick="showContent('others')">
            <i class="fas fa-link"></i> Others
            <span class="tab-count">{total_others}</span>
        </button>
        <button class="btn-custom-url" onclick="toggleCustomUrl()" title="Play custom URL">
            <i class="fas fa-terminal"></i> Custom URL
        </button>
    </div>

    <div id="noResults" class="no-results" style="display:none;">
        <i class="fas fa-search"></i>
        <div>No results found.</div>
    </div>

    <div id="videos" class="content-panel active">
        <div class="panel-header">
            <div class="panel-heading"><i class="fas fa-film"></i> Video Lectures</div>
            <div class="panel-count">{total_videos} videos</div>
        </div>
        {"<div class='empty-state'><i class='fas fa-video-slash'></i><div>No videos found</div></div>" if total_videos == 0 else video_items_html}
    </div>

    <div id="pdfs" class="content-panel">
        <div class="panel-header">
            <div class="panel-heading"><i class="fas fa-file-pdf"></i> PDF Documents</div>
            <div class="panel-count">{total_pdfs} files</div>
        </div>
        {"<div class='empty-state'><i class='fas fa-file-times'></i><div>No PDFs found</div></div>" if total_pdfs == 0 else pdf_items_html}
    </div>

    <div id="others" class="content-panel">
        <div class="panel-header">
            <div class="panel-heading"><i class="fas fa-link"></i> Other Resources</div>
            <div class="panel-count">{total_others} links</div>
        </div>
        {"<div class='empty-state'><i class='fas fa-folder-open'></i><div>No other links found</div></div>" if total_others == 0 else other_items_html}
    </div>

    <div class="footer">
        <b>Extracted By : {CREDIT}</b> &nbsp;|&nbsp; Open in Chrome for best experience
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('engineer-babu-player', {{
            controls: true,
            autoplay: true,
            preload: 'auto',
            fluid: true,
            playbackRates: [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
            controlBar: {{
                children: [
                    'playToggle',
                    'volumePanel',
                    'currentTimeDisplay',
                    'timeDivider',
                    'durationDisplay',
                    'progressControl',
                    'liveDisplay',
                    'remainingTimeDisplay',
                    'customControlSpacer',
                    'playbackRateMenuButton',
                    'chaptersButton',
                    'descriptionsButton',
                    'subsCapsButton',
                    'audioTrackButton',
                    'fullscreenToggle'
                ]
            }}
        }});

        let activePlayBtn = null;

        function playVideo(url, btnEl) {{
            if (activePlayBtn && activePlayBtn !== btnEl) {{
                activePlayBtn.classList.remove('active-playing');
                activePlayBtn.innerHTML = '<i class="fas fa-play"></i> Play';
            }}
            const playerWrapper = document.getElementById('player-wrapper');
            const titleEl = document.getElementById('now-playing-title');
            let title = '—';
            if (btnEl) {{
                const item = btnEl.closest('.media-item');
                if (item) title = item.querySelector('.item-title').textContent;
                btnEl.classList.add('active-playing');
                btnEl.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Playing';
                activePlayBtn = btnEl;
            }}
            if (url.includes('.m3u8')) {{
                playerWrapper.style.display = 'block';
                titleEl.textContent = title;
                player.src({{ src: url, type: 'application/x-mpegURL' }});
                player.play().catch(() => window.open(url, '_blank'));
                playerWrapper.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }} else if (url.includes('.mp4')) {{
                playerWrapper.style.display = 'block';
                titleEl.textContent = title;
                player.src({{ src: url, type: 'video/mp4' }});
                player.play().catch(() => window.open(url, '_blank'));
                playerWrapper.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }} else {{
                window.open(url, '_blank');
                if (btnEl) {{
                    btnEl.classList.remove('active-playing');
                    btnEl.innerHTML = '<i class="fas fa-play"></i> Play';
                    activePlayBtn = null;
                }}
            }}
        }}

        function closePlayer() {{
            player.pause();
            document.getElementById('player-wrapper').style.display = 'none';
            if (activePlayBtn) {{
                activePlayBtn.classList.remove('active-playing');
                activePlayBtn.innerHTML = '<i class="fas fa-play"></i> Play';
                activePlayBtn = null;
            }}
        }}

        function openPdf(url) {{
            const pdfWrapper = document.getElementById('pdf-wrapper');
            const frame = document.getElementById('pdf-frame');
            const titleEl = document.getElementById('pdf-title');
            const viewerUrl = 'https://docs.google.com/viewer?url=' + encodeURIComponent(url) + '&embedded=true';
            frame.src = viewerUrl;
            titleEl.textContent = url.split('/').pop().split('?')[0] || 'Document';
            pdfWrapper.style.display = 'block';
            pdfWrapper.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}

        function closePdfViewer() {{
            document.getElementById('pdf-frame').src = '';
            document.getElementById('pdf-wrapper').style.display = 'none';
        }}

        function toggleCustomUrl() {{
            const bar = document.getElementById('custom-url-bar');
            bar.style.display = (bar.style.display === 'none' || bar.style.display === '') ? 'block' : 'none';
            if (bar.style.display === 'block') document.getElementById('url-input').focus();
        }}

        function playCustomUrl() {{
            const url = document.getElementById('url-input').value.trim();
            if (url) playVideo(url, null);
        }}

        function showContent(tabName) {{
            document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            const panel = document.getElementById(tabName);
            if (panel) panel.classList.add('active');
            const tabEl = document.getElementById('tab-' + tabName);
            if (tabEl) tabEl.classList.add('active');
            filterContent();
        }}

        function filterContent() {{
            const term = document.getElementById('searchInput').value.toLowerCase().trim();
            let totalVisible = 0;
            document.querySelectorAll('.content-panel').forEach(panel => {{
                const items = panel.querySelectorAll('.media-item');
                let panelVisible = 0;
                items.forEach(item => {{
                    const text = (item.dataset.search || '') + ' ' + item.querySelector('.item-title').textContent.toLowerCase();
                    const match = !term || text.includes(term);
                    item.style.display = match ? 'flex' : 'none';
                    if (match) {{ panelVisible++; totalVisible++; }}
                }});
                const heading = panel.querySelector('.panel-header');
                if (heading) heading.style.opacity = (panelVisible === 0 && term) ? '0.3' : '1';
            }});
            document.getElementById('noResults').style.display = (term && totalVisible === 0) ? 'block' : 'none';
        }}

        document.addEventListener('DOMContentLoaded', () => {{ showContent('videos'); }});
        document.getElementById('url-input').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter') playCustomUrl();
        }});
    </script>
</body>
</html>
"""
    return html_template

# Function to download video using FFmpeg
def download_video(url, output_path):
    command = f"ffmpeg -i {url} -c copy {output_path}"
    subprocess.run(command, shell=True, check=True)




#======================================================================================================================================================================================

async def html_handler(bot: Client, message: Message):
    editable = await message.reply_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐩𝐥𝐨𝐚𝐝 𝐚 .𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐜𝐨𝐧𝐭𝐚𝐢𝐧𝐢𝐧𝐠 𝐔𝐑𝐋𝐬.✓")
    input: Message = await bot.listen(editable.chat.id)
    if input.document and input.document.file_name.endswith('.txt'):
        file_path = await input.download()
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        b_name = file_name.replace('_', ' ')
    else:
        await message.reply_text("**• Invalid file input.**")
        return
           
    with open(file_path, "r") as f:
        file_content = f.read()

    urls = extract_names_and_urls(file_content)

    videos, pdfs, others = categorize_urls(urls)

    html_content = generate_html(file_name, videos, pdfs, others)
    html_file_path = file_path.replace(".txt", ".html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    await message.reply_document(document=html_file_path, caption=f"✅𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞!\n<blockquote><b>`{b_name}`</b></blockquote>\n❖**Open in Chrome.**\n\n🌟**Extracted By : {CREDIT}**")
    os.remove(file_path)
    os.remove(html_file_path)
    
#============================================================================================================================
def register_html_handlers(bot):
    @bot.on_message(filters.command(["t2h"]))
    async def call_html_handler(bot: Client, message: Message):
        await html_handler(bot, message)
