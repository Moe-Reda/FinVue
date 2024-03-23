import yfinance as yf


class ExchangeCurrency:

    def exchangeCurrency(self, source, target, amount):
        try:
            ticker_symbol = f"{source}{target}=X"
            ticker_data = yf.Ticker(ticker_symbol)

            # Fetch the latest close price as the exchange rate
            hist = ticker_data.history(period="1d")
            exchange_rate = hist['Close'].iloc[-1]
            return amount * exchange_rate, 200
        except Exception as e:
            return {'error': str(e)}, 500
