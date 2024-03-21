from datetime import datetime, timedelta

import requests
from .stocksRepository import StocksRepository
import yfinance as yf


class Stocks:
    stocksRepository = StocksRepository()

    def getStockTimeSeries(self, stock, days=7):
        try:
            # Fetch historical stock data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Download stock data for the last n days
            stock_data = yf.download(stock, start=start_date, end=end_date)

            # Extract closing prices
            closing_prices = [{"day": str(day.date()), "price": price} for day, price in zip(stock_data.index, stock_data["Close"])]

            return closing_prices, 200
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred: {e}")
            return {"error": "Error fetching Stock time series"}, 500

    def getStockQuantity(self, username, stock):
        try:
            user_id_result = self.stocksRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            quantities = self.stocksRepository.getStockQuantity(user_id, stock)
            return self.stocksRepository.getStockQuantity(user_id, stock), 200
        except Exception as e:
            return {'error': str(e)}, 500

    def getPortfolioTimeSeries(self, username, days):
        try:
            stocks = self.fetchAllStocks(username)[0]
            stocks_data = [self.getStockTimeSeries(stock, days)[0] for stock in stocks]
            stocks_quantity = [self.getStockQuantity(username, stock)[0][0] for stock in stocks]
            aggregate_prices = {}
            for i, stock_data in enumerate(stocks_data):
                for day in stock_data:
                    aggregate_prices[day["day"]] = aggregate_prices.setdefault(day["day"], 0) + day["price"] * stocks_quantity[i]
            portfolio_data = []
            for day in aggregate_prices:
                day_data = {
                    "day": day,
                    "price": aggregate_prices[day]
                }
                portfolio_data.append(day_data)
            return portfolio_data, 200
        except Exception as e:
            return {"error": "Error fetching Stock time series: " + str(e)}, 500

    def fetchAllStocks(self, username):
        try:
            user_id_result = self.stocksRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            stocks = self.stocksRepository.fetchAll(user_id)

            if not stocks:
                return {'message': 'No stocks found for the user'}, 404

            stocks_list = [tick for stock in stocks for tick in stock]

            return stocks_list, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def addStock(self, tick, username, quantity, order):
        try:
            user_id_result = self.stocksRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            self.stocksRepository.addStock(tick, user_id, quantity, order)
            return {'message': 'Stock created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
