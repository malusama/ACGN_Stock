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
from app.forms import (
    Buy_stock
)

from app import handlers


@app.route('/stock/', methods=['GET', 'POST'])
def stock():
    if 'username' not in session:
        username = None
        user_authority = '0'
    else:
        username = session['username']
        user_authority = handlers.get_user_authority(username)
    form = Buy_stock()
    id = request.args.get('id')
    stock = handlers.get_stock(user_id=id)
    stock_order_buy = handlers.get_stock_order(stock_id=id, order_type=1)
    if id:
        return render_template(
            'stock.html',
            stocks=stock,
            title="Stock",
            form=form,
            image="{}{}".format(
                "", handlers.get_stock_cover(request.args.get('id'))),
            stock_id=request.args.get('id'),
            username=username,
            user_authority=user_authority,
            stock_order_buy=stock_order_buy)
    else:
        return redirect(url_for('index'))


@app.route('/api/stock/', methods=['GET'])
def get_stock_order():
    stock_id = request.args.get('id')
    order_type = request.args.get('type')
    # app.logger.info('id:,type:'.format(stock_id, order_type))
    return jsonify({
        "msg": "tset",
        "body": handlers.get_stock_order(
            stock_id=stock_id,
            order_type=order_type)
    })


@app.route('/api/order_submit/', methods=['POST'])
def order_submit():
    msg = handlers.buy_stock(
        stock_id=request.get_json().get('stock_id'),
        order_number=request.get_json().get('order_number'),
        order_price=request.get_json().get('order_price'),
        user_name=session['username'],
        order_type=request.get_json().get('order_type')
    )
    app.logger.info(
        "stock_id:{},order_number:{},order_price:{},order_type:{}".format(
            request.get_json().get('stock_id'),
            request.get_json().get('order_number'),
            request.get_json().get('order_price'),
            request.get_json().get('order_type'),
        ))
    return jsonify({
        'msg': msg,
        'body': request.get_json()
    })


@app.route('/api/Magnet/', methods=['POST'])
def add_Magnet():
    if 'username' in session:
        msg = handlers.addMagnet(
            stock_id=request.get_json().get('stock_id'),
            Magnet=request.get_json().get('Magnet'),
            user_id=handlers.get_userid(session['username']))
        return jsonify({
            "msg": msg
        })
    else:
        return jsonify({
            "msg": "必须登录才可以提交"
        })
    pass


@app.route('/api/Magnet/', methods=['GET'])
def get_Magnet():
    # print(request.args.get('stock_id'))
    magnet = handlers.getMagenet(stock_id=request.args.get('stock_id'))
    return jsonify({
        "msg": 'ok',
        "Magnet": magnet
    })
    pass


@app.route('/api/stockinfo/', methods=['GET'])
def get_Stock_info():
    json = handlers.get_stock_info(stock_id=request.args.get('stock_id'))
    return jsonify({
        "msg": "ok",
        "json": json
    })
    pass
