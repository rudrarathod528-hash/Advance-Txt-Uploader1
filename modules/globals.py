import os
import json
from vars import OWNER, CREDIT

processing_request = False
cancel_requested = False
caption = '/cc1'
endfilename = '/d'
thumb = '/d'
CR = f"{CREDIT}"
cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
cptoken = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYzNjkyNjM0LCJvcmdJZCI6NjA5NzQyLCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTk0MDQ0MDg3NDAiLCJuYW1lIjoiTXlyYSIsImVtYWlsIjoicml5YWhzaHJpdmFzdGF2NCs1MzMyQGdtYWlsLmNvbSIsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjoiRU4iLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpc0RpeSI6dHJ1ZSwibG9naW5WaWEiOiJPdHAiLCJmaW5nZXJwcmludElkIjoiODZmN2RhMjMyMzgxNDk2YTliMjY4YzhkMTAxOGNkMGEiLCJpYXQiOjE3NTkyMTA3ODksImV4cCI6MTc1OTgxNTU4OX0.O3DG_gMpOUet2HKSmH1jK9EEWmjREEMh4cX7DW4yqqkCTzcV5C6-lr6zaY1ihhR4"
pwtoken = "pwtoken"
vidwatermark = '/d'
pdfwatermark = '/d'
videocover = '/d'
raw_text2 = '480'
quality = '480p'
res = '854x480'
topic = '/d'

# ── Multi-location PDF watermark settings ────────────────────────────────────
# Each location stores {"title": str|"/d", "url": str|"/d"}
# Default: all disabled (/d)
pdf_wm_upper_right = {"title": "/d", "url": "/d"}   # 25% opacity, 45° rotation (original)
pdf_wm_upper_left  = {"title": "/d", "url": "/d"}   # 25% opacity, 45° rotation
pdf_wm_down_right  = {"title": "JOIN NOW", "url": "https://t.me/Toxic_Official_1"}   # 90% opacity, 0° rotation
pdf_wm_down_left   = {"title": "/d", "url": "/d"}   # 90% opacity, 0° rotation
pdf_wm_down_middle = {"title": "/d", "url": "/d"}   # 90% opacity, 0° rotation
# ─────────────────────────────────────────────────────────────────────────────

# ── pdfthumb — load from persistent store on start ───────────────────────────
_THUMB_STORE = "pdfthumb_store.json"

def _load_pdfthumb_from_store() -> str:
    """Bot start par pdfthumb_store.json se last saved thumb load karo."""
    if os.path.exists(_THUMB_STORE):
        try:
            with open(_THUMB_STORE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                last_val = list(data.values())[-1]
                if last_val and last_val != "/d":
                    print(f"[globals] pdfthumb loaded from store: {str(last_val)[:60]}")
                    return last_val
        except Exception as e:
            print(f"[globals] pdfthumb store load error: {e}")
    return "/d"

pdfthumb = _load_pdfthumb_from_store()
