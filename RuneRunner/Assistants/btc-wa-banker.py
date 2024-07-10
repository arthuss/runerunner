import requests

class WalletBanker:
    def __init__(self):
        self.rpc_user = "yourrpcuser"
        self.rpc_password = "yourrpcpassword"
        self.rpc_url = "http://localhost:8332"

    def check_funds(self):
        response = requests.post(self.rpc_url, json={"jsonrpc": "1.0", "id":"curltest", "method": "getbalance"}, auth=(self.rpc_user, self.rpc_password))
        return response.json().get('result', 0)

    def buy_rune(self, rune_id, amount):
        # Implementiere den Kaufvorgang hier
        pass
