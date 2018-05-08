# -*- coding: utf-8 -*
from .. import app
from flask import (
    render_template,
    session,
    request,
    jsonify,
)

from app import handlers


@app.route('/stock_apply/', methods=['GET'])
def stock_apply():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('stock_apply.html', username=username)


@app.route('/api/stock_apply/', methods=['POST'])
def stock_apply_submit():
    # print(request.get_json())
    try:
        msg = handlers.stock_apply(user_id=request.get_json().get('user_id'),
                                   stock_name=request.get_json().get('stock_name'),
                                   stock_image=request.get_json().get('stock_image'),
                                   stock_cover=request.get_json().get('stock_cover'),
                                   stock_introduction=request.get_json().get('stock_introduction'),
                                   apply_status=0)
    except ValueError:
        msg = '输入参数异常'

    return jsonify({
        "msg": msg
    })


@app.route('/apply_review/', methods=['GET'])
def apply_review():
    if 'username' in session:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
    else:
        username = None
    return render_template('apply_review.html',
                           username=username,
                           user_authority=user_authority)


@app.route('/api/get_apply/', methods=['GET'])
def get_apply():
    stock_apply = handlers.get_apply()
    return jsonify({
        "json": stock_apply
    })


@app.route('/api/apple_pass/', methods=['POST'])
def apple_pass():
    if 'username' in session:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
        if user_authority == "1":
            msg = handlers.review_pass(request.get_json().get('id'))
            return jsonify({
                "msg": msg
            })
        else:
            return jsonify({
                "msg": "用户权限不够"
            })
    else:
        return jsonify({
            "msg": "用户不存在"
        })
