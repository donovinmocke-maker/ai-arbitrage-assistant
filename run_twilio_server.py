from flask import Flask, request, render_template_string, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CC Palms LLC - AI Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin:0; background:#f0f7ff; }
        .header { background: linear-gradient(135deg, #1e40af, #3b82f6); color:white; padding:40px; text-align:center; }
        .container { max-width:1200px; margin:30px auto; padding:20px; }
        .card { background:white; border-radius:12px; padding:25px; margin-bottom:25px; box-shadow:0 4px 15px rgba(0,0,0,0.1); }
        button { padding:14px 28px; background:#1e40af; color:white; border:none; border-radius:8px; cursor:pointer; font-size:16px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 CC Palms LLC</h1>
        <p><strong>Home Improvement AI Assistant</strong></p>
    </div>
    <div class="container">
        <h2>Welcome back, Lee! 👋</h2>
        <p>System Status • Last updated: {{ now }}</p>

        <div class="card">
            <h3>📱 Social Media Tool</h3>
            <p>Generate captions and image prompts for Instagram & Facebook.</p>
            <button onclick="alert('Social media generation is ready.\\n\\nType a topic like \"kitchen remodel\" in the input box and click Generate.')">Generate New Post</button>
        </div>

        <div class="card">
            <h3>🖼️ Saved Gallery</h3>
            <p>Bathroom and kitchen remodel images are saved here for easy access.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
        return redirect(url_for('dashboard'))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(DASHBOARD_HTML, now=now)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
