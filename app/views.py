from flask import render_template, flash, redirect, session, url_for, request, g,current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm,db,mail
from .forms import LoginForm,SignupForm,RechangeForm
from .models import User
from .email import send_email
from .draw import Recaptcha
import io

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
            flash(u'用户名或密码错误')
            return redirect(url_for('login'))
        flash(u'未找到该用户')
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
        flash(u'已向您的邮箱发送确认邮件')
        login_user(user)
        return redirect(url_for('hello'))
    return render_template('signup.html',
        title = 'Sign Up',
        form = form)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('hello'))
    if current_user.confirm(token):
        flash(u'认证成功')
        return redirect(url_for('index'))
    else:
        flash(u'认识失败')
    return redirect(url_for(index))

@app.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','confirm',user = current_user,token = token)
    flash(u'已重新发送确认邮件，请注意查收')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功')
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
        flash('修改成功')
        return redirect(url_for('hello'))
    return render_template('rechange.html',
        title = 'Sign Up',
        form = form)

@app.route('/code', methods=['GET'])
def generate_code():
    """生成验证码
    """
    ic = Recaptcha(fontColor=(100,211, 90))
    strs,code_img = ic.generate()
    session['S_RECAPTCHA']= str(strs)
    buf = io.BytesIO()
    code_img.save(buf,'JPEG',quality=70)
    buf_str = buf.getvalue()
    response = current_app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response



