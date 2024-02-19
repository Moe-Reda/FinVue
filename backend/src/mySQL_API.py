from __future__ import annotations

import sys

from flask import Flask, Response, current_app, jsonify, request, url_for
import requests
import pymysql
import hashlib
import random
import string
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# MySQL Configuration
# TODO: Change these values
mysql_host = '100.113.48.195'
mysql_user = 'projectfinance'
mysql_password = 'Finance@2003'
mysql_db = 'finvue'

# Connect to MySQL
db = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,
                     db=mysql_db)
cursor = db.cursor()


# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Endpoint to execute a SELECT query
# Here it is implied that in the database, we have (user_id, username, password...)
@app.route('/api/login_user', methods=['POST'])
def login_user():
    data = request.json
    username = data['username']
    password = hash_password(data['password'])
    try:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        data = cursor.fetchone()
        if data is None:
            return jsonify({'message': 'User not found'}), 404
        elif password != data[3]:
            print(data[3], password)
            return jsonify({'message': 'Invalid login'}), 405
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoint to execute an INSERT query/ REGISTER user
@app.route('/api/register_user', methods=['POST'])
@cross_origin()
def register_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = hash_password(data['password'])  # Hash the password
    try:
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint to execute a DELETE query/ REMOVE user
@app.route('/api/delete_user/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        db.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint to UPDATE a user's password
@app.route('/api/update_user/<string:username>/<string:password>',
           methods=['POST'])
def update_user():
    data = request.json
    username = data['username']
    new_password = hash_password(data['new_password'])  # Hash the new password
    try:
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (new_password, username))
        db.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint to RETRIEVE a new password for someone who forgot a password
# TODO : Change this
@app.route('/api/retrieve_password/<string:username>/<string:email>',
           methods=['GET'])
def retrieve_password(username, email):
    try:
        data = request.json
        username = data[username]
        email = data[email]
        query = "SELECT * FROM users WHERE username = %s AND email = %s"
        cursor.execute(query, (username, email))
        data = cursor.fetchone()
        if data is None:
            return jsonify({'message': 'User not found'}), 404
        new_password = generate_random_string()
        endpoint_url = url_for('api/update_user', _external=True)
        endpoint_url += f"/{username}/{new_password}"
        response, code = requests.get(endpoint_url)
        if code == 200:
            return jsonify({
                'message': f'The new password is: {new_password} and is updated in the database'}), 200
        else:
            return response, code
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


def generate_random_string(length=8):
    """Generate a random alphanumeric string of specified length."""
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))


# Endpoint to CREATE a transaction
@app.route('/api/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    username = data['username']
    # need to get user_id from database by searching database with username
    amount = data['amount']
    category = data.get('category',
                        'Uncategorized')  # Default category to 'Uncategorized' if not provided
    user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
    try:
        cursor.execute(user_id_query, (username,))
        user_id_result = cursor.fetchone()
        if user_id_result is None:
            return jsonify({'message': 'Username not found'}), 404
        user_id = user_id_result[0]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    try:
        query = "INSERT INTO transactions (amount, user_id, category) VALUES (%s, %s, %s)"
        cursor.execute(query, (amount, user_id, category))
        db.commit()
        return jsonify({'message': 'Transaction created successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint to count transactions for a user
@app.route('/api/count_user_transactions/<int:user_id>', methods=['GET'])
def count_user_transactions(user_id):
    try:
        query = "SELECT COUNT(*) FROM transactions WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        transaction_count = cursor.fetchone()[0]
        return jsonify({'count': transaction_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fetch_transactions/<string:username>', methods=['GET'])
def fetch_transactions(username):
    user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
    try:
        cursor.execute(user_id_query, (username,))
        user_id_result = cursor.fetchone()
        if user_id_result is None:
            return jsonify({'message': 'Username not found'}), 404
        user_id = user_id_result[0]
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    transactions_query = "SELECT category, amount FROM transactions WHERE user_id = %s"
    try:
        cursor.execute(transactions_query, (user_id,))
        transactions = cursor.fetchall()

        if not transactions:
            return jsonify(
                {'message': 'No transactions found for the user'}), 404

        transactions_list = [{'category': category, 'amount': amount} for
                             category, amount in transactions]

        return jsonify(transactions=transactions_list), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
