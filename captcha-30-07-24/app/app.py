from flask import Flask, send_file, request, session, redirect, url_for, render_template, abort
from captcha.image import ImageCaptcha
from io import BytesIO
import random
import string
from datetime import datetime, timedelta
import os
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secure_persistent_secret_key')

# CSRF Protection
csrf = CSRFProtect(app)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/captcha')
@limiter.limit("10 per minute")
def captcha():
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session['captcha_text'] = text
    session['captcha_expiry'] = (datetime.utcnow() + timedelta(minutes=5)).isoformat()  # Store as ISO string

    captcha = ImageCaptcha(width=400, height=220, font_sizes=(40, 70, 100))
    data = BytesIO()
    image = captcha.generate_image(text)
    image.save(data, format='PNG')
    data.seek(0)

    return send_file(data, mimetype='image/png')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
@limiter.limit("5 per minute")
def verify():
    user_input = request.form.get('captcha_text')
    captcha_text = session.get('captcha_text')
    captcha_expiry_str = session.get('captcha_expiry')

    if not captcha_text or not captcha_expiry_str:
        abort(400, description="Captcha expired or missing")  # Provide meaningful error

    captcha_expiry = datetime.fromisoformat(captcha_expiry_str)  # Convert from ISO string

    # Check if the captcha has expired
    if datetime.utcnow() > captcha_expiry:
        abort(400, description="Captcha expired")  # Provide meaningful error

    # Validate captcha
    if user_input and user_input == captcha_text:
        return render_template('success.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production