class Credentials():
    """ 
    Stores Key / Secret Pairs
    """
    def __init__(self,exchange,key,secret):
        self.key = key
        self.secret = secret
        self.exchange = exchange

    def add_credentials(self,exchange,key,secret):
        self.exchange = exchange
        self.key = key
        self.secret = secret

    def get_both(self):
        return self.key, self.secret

    def get_key(self):
        return self.key

    def get_secret(self):
        return self.secret