import requests
from wallet_bank import WalletBanker
from price_prediction import PricePredictionAssistant
from data_scraper import DataScraper
from safeguard import Safeguard

class TradingManager:
    def __init__(self):
        self.wallet_banker = WalletBanker()
        self.price_predictor = PricePredictionAssistant()
        self.scraper = DataScraper()
        self.safeguard = Safeguard()

    def check_and_trade(self, rune_id, rune_name):
        if self.safeguard.check_for_errors():
            print("Errors detected, aborting trade.")
            return

        available_funds = self.wallet_banker.check_funds()
        if available_funds <= 0:
            print("No funds available.")
            return

        market_data = self.scraper.get_market_data(rune_name)
        price_prediction = self.price_predictor.predict(market_data)

        if price_prediction['buy_signal']:
            amount_to_buy = price_prediction['recommended_amount']
            self.wallet_banker.buy_rune(rune_id, amount_to_buy)

if __name__ == "__main__":
    manager = TradingManager()
    manager.check_and_trade("3", "dog.go.to.the.moon")
