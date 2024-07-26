from flask import Flask, send_file, request, session, redirect, url_for, render_template
from captcha.image import ImageCaptcha
from io import BytesIO
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secure_persistent_secret_key'  # Use a strong, persistent key

# Route to generate and display CAPTCHA
@app.route('/captcha')
def captcha():
    # Generate random CAPTCHA text
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session['captcha_text'] = text  # Store CAPTCHA text in the session
    
    captcha = ImageCaptcha(width=400, height=220, font_sizes=(40, 70, 100))
    data = BytesIO()
    image = captcha.generate_image(text)
    image.save(data, format='PNG')
    data.seek(0)

    return send_file(data, mimetype='image/png')

# Route to display CAPTCHA form
@app.route('/')
def index():
    return render_template('index.html')

# Route to verify CAPTCHA
@app.route('/verify', methods=['POST'])
def verify():
    user_input = request.form.get('captcha_text')  # Get user input
    captcha_text = session.get('captcha_text')  # Get CAPTCHA text from session
    
    if user_input and captcha_text and user_input == captcha_text:
        return render_template('success.html')  # Render success page
    else:
        return redirect(url_for('index'))  # Redirect to the form for a new CAPTCHA

if __name__ == '__main__':
    app.run(debug=True)
