from flask import Flask, render_template, request, session, jsonify
import smtplib
import random
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'super_maxfiy_kalit'

# EMAIL SOZLAMALARI - DIQQAT: Bularni o'zingizniki bilan almashtiring!
MY_EMAIL = "sattorxonovas@gmail.com"
MY_PASSWORD = "ivps plce laqf zmvx" # Agarda xato bersa, yangi App Password oling

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp

        msg = EmailMessage()
        msg['Subject'] = "Sizning tasdiqlash kodingiz"
        msg['From'] = MY_EMAIL
        msg['To'] = email
        msg.set_content(f"❗Salom Ro'yxatdan o'tish kodingiz: {otp}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MY_EMAIL, MY_PASSWORD)
            server.send_message(msg)
        
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    user_otp = "".join(data.get('otp'))
    if user_otp == session.get('otp'):
        return jsonify({"status": "success", "message": "Muvaffaqiyatli o'tdingiz!"})
    else:
        return jsonify({"status": "fail", "message": "Kod xato!"})

if __name__ == '__main__':
    app.run(debug=True)