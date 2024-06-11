from flask import render_template, url_for, flash, redirect, request
from careercrafter import app, db, bcrypt, mail
from careercrafter.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, VerifyOtpForm
from careercrafter.models import users, careers, d
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import random
import pandas as pd
from careercrafter.prediction import X_personality, knn_personality, encoder, career_dataset
 


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.htm')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in Unsuccessfull. Please check email and password', 'danger')
    return render_template('login.htm', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users(user_name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.htm', title='Register', form=form)


@app.route('/account')
@login_required
def account():
    if current_user.is_authenticated:
        predicted_personality_type = current_user.personality_type
    predicted_career = career_dataset[career_dataset['Personality Type'] == predicted_personality_type][
            'Career'].tolist()
    return render_template('account.htm', title='Account', predicted_career=predicted_career)


# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)  # Generate a 6-digit OTP, change as needed


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = users.query.filter_by(email=email).first()
        if user:
            otp = generate_otp()
            user.otp = otp
            db.session.commit()
            msg = Message('Forgot Password OTP', recipients=[email])
            msg.body = f'Your one-time password (OTP) for password reset is: {otp}'
            mail.send(msg)
            flash('OTP sent to your email. Check your inbox and enter the OTP below.')
            return redirect(url_for('verify_otp', email=email))
        else:
            flash('Email address not found.')
    return render_template('forgot_password.html', form=form)


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    email = request.args.get('email')
    if email:
        user = users.query.filter_by(email=email).first()
        if user:
            if request.method == 'POST':
                otp_entered = int(request.form['otp'])
                if otp_entered == user.otp:
                    flash('OTP verified successfully. You can now reset your password.')
                    return redirect(url_for('reset_password', email=email))
                else:
                    flash('Invalid OTP. Please try again.')
    else:
        flash('Invalid request. Please provide a valid email address.')
        return redirect(url_for('forgot_password'))
    return render_template('verify_otp.html', email=email)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    email = request.args.get('email')
    if email:
        user = users.query.filter_by(email=email).first()
        if user:
            if form.validate_on_submit():
                new_password = form.password.data
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.password = hashed_password
                user.otp = None 
                db.session.commit()
                flash('Password reset successful. You can now login with your new password.')
                return redirect(url_for('login'))
        else:
            flash('Invalid request. Please provide a valid email address.')
            return redirect(url_for('forgot_password'))
    return render_template('reset_password.htm', form=form, email=email)



def add_personality_to_user(email, personality_type):
    # Find the user by email
    user = users.query.filter_by(email=email).first()

    if user:
        # Update the user's personality type
        user.personality_type = personality_type
        db.session.commit()
        return True
    else:
        return False



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        user_answers = []
        for i in range(len(X_personality.columns)):
            answer = request.form[f"question_{i + 1}"]
            try:
                converted_answer = (int(answer) * 6 // 100) - 3
                user_answers.append(int(-converted_answer))
            except KeyError:
                print("KeyError occurred for answer:", answer)
                user_answers.append(0)

        user_answers_df = pd.DataFrame([user_answers], columns=X_personality.columns)

        # Predict personality type
        predicted_personality = knn_personality.predict(user_answers_df)[0]

        # Decode the predicted personality type from numerical representation to label
        predicted_personality_type = encoder.inverse_transform([predicted_personality])[0]

        # Predict career based on predicted personality type
        predicted_career = career_dataset[career_dataset['Personality Type'] == predicted_personality_type][
            'Career'].tolist()
        
        personality_details = d.query.filter_by(personality_type=predicted_personality_type).first()
        description = personality_details.description if personality_details else "Not found."

        # add_personality_to_user(email, predicted_personality_type)
        if current_user.is_authenticated:
            email = current_user.email
            add_personality_to_user(email, predicted_personality_type)

        return render_template('result.htm', predicted_personality_type=predicted_personality_type,
                               description=description,
                               predicted_career=predicted_career)
    return render_template('index.htm', title='Personality Test')


@app.route('/result')
def result():
    return render_template('result.htm', title='Careers')

@app.route('/result/<string:title>')
def career(title):
    career = careers.query.get_or_404(title)
    return render_template('career.html', title=career.title, career=career)


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('404.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('404.html'), 500