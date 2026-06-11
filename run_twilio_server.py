from flask import Flask, request, render_template_string, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"

# Saved posts with images
saved_posts = [
    {
        "caption": "Professional, bright photograph of a modern luxury kitchen remodel with white shaker cabinets, large marble island, brushed gold hardware, stainless steel appliances, and natural light.",
        "image_url": "https://picsum.photos/id/1015/800/600",  # Placeholder for now
        "date": "June 11, 2026"
    }
]

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
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }
        .gallery-item { border:1px solid #ddd; border-radius:8px; padding:12px; background:white; }
        img { max-width:100%; border-radius:8px; margin:8px 0; }
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
            <button onclick="alert('Social media tool is ready.\\n\\nType a topic and click Generate to create posts.')">Generate New Post</button>
        </div>

        <div class="card">
            <h3>🖼️ Saved Gallery</h3>
            <div class="gallery">
                {% for post in saved_posts %}
                <div class="gallery-item">
                    <small>{{ post.date }}</small><br>
                    <p>{{ post.caption[:100] }}...</p>
                    {% if post.image_url %}
                    <img src="{{ post.image_url }}" alt="Generated Image">
                    {% endif %}
                </div>
                {% endfor %}
            </div>
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
    return render_template_string(DASHBOARD_HTML, now=now, saved_posts=saved_posts)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
