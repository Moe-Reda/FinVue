from flask import Blueprint, Flask
from flask_cors import CORS, cross_origin

from FinVue.backend.src.app.cryptos.cryptosController import cryptos_blueprint
from FinVue.backend.src.app.currency.currencyController import \
    currency_blueprint
from stocks.stocksController import stocks_blueprint
from user.userController import user_blueprint
from transactions.transactionsController import transactions_blueprint
from budget.budgetController import budgets_blueprint
from savings.savingsController import savings_blueprint
from bills.billsController import bills_blueprint
from news.newsController import news_blueprint


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(transactions_blueprint, url_prefix='/api')
app.register_blueprint(stocks_blueprint, url_prefix='/api')
app.register_blueprint(budgets_blueprint, url_prefix='/api')
app.register_blueprint(savings_blueprint, url_prefix='/api')
app.register_blueprint(cryptos_blueprint, url_prefix='/api')
app.register_blueprint(currency_blueprint, url_prefix='/api')
app.register_blueprint(bills_blueprint, url_prefix='/api')
app.register_blueprint(news_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)