from flask import Blueprint, jsonify, request
from .loginUseCase import Login
from .registerUseCase import Register
from .hashPassword import HashPassword

user_blueprint = Blueprint('user', __name__)
login_use_case = Login()
register_use_case = Register()

@user_blueprint.route('/login_user', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = HashPassword.hash_password(data['password'])
    msg = login_use_case.login_user(username, password)
    return jsonify(msg[0]), msg[1]


@user_blueprint.route('/logout')
def logout():
    return 'Logout'


@user_blueprint.route('/register_user', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = HashPassword.hash_password(data['password'])
    msg = register_use_case.register_user(email, username, password)
    return jsonify(msg[0]), msg[1]
