from flask import Flask, request, render_template_string, session, redirect, url_for
from dotenv import load_dotenv
import os
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_PASSWORD = "ccpalms2026"

# Simple handler for now (we'll expand later)
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
        return redirect(url_for('dashboard'))

    logged_in = session.get('logged_in', False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>CC Palms LLC - AI Assistant</title>
    <style>body { font-family: Arial; background:#f0f7ff; } .header { background: linear-gradient(135deg, #1e40af, #3b82f6); color:white; padding:40px; text-align:center; } .card { background:white; padding:25px; margin:20px; border-radius:12px; }</style>
    </head>
    <body>
        <div class="header"><h1>🏠 CC Palms LLC</h1><p><strong>AI Virtual Assistant</strong></p></div>
        <div class="card">
            <h2>Welcome back, Lee!</h2>
            <p>System Status: ✅ Live</p>
            <p>Your AI is ready to handle customer texts and schedule jobs.</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    from_number = request.form.get('From')
    body = request.form.get('Body', '')
    
    print(f"📱 New message from {from_number}: {body}")
    
    resp = MessagingResponse()
    resp.message("Thank you for contacting CC Palms LLC. We'll get back to you shortly about your home improvement project.")
    
    return str(resp), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CC Palms LLC AI Assistant running on port {port}")
    app.run(host='0.0.0.0', port=port)
