# -*- coding: utf-8 -*-
"""Gemini-task5-p1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t2mei_TMlnNaLPOVYti8pvkpthLBuneq
"""

from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# In-memory product and user data
products = {
    '1': {'name': 'T-Shirt', 'price': 20.0, 'description': 'A comfortable cotton T-Shirt'},
    '2': {'name': 'Coffee Mug', 'price': 15.0, 'description': 'Start your day with a smile'},
}

users = {
    'admin': {'password': generate_password_hash('secret')}
}

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(list(products.values()))

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    if product_id not in products:
        abort(404)
    return jsonify(products[product_id])

def _requires_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.authorization:
            abort(401)
        username, password = request.authorization.username, request.authorization.password
        if not username or not password or not is_admin(username) or not check_password_hash(users[username]['password'], password):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

@app.route('/products', methods=['POST'])
#@_requires_admin
def add_product():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not all(key in data for key in ('name', 'price', 'description')):
        abort(400)
    new_id = str(max(int(key) for key in products.keys()) + 1)
    products[new_id] = data
    return jsonify({'message': 'Product added successfully', 'id': new_id})

@app.route('/products/<product_id>', methods=['PUT'])
#@_requires_admin
def update_product(product_id):
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if product_id not in products:
        abort(404)
    products[product_id].update(data)
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<product_id>', methods=['DELETE'])
#@_requires_admin
def delete_product(product_id):
    if product_id not in products:
        abort(404)
    del products[product_id]
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not all(key in data for key in ('username', 'password')):
        abort(400)
    if data['username'] not in users:
        abort(400)
    if not check_password_hash(users[data['username']]['password'], data['password']):
        abort(400)
    return jsonify({'message': 'Logged in successfully'})

def is_admin(username):
    return username == 'admin'

if __name__ == '__main__':
    app.run(debug=True)