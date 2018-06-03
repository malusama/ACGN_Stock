# -*- coding: utf-8 -*
from .. import app
from flask import (
    render_template,
    redirect,
    session,
    url_for,
    request,
    jsonify,
)

from app import handlers


@app.route('/user/', methods=['GET', 'POST'])
def user():
    id = request.args.get('id')
    user, user_stock = handlers.get_user_stock(id)
    if user:
        return render_template('user.html',
                               username=user.nickname,
                               user=user,
                               user_stock=user_stock)
    else:
        return redirect(url_for('index'))


@app.route('/api/user_id/', methods=['GET'])
def get_userid():
    print(session.items())
    if 'username' in session:
        username = session['username']
        userid = handlers.get_userid(username)
        msg = 'ok'
        return jsonify({
            "msg": msg,
            "userid": userid
        })

    else:
        username = 'None'
        msg = '没有用户'
        return jsonify({
            "msg": msg,
            "userid": username
        })


@app.route('/api/user_id_authority/', methods=['GET'])
def get_userid_authority():
    if 'username' in session:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
        msg = 'ok'
        return jsonify({
            "msg": msg,
            "user_id_authority": user_authority
        })

    else:
        user_authority = 'None'
        msg = '没有用户'
        return jsonify({
            "msg": msg,
            "user_authority": user_authority
        })
