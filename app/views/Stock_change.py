# -*- coding: utf-8 -*
from .. import app
from flask import (
    render_template,
    session,
    request,
    jsonify,
)

from app import handlers


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        username = None
        user_authority = '0'
    else:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
    return render_template('stock_change.html',
                           title='ACGN 交易所',
                           user_authority=user_authority
                           )


@app.route('/stock_change/', methods=['GET'])
def stock_change():
    if 'username' not in session:
        username = None
        user_authority = '0'
    else:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
    return render_template('stock_change.html',
                           title='Stock Change',
                           user_authority=user_authority
                           )


@app.route('/api/stock_change/', methods=['GET'])
def get_stock_change():
    result = handlers.get_stock(limit=request.args.get('limit'),
                                offset=request.args.get('offset'),
                                user_id=request.args.get('id'),
                                name=request.args.get('name'),
                                company=request.args.get('company'),
                                factory=request.args.get('factory'),
                                category=request.args.get('category')
                                )
    return jsonify({
        "msg": "tset",
        "count": result[0],
        "offset": request.args.get('offset'),
        "limit": request.args.get('limit'),
        "company": request.args.get('company'),
        "factory": request.args.get('factory'),
        "name": request.args.get('name'),
        "category": request.args.get('category'),
        "stock": result[1]
    })
