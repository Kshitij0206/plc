from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# ── Email config ──
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gkshitij2026@gmail.com'      # sending from this
app.config['MAIL_PASSWORD'] = 'jkmgskkdzbubftht'
app.config['MAIL_DEFAULT_SENDER'] = 'gkshitij2026@gmail.com'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ── Email route ──
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()

    name    = data.get('name')
    email   = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not all([name, email, subject, message]):
        return jsonify({'success': False, 'error': 'All fields are required.'}), 400

    try:
        msg = Message(
            subject=f"Doubt by {name} regarding {subject}",
            recipients=['gkshitij0206@gmail.com'],           # receiving at this
            body=f"""Hello Kunal! This is an automated response from PLC.

A user by the name {name} with email id {email} has expressed doubt on the matter {subject}.

Complete details given by the user are:
{message}

---
Sent on: {datetime.now().strftime("%d %B %Y, %I:%M %p")}"""
        )
        mail.send(msg)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)