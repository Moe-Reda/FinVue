from flask import Blueprint, Flask
from flask_cors import CORS, cross_origin

from stocks.stocksController import stocks_blueprint
from user.userController import user_blueprint
from transactions.transactionsController import transactions_blueprint

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(transactions_blueprint, url_prefix='/api')
app.register_blueprint(stocks_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
