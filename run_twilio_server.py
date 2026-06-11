from flask import Flask, request, render_template_string, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import datetime
from src.social_content import SocialContentGenerator

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"
generator = SocialContentGenerator()

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
            <form method="post" action="/generate_post">
                <input type="text" name="topic" placeholder="E.g. kitchen remodel, bathroom renovation" style="width:100%; padding:12px; margin-bottom:10px;">
                <button type="submit">Generate New Post</button>
            </form>
        </div>

        <div class="card">
            <h3>🖼️ Saved Gallery</h3>
            <p>Bathroom and kitchen remodel images are saved here.</p>
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

@app.route('/generate_post', methods=['POST'])
def generate_post():
    topic = request.form.get('topic', 'kitchen remodel')
    result = generator.generate_post(topic)
    return f"""
    <h3>Generated Post</h3>
    <p><strong>CAPTION:</strong><br>{result.get('caption', 'No caption')}</p>
    <p><strong>IMAGE PROMPT:</strong><br>{result.get('image_prompt', 'No prompt')}</p>
    <p><a href="/">Back to Dashboard</a></p>
    """

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
