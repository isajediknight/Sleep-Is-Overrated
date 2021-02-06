class Tracking:
    def __init__(self,main='BTC',alt='DOGE'):
        self.main = main
        self.alt = alt

        self.ticker = {}

    def add_ticker_results(self,timestamp,exchange,bid,ask,bid_volume,ask_volume):
        """
        Save the results
        """


        #if exchange == 'tradeogre':
        #    this_ticker[exchange] = Ticker(timestamp, exchange, bid, ask, bid_volume, ask_volume)
        #    self.ticker[timestamp] = this_ticker[exchange]
        #else:
        this_ticker = {}
        this_ticker[exchange] = Ticker(timestamp,exchange,bid,ask,bid_volume,ask_volume)
        if timestamp not in list(self.ticker.keys()):
            self.ticker[timestamp] = {}

        self.ticker[timestamp][exchange] = this_ticker[exchange]
        #self.ticker[timestamp][exchange] = Ticker(timestamp,exchange,bid,ask,bid_volume,ask_volume)

    def get_keys(self):
        return list(self.ticker.keys())

    def get_ticker(self):
        return self.ticker

class Ticker:
    def __init__(self,timestamp,exchange,bid,ask,bid_volume,ask_volume):
        """
        Initialize
        """
        self.timestamp = timestamp
        self.exchange = exchange
        self.bid = bid
        self.ask = ask
        self.bid_volume = bid_volume
        self.ask_volume = ask_volume

    def get_timestamp(self):
        return self.timestamp

    def get_exchange(self):
        return self.exchange

    def get_bid(self):
        return self.bid

    def get_ask(self):
        return self.ask

    def get_bid_volume(self):
        return self.bid_volume

    def get_ask_volume(self):
        return self.ask_volume

