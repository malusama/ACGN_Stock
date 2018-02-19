from app import (
    models,
    lm,
    oid,
    app,
    handle
)
from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    request,
    jsonify,
)
from .forms import LoginForm, Register, Buy_stock


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = 'None'
    return render_template('index.html',
                           title='ACGN Stock Change',
                           username=username,
                           posts=handle.get_post())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        if handle.authorization(user_name, password):
            session['username'] = user_name
            app.logger.info('loggin')
            return redirect(url_for('index'))
        else:
            flash('login find')
            app.logger.info(
                'loggin faid.user={},pd={},result={}'.format(
                    user_name, password,
                    handle.authorization(user_name, password)))
            return redirect(url_for('login'))
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    # 如果会话中有用户名就删除它。
    # 同时从客户端浏览器中删除 session的 name属性
    flash('logout')
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        if handle.register(user_name, password, email):
            return redirect(url_for('login'))
        else:
            flash('register fail')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/stock_change', methods=['GET', 'POST'])
def stock_change():
    stock = handle.get_stock()
    return render_template('stock_change.html',
                           title='Stock Change',
                           username=session['username'],
                           stocks=stock)


@app.route('/stock/', methods=['GET', 'POST'])
def stock():
    form = Buy_stock()
    id = request.args.get('id')
    stock_info = handle.get_stock(id)
    stock_order_buy = handle.get_stock_order(stock_id=id, order_type=1)
    if form.validate_on_submit():
        number = request.form.get('num', None)
        status = handle.buy_stock(
            id=id, number=number, user_name=session['username'])
        stock_info = handle.get_stock(id)
        if status == 1:
            flash('buy:{}'.format(number))
            app.logger.info('buy:{}'.format(request.form.get('num', None)))
        if status == 2:
            flash('购买失败，余额不足')
    if id:
        return render_template(
            'stock.html',
            stocks=stock_info,
            form=form,
            stock_id=request.args.get('id'),
            username=session['username'],
            stock_order_buy=stock_order_buy)
    else:
        return redirect(url_for('index'))


@app.route('/api/stock/', methods=['GET'])
def get_stock_order():
    stock_id = request.args.get('id')
    order_type = request.args.get('type')
    app.logger.info('id:,type:'.format(stock_id, order_type))
    return jsonify({
        "msg": "tset",
        "body": handle.get_stock_order(
            stock_id=stock_id,
            order_type=order_type)
    })


@app.route('/api/order_submit/', methods=['POST'])
def order_submit():
    msg = handle.buy_stock(
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


@app.route('/user/', methods=['GET', 'POST'])
def user():
    id = request.args.get('id')
    user, user_stock = handle.get_user_stock(id)
    if user:
        return render_template('user.html',
                               username=user.nickname,
                               user=user,
                               user_stock=user_stock)
    else:
        return redirect(url_for('index'))
