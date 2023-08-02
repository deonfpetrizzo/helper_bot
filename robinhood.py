import json
import time
from helpers import *
import robin_stocks.robinhood as r
from urls import ROBINHOOD_URL

class Robinhood:
    """base class for Portfolio and Stocks"""
    def __init__(self, acct_file_path):
        self.acct_file_path = acct_file_path
        self.__login()
        pass

    def __login(self):
        """logs into robinhood"""
        with open(self.acct_file_path, "r", encoding="utf-8") as f:
            acct = json.load(f)
        r.login(acct["username"], acct["password"], by_sms=True)

class Portfolio(Robinhood):
    """portfolio of traded securities"""
    def __init__(self, acct_file_path):
        super().__init__(acct_file_path)
        self.positions = self.__positions()
        self.starting_values = self.__previous_close_prices()

    def __positions(self):
        """returns a list of all open positions"""
        raw_positions = r.get_open_stock_positions()
        tickers = [r.get_symbol_by_url(item["instrument"]) for item in raw_positions]
        prices = r.get_quotes(tickers, "last_trade_price")
        quantities = [float(item["quantity"]) for item in raw_positions]
        positions = [(tickers[i], float(prices[i]), float(quantities[i])) for i in range(len(raw_positions))]
        return positions

    def __previous_close_prices(self):
        """gets the previous close price for all stocks in the portfolio"""
        starting_values = []
        for pos in self.positions:
            starting_values.append(float(r.get_quotes(pos[0], "previous_close")[0]))
        return starting_values

    def __position_pnls(self):
        """returns the pnl of each position as money and percentage values"""
        i = 0
        pnls = []
        percentile_pnls = []
        for pos in self.positions:
            first = self.starting_values[i]
            last = pos[1]
            quantity = pos[2]
            pnl = (last - first) * quantity
            percentile_pnl = 100 * (last - first) / first
            pnls.append(pnl)
            percentile_pnls.append(percentile_pnl)
            i += 1
        return pnls, percentile_pnls

    def __portfolio_pnl(self):
        """returns the overall pnl of the portfolio as money and percentage values"""
        value = self.__portfolio_value()
        initial_value = self.__portfolio_initial_value()
        pnl = value - initial_value
        percentile_pnl = 100 * (value - initial_value) / initial_value
        return pnl, percentile_pnl

    def __portfolio_value(self):
        """returns the value of the portfolio"""
        values = [pos[1]*pos[2] for pos in self.positions]
        return sum(values)

    def __portfolio_initial_value(self):
        """returns the value of the portfolio at the end of the last trading period"""
        values = [self.starting_values[i]*self.positions[i][2] for i in range(len(self.positions))]
        return sum(values)

    def performance(self):
        """prints portfolio's performance, detailing all open positions"""
        position_pnls, position_percentile_pnls = self.__position_pnls()
        portfolio_pnl, portfolio_percentile_pnl = self.__portfolio_pnl()
        portfolio_value = self.__portfolio_value()

        i = 0
        pad = lambda s : s.ljust(12)
        position_performance = f"{pad('ticker')}{pad('price')}{pad('shares')}{pad('pnl')}\n"
        for pos in self.positions:
            ticker = pos[0]
            price = n_to_s(pos[1], money=True)
            quantity = n_to_s(pos[2])
            position_performance += (
                f"{pad(ticker)}"
                f"{pad(price)}"
                f"{pad(quantity)}"
                f"{pretty_n_to_s(position_pnls[i], money=True)}"
                f" {pretty_n_to_s(position_percentile_pnls[i], percentage=True)}\n"
            )
            i += 1

        portfolio_performance = (
            f"{pretty_n_to_s(portfolio_value, money=True, yellow=True)}"
            f" {pretty_n_to_s(portfolio_pnl, money=True)}"
            f" {pretty_n_to_s(portfolio_percentile_pnl, percentage=True)}"
        )
        
        print(f"{portfolio_performance}\n\n{position_performance}")

class Stock(Robinhood):
    def __init__(self, acct_file_path, ticker):
        super().__init__(acct_file_path)

if __name__ == "__main__":
    portfolio = Portfolio("res/robinhood-login.json")
    portfolio.performance()