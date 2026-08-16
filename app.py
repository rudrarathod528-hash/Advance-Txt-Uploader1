import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digizoro Bot</title>
    <!-- ========== ARZANXD ========== -->
    <style>
        /* ─── Base ─── */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0b0b0b;
            color: #eee;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 780px;
            width: 100%;
            background: #121212;
            border-radius: 32px;
            padding: 50px 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            border: 1px solid #2a2a2a;
            text-align: center;
            transition: all 0.3s;
        }

        /* ─── Logo / Brand ─── */
        .logo {
            font-size: 1.6rem;
            font-weight: 900;
            letter-spacing: 6px;
            color: #a855f7;
            text-shadow: 0 0 20px #a855f766;
            margin-bottom: 10px;
            font-family: 'Courier New', monospace;
        }
        .logo span {
            color: #f0abfc;
        }

        /* ─── Title ─── */
        h1 {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 10px 0 8px;
            letter-spacing: 2px;
        }

        .tagline {
            color: #888;
            font-size: 1.1rem;
            letter-spacing: 3px;
            margin-bottom: 30px;
            border-bottom: 1px solid #2a2a2a;
            padding-bottom: 20px;
        }

        /* ─── Power & Join ─── */
        .credit {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin: 25px 0 10px;
        }
        .powered {
            background: #1e1e1e;
            padding: 12px 30px;
            border-radius: 60px;
            border: 1px solid #a855f755;
            box-shadow: 0 0 30px #a855f722;
            font-size: 1.1rem;
        }
        .powered a {
            color: #a855f7;
            text-decoration: none;
            font-weight: 700;
            transition: 0.3s;
        }
        .powered a:hover {
            text-shadow: 0 0 30px #a855f7;
            color: #fff;
        }
        .team {
            color: #666;
            font-size: 0.95rem;
            letter-spacing: 1px;
        }
        .team strong {
            color: #a855f7;
            font-weight: 700;
        }

        /* ─── Status ─── */
        .status {
            margin-top: 25px;
            color: #4ade80;
            font-weight: 500;
            font-size: 0.9rem;
            letter-spacing: 2px;
            background: #1a2a1a;
            display: inline-block;
            padding: 6px 24px;
            border-radius: 40px;
            border: 1px solid #4ade8055;
        }

        /* ─── Footer ─── */
        .footer {
            margin-top: 30px;
            color: #444;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }

        /* ─── Responsive ─── */
        @media (max-width: 480px) {
            .container { padding: 30px 15px; }
            h1 { font-size: 2rem; }
            .logo { font-size: 1.2rem; }
            .powered { font-size: 0.95rem; padding: 10px 20px; }
        }

        /* ============================================= */
        /* ==== ARZANXD ==== */
        /* ============================================= */
        /* Example: change colors, fonts, background, etc. */
    </style>
</head>
<body>
    <div class="container">

        <!-- Logo / Brand (replace with your own ASCII or image) -->
        <div class="logo">
            ⚡ <span>DIGIZORO</span> ⚡
        </div>

        <h1>Uploader Bot</h1>
        <div class="tagline">✦ smooth · smart · seamless ✦</div>

        <div class="credit">
            <div class="powered">
                🚀 Powered by <a href="https://t.me/Digizoro_Official" target="_blank">Digizoro</a>
                <span style="color:#888;margin:0 6px;">—</span>
                <a href="https://t.me/Digizoro_Official" target="_blank" style="color:#c084fc;">join here for free courses and much more</a>
            </div>
            <div class="team">
                Team: <strong>ArzanXD</strong>
            </div>
        </div>

        <div class="status">✅ Running flawlessly</div>

        <div class="footer">
            ✦ crafted with precision ✦
        </div>

    </div>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)