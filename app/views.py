from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm,db,mail
from .forms import LoginForm,SignupForm,RechangeForm
from .models import User
from .email import send_email

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",title = 'Home')

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login',methods = ['GET','POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = str(form.username.data)
        password = str(form.password.data)
        remember_me = request.form.get('rememberme',False)
        user = User.query.filter_by(username = user_name).first()
        if user is not None:
            if user.verify_password(password):
                login_user(user,remember = remember_me)
                return redirect(url_for('hello'))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        flash('the username not exit')
    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/signup',methods = ['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username = str(form.username.data),
            password = str(form.password.data),email = str(form.email.data))
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account','confirm',user = user,token = token)
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('index'))
    return render_template('signup.html',
        title = 'Sign Up',
        form = form)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('hello'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
        return redirect(url_for('hello'))
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for(index))

@app.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    print(current_user.email)
    send_email(current_user.email,'Confirm Your Account','confirm',user = current_user,token = token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been loggged out.')
    return redirect(url_for('index'))

@app.route('/hello')
@login_required
def hello():
    return render_template('hello.html',title = 'hello')

@app.route('/rechange',methods = ['GET','POST'])
@login_required
def rechange():
    form = RechangeForm()
    if form.validate_on_submit():
        current_user.password = str(form.newpassword.data)
        db.session.add(current_user)
        db.session.commit()
        flash('Your password has been rechanged')
        return redirect(url_for('hello'))
    return render_template('rechange.html',
        title = 'Sign Up',
        form = form)



