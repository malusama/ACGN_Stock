# -*- coding: utf-8 -*
from .. import app
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from app.forms import (
    Register,
)

from app import handlers


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        if handlers.register(user_name, password, email):
            return redirect(url_for('login'))
        else:
            flash('register fail')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)
