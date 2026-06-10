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
        button { padding:10px 16px; background:#1e40af; color:white; border:none; border-radius:6px; cursor:pointer; margin:5px 5px 5px 0; }
        .copy-btn { background:#22c55e; }
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
            <input type="text" id="topic" placeholder="E.g. kitchen remodel, bathroom renovation, new patio" style="width:100%; padding:12px; margin-bottom:10px;">
            <button onclick="generatePost()" style="width:100%;">Generate Instagram / Facebook Post</button>
            <div id="result" class="post-result" style="display:none;"></div>
        </div>

        <div class="card">
            <h3>✅ System Status</h3>
            <p>Grok AI: Online | Twilio SMS: Ready | Social Media: Active</p>
        </div>
        {% endif %}
    </div>

    <script>
        async function generatePost() {
            const topic = document.getElementById('topic').value || "recent remodeling project";
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = "Generating professional post...";
            resultDiv.style.display = "block";

            const response = await fetch('/generate_post', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic: topic})
            });
            const data = await response.json();
            
            resultDiv.innerHTML = `
                <strong>CAPTION:</strong><br>${data.caption}<br><br>
                <button class="copy-btn" onclick="copyText('${data.caption.replace(/'/g, "\\'")}')">📋 Copy Caption</button><br><br>
                <strong>IMAGE PROMPT:</strong><br>${data.image_prompt}<br><br>
                <button class="copy-btn" onclick="copyText('${data.image_prompt.replace(/'/g, "\\'")}')">📋 Copy Image Prompt</button><br><br>
                <strong>HASHTAGS:</strong><br>${data.hashtags}
            `;
        }

        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert("✅ Copied to clipboard!");
            });
        }
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
    content = generator.generate_post(topic)
    
    caption = content.split("IMAGE_PROMPT:")[0].replace("CAPTION:", "").strip() if "CAPTION:" in content else content
    image_prompt = "Professional photo of home improvement project"
    hashtags = "#CCPalmsLLC #HomeRemodeling #FloridaContractor"
    
    if "IMAGE_PROMPT:" in content:
        parts = content.split("IMAGE_PROMPT:")
        caption = parts[0].replace("CAPTION:", "").strip()
        remaining = parts[1]
        if "HASHTAGS:" in remaining:
            image_prompt = remaining.split("HASHTAGS:")[0].strip()
            hashtags = remaining.split("HASHTAGS:")[-1].strip()
        else:
            image_prompt = remaining.strip()
    
    return jsonify({
        "caption": caption,
        "image_prompt": image_prompt,
        "hashtags": hashtags
    })

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
