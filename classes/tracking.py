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

class Trending:
    def __init__(self,up_color='green',down_color='red',no_change='grey'):
        self.up_color = up_color
        self.down_color = down_color
        self.no_change = no_change
        self.trend_count = 0
        self.current_color = no_change
        self.direction_total = 0

    def compute_trend(self,color,change):


        if self.current_color == color and self.up_color == color:
            self.direction_total += change
            self.trend_count += 1
        elif self.current_color == color and self.down_color == color:
            self.direction_total += change
            self.trend_count += 1
        elif self.current_color == color and self.no_change == color:
            self.trend_count += 1

        if self.current_color != color and self.no_change != color:
            self.trend_count = 0
            self.current_color = color
            self.direction_total = change

        #if self.current_color != self.no_change and color == self.no_change:
        #    pass
        #elif self.current_color == color:
        #    self.trend_count += 1
        #else:
        #    self.trend_count = 0
        #    self.current_color = color

    def get_cc_trend_count(self):
        return self.trend_count

    def get_cc_color(self):
        return self.current_color

    def get_cc_direction_total(self):
        return self.direction_total