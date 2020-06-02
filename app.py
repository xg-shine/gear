#!/usr/bin/env python
# coding: utf8

from datetime import datetime
from typing import List, Optional

import pydantic
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger(__name__)


class Foo(pydantic.BaseModel):
    count: int
    size: float = None


class Bar(pydantic.BaseModel):
    apple = 'x'
    banana = 'y'
    foos: List[Foo] = []


class User(pydantic.BaseModel):
    id: int
    name: str = "John Wick"
    signup_at: Optional[datetime] = datetime.utcnow()  # 默认值？
    friends: List[int] = []
    size: float = None


app = Flask(__name__)

external_data = {
    'id': '23',
    'signup_at': '2020-06-01 17:30',
    'friends': [],
}


@app.errorhandler(pydantic.ValidationError)
def handle_model_invalid(ex):
    log.error('request: %s %s', request.method, request.full_path)
    return jsonify({
        'success': False,
        'error': str(ex),
        'request': str(request),
    })


# app._register_error_handler(None, pydantic.ValidationError, handle_model_invalid)


@app.route('/user', methods=['GET', 'POST'])
def index():
    log.info('method: %s, req: %s', request.method, request.json)
    user = User(**request.json)
    return jsonify(user.dict())


@app.route('/foo', methods=['POST'])
def foo():
    f = Foo(**request.json)
    return jsonify(f.dict())
