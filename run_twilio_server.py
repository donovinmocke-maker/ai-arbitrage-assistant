from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify
from dotenv import load_dotenv
import os
from datetime import datetime
from src.social_content import SocialContentGenerator

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"
generator = SocialContentGenerator()
saved_posts = []

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
        .post-result { background:#f0fdf4; border-left:5px solid #22c55e; padding:20px; margin-top:15px; border-radius:8px; }
        button { padding:12px 24px; background:#1e40af; color:white; border:none; border-radius:8px; cursor:pointer; font-size:16px; width:100%; margin:8px 0; }
        .copy-btn { background:#22c55e; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-top:15px; }
        .gallery-item { border:1px solid #ddd; border-radius:8px; padding:12px; background:white; }
        .instructions { background:#fefce8; padding:15px; border-radius:8px; font-size:14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 CC Palms LLC</h1>
        <p><strong>Home Improvement AI Assistant</strong></p>
    </div>
    <div class="container">
        {% if not logged_in %}
        <div style="max-width:400px; margin:100px auto; background:white; padding:40px; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.1); text-align:center;">
            <h2>Login for Lee</h2>
            <form method="post">
                <input type="password" name="password" placeholder="Enter Password" style="width:100%; padding:14px; margin:15px 0;">
                <button type="submit" style="width:100%; padding:14px; background:#1e40af; color:white; border:none; border-radius:8px; cursor:pointer;">Login to Dashboard</button>
            </form>
        </div>
        {% else %}
        <h2>Welcome back, Lee! 👋</h2>
        <p>System Status • Last updated: {{ now }}</p>

        <div class="card">
            <h3>📱 Generate Social Media Post</h3>
            <input type="text" id="topic" placeholder="E.g. kitchen remodel, bathroom renovation" style="width:100%; padding:12px; margin-bottom:15px;">
            <button onclick="generatePost()">Generate Post</button>
            <div id="result" class="post-result" style="display:none;"></div>
        </div>

        <div class="card">
            <h3>🖼️ How to Create the Image (Simple Steps)</h3>
            <div class="instructions">
                1. Click <strong>"Copy Image Prompt"</strong><br>
                2. Go to <strong>Grok</strong> (on x.com or Grok app)<br>
                3. Paste the prompt and say "Generate image"<br>
                4. Download the image and post with the caption
            </div>
        </div>

        <div class="card">
            <h3>🖼️ Saved Posts Gallery</h3>
            <div id="gallery" class="gallery"></div>
        </div>

        <div class="card">
            <h3>✅ System Status</h3>
            <p>Grok AI: Online | Twilio SMS: Ready | Social Media: Active</p>
        </div>
        {% endif %}
    </div>

    <script>
        let currentCaption = "";
        let currentPrompt = "";

        async function generatePost() {
            const topic = document.getElementById('topic').value || "kitchen remodel";
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = "Generating...";
            resultDiv.style.display = "block";

            const response = await fetch('/generate_post', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic: topic})
            });
            const data = await response.json();
            
            currentCaption = data.caption;
            currentPrompt = data.image_prompt;

            resultDiv.innerHTML = `
                <strong>CAPTION:</strong><br>${data.caption}<br><br>
                <button class="copy-btn" onclick="copyCaption()">📋 Copy Caption</button><br><br>
                <strong>IMAGE PROMPT:</strong><br>${data.image_prompt}<br><br>
                <button class="copy-btn" onclick="copyPrompt()">📋 Copy Image Prompt</button><br><br>
                <button onclick="saveToGallery()">💾 Save to Gallery</button>
            `;
        }

        function copyCaption() { navigator.clipboard.writeText(currentCaption).then(() => alert("✅ Caption copied!")); }
        function copyPrompt() { navigator.clipboard.writeText(currentPrompt).then(() => alert("✅ Image Prompt copied!")); }

        function saveToGallery() {
            savedPosts.push({
                caption: currentCaption,
                prompt: currentPrompt,
                date: new Date().toLocaleDateString()
            });
            renderGallery();
            alert("✅ Post saved to gallery!");
        }

        function renderGallery() {
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = savedPosts.map((post, index) => `
                <div class="gallery-item">
                    <small>${post.date}</small><br>
                    <p>${post.caption.substring(0, 100)}...</p>
                    <button onclick="copySavedCaption(${index})" style="margin-top:8px; width:auto;">Copy Caption</button>
                </div>
            `).join('');
        }

        function copySavedCaption(index) {
            navigator.clipboard.writeText(savedPosts[index].caption).then(() => alert("✅ Caption copied!"));
        }

        let savedPosts = [];
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
        return redirect(url_for('dashboard'))

    logged_in = session.get('logged_in', False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(DASHBOARD_HTML, logged_in=logged_in, now=now)

@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.get_json()
    topic = data.get('topic', 'recent project')
    result = generator.generate_post(topic)
    return jsonify(result)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
