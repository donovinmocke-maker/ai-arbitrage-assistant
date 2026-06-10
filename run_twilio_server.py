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
            <h3>✅ System Status</h3>
            <p>Grok AI: Online</p>
            <p>Twilio SMS: Ready</p>
            <p>Bookings: Active</p>
        </div>
        
        <div class="card">
            <h3>🏠 CC Palms LLC AI Assistant</h3>
            <p>Your AI answers homeowner texts, schedules site visits, manages remodeling leads, and creates social media posts for your contracting business.</p>
        </div>
        {% endif %}
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

    logged_in = session.get('logged_in', False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(DASHBOARD_HTML, logged_in=logged_in, now=now)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    print("📱 CC Palms SMS received")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
