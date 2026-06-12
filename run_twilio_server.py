from flask import Flask, request, render_template_string, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"

saved_posts = [
    {
        "date": "June 11, 2026",
        "caption": "Elegant white & marble luxury kitchen remodel by CC Palms LLC.",
        "image_url": "/static/images/kitchen1.jpg",
        "prompt": "High-end white shaker kitchen with marble island"
    },
    {
        "date": "June 11, 2026",
        "caption": "Sophisticated modern neutral high-end kitchen transformation.",
        "image_url": "/static/images/kitchen2.jpg",
        "prompt": "Luxury gray kitchen with large island"
    },
    {
        "date": "June 11, 2026",
        "caption": "Timeless white & gold luxury kitchen completed by CC Palms LLC.",
        "image_url": "/static/images/kitchen3.jpg",
        "prompt": "Premium white kitchen with gold accents"
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
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .gallery-item { border:1px solid #ddd; border-radius:12px; overflow:hidden; background:white; }
        .gallery-item img { width:100%; height:220px; object-fit:cover; display:block; }
        input, button { padding:12px; margin:8px 0; font-size:16px; border-radius:8px; }
        button { background:#1e40af; color:white; border:none; cursor:pointer; width:100%; }
        .copy-btn { background:#16a34a; width:auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 CC Palms LLC</h1>
        <p><strong>Premium Home Improvement AI Assistant</strong></p>
    </div>
    <div class="container">
        <h2>Welcome back, Lee! 👋</h2>
        <p>System Status • Last updated: {{ now }}</p>

        <div class="card">
            <h3>📱 Generate Social Media Post</h3>
            <form method="post" action="/generate_post">
                <input type="text" name="topic" placeholder="E.g. kitchen remodel, bathroom renovation, outdoor lighting" style="width:100%;">
                <button type="submit">Generate New Post</button>
            </form>
        </div>

        <div class="card">
            <h3>🖼️ Saved Gallery - High-End Kitchens</h3>
            <div class="gallery">
                {% for post in saved_posts %}
                <div class="gallery-item">
                    <small>{{ post.date }}</small>
                    <img src="{{ post.image_url }}" alt="Luxury Kitchen">
                    <p><strong>{{ post.caption }}</strong></p>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('{{ post.caption }}'); alert('✅ Caption copied!')">Copy Caption</button>
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

@app.route('/generate_post', methods=['POST'])
def generate_post():
    topic = request.form.get('topic', 'kitchen remodel')
    return f"""
    <h3>✅ Generated Post for "{topic}"</h3>
    <p><strong>CAPTION:</strong><br>Stunning {topic} by CC Palms LLC – premium quality you can trust.</p>
    <p><strong>IMAGE PROMPT:</strong><br>Professional high-end photo of luxury {topic} project.</p>
    <a href="/">← Back to Dashboard</a>
    """

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 New SMS for CC Palms LLC")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant is LIVE")
    app.run(host='0.0.0.0', port=port)
