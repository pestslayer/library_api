from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import User, Stock, stock_schema, stocks_schema, db

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{'Test': 'complete'}

@api.route('/stock', methods = ['POST'])
@token_required
def create_stock(current_user_token):
    title = request.json['title']
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    book_length = request.json['book_length']
    book_type = request.json['book_type']
    user_token = current_user_token.token

    print(f'Test: {user_token}')

    stock = Stock(title, isbn, author_name, book_length, book_type, user_token=user_token)

    db.session.add(stock)
    db.session.commit()

    response = stock_schema.dump(stock)
    return jsonify(response)

@api.route('/stock', methods = ['GET'])
@token_required
def get_stock(current_user_token):
    a_user = current_user_token.token
    stocks = Stock.query.filter_by(user_token = a_user).all()
    response = stocks_schema.dump(stocks)
    return jsonify(response)

@api.route('/stock/<id>', methods = ['GET'])
@token_required
def get_single_stock(current_user_token, id):
    stock = Stock.query.get(id)
    response = stock_schema.dump(stock)
    return jsonify(response)

@api.route('/stock/<id>', methods = ['POST', 'PUT'])
@token_required
def update_stock(current_user_token,id):
    stock = Stock.query.get(id)
    stock.title = request.json['title']
    stock.isbn = request.json['isbn']
    stock.author_name = request.json['author_name']
    stock.book_length = request.json['book_length']
    stock.book_type = request.json['book_type']
    stock.user_token = current_user_token.token

    db.session.commit()
    response = stock_schema.dump(stock)
    return jsonify(response)

@api.route('/stock/<id>', methods = ['DELETE'])
@token_required
def delete_stock(current_user_token, id):
    stock = Stock.query.get(id)
    db.session.delete(stock)
    db.session.commit()
    response = stock_schema.dump(stock)
    return jsonify(response)
