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
        table { width:100%; border-collapse:collapse; }
        th, td { padding:12px; text-align:left; border-bottom:1px solid #eee; }
        .status { color:#22c55e; font-weight:bold; }
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

        <!-- System Status -->
        <div class="card">
            <h3>✅ System Status</h3>
            <p><strong>Grok AI:</strong> Online</p>
            <p><strong>Twilio SMS:</strong> Ready</p>
            <p><strong>Bookings:</strong> Active</p>
        </div>

        <!-- Upcoming Jobs -->
        <div class="card">
            <h3>📅 Upcoming Jobs</h3>
            <table>
                <tr><th>Client</th><th>Project</th><th>Date</th><th>Status</th></tr>
                <tr><td>John Smith</td><td>Kitchen Remodel</td><td>June 12</td><td>Confirmed</td></tr>
                <tr><td>Maria Lopez</td><td>Bathroom Renovation</td><td>June 15</td><td>Site Visit</td></tr>
            </table>
        </div>

        <!-- Active Leads -->
        <div class="card">
            <h3>🚀 Active Leads</h3>
            <table>
                <tr><th>Client</th><th>Project</th><th>Source</th><th>Next Action</th></tr>
                <tr><td>David Chen</td><td>Roof Repair</td><td>Text</td><td>Send Quote</td></tr>
                <tr><td>Lisa Patel</td><td>Full Home Remodel</td><td>Website</td><td>Schedule Visit</td></tr>
            </table>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <h3>⚡ Quick Actions</h3>
            <p><strong>Send Broadcast Message</strong> • Generate Social Post • View All Leads</p>
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
