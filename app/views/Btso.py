# -*- coding: utf-8 -*
from .. import app
from flask import (
    request,
    jsonify,
)

from app.handlers.btso import (
    btsoSearch
)


@app.route('/api/btso/', methods=['GET'])
def btso():
    return jsonify({
        "msg": "tset",
        "json": btsoSearch(keywords=request.args.get('keywords')),
    })
