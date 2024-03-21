from datetime import datetime, timedelta

import requests
from .cryptosRepository import CryptosRepository
import yfinance as yf


class Cryptos:
    cryptosRepository = CryptosRepository()

    def getCryptoTimeSeries(self, crypto, days=7):
        try:
            # Fetch historical crypto data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Download crypto data for the last n days
            crypto_data = yf.download(crypto, start=start_date, end=end_date)

            # Extract closing prices
            closing_prices = [{"day": str(day.date()), "price": price} for day, price in zip(crypto_data.index, crypto_data["Close"])]

            return closing_prices, 200
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred: {e}")
            return {"error": "Error fetching Crypto time series"}, 500

    def getCryptoQuantity(self, username, crypto):
        try:
            user_id_result = self.cryptosRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            quantities = self.cryptosRepository.getCryptoQuantity(user_id, crypto)
            return self.cryptosRepository.getCryptoQuantity(user_id, crypto), 200
        except Exception as e:
            return {'error': str(e)}, 500

    def getPortfolioTimeSeries(self, username, days):
        try:
            cryptos = self.fetchAllCryptos(username)[0]
            cryptos_data = [self.getCryptoTimeSeries(crypto, days)[0] for crypto in cryptos]
            cryptos_quantity = [self.getCryptoQuantity(username, crypto)[0][0] for crypto in cryptos]
            aggregate_prices = {}
            for i, crypto_data in enumerate(cryptos_data):
                for day in crypto_data:
                    aggregate_prices[day["day"]] = aggregate_prices.setdefault(day["day"], 0) + day["price"] * cryptos_quantity[i]
            portfolio_data = []
            for day in aggregate_prices:
                day_data = {
                    "day": day,
                    "price": aggregate_prices[day]
                }
                portfolio_data.append(day_data)
            return portfolio_data, 200
        except Exception as e:
            return {"error": "Error fetching Crypto time series: " + str(e)}, 500

    def fetchAllCryptos(self, username):
        try:
            user_id_result = self.cryptosRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            cryptos = self.cryptosRepository.fetchAll(user_id)

            if not cryptos:
                return {'message': 'No cryptos found for the user'}, 404

            cryptos_list = [tick for crypto in cryptos for tick in crypto]

            return cryptos_list, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def addCrypto(self, tick, username, quantity, order):
        try:
            user_id_result = self.cryptosRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            self.cryptosRepository.addCrypto(tick, user_id, quantity, order)
            return {'message': 'Crypto created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
