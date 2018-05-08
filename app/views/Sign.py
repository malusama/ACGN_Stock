# -*- coding: utf-8 -*
from .. import app
from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    request,
)
from app.forms import (
    LoginForm,
)

from app import handlers


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        if handlers.authorization(user_name, password):
            session['username'] = user_name
            app.logger.info('loggin')
            return redirect(url_for('index'))
        else:
            flash('login find')
            app.logger.info(
                'loggin faid.user={},pd={},result={}'.format(
                    user_name, password,
                    handlers.authorization(user_name, password)))
            return redirect(url_for('login'))
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    # 如果会话中有用户名就删除它。
    # 同时从客户端浏览器中删除 session的 name属性
    flash('logout')
    session.pop('username', None)
    return redirect(url_for('index'))
