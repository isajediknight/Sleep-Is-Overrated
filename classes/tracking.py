from custom_colors import *
from pretty_formatting import *

class Tracking:
    def __init__(self,main='BTC',alt='DOGE',colored_keys=['exchange','attention'],colored_colors=['38;5;214m','38;5;226m']):
        # main crypto
        self.main = main
        # shitcoin
        self.alt = alt

        # Our dictionary of results
        self.object = {}

        # Text Coloration
        self.cc = ColoredText(colored_keys, colored_colors)

        # List of exchanges from the previous order book
        self.previous_order_book_exchanges = []

        # List of previous sell wall
        self.previous_sell_wall = {}

        # List of previous buy wall
        self.previous_buy_wall = {}

        self.buy_prices = {}
        self.sell_prices = {}

        self.track_buy_prices = Price()
        self.track_sell_prices = Price()

    def add_ticker_results(self,timestamp,exchange,bid,ask,bid_volume,ask_volume):
        """
        Save the results
        """
        #if exchange == 'tradeogre':
        #    this_ticker[exchange] = Ticker(timestamp, exchange, bid, ask, bid_volume, ask_volume)
        #    self.object[timestamp] = this_ticker[exchange]
        #else:
        this_ticker = {}
        this_ticker[exchange] = Ticker(timestamp,exchange,bid,ask,bid_volume,ask_volume)
        if timestamp not in list(self.object.keys()):
            self.object[timestamp] = {}

        self.object[timestamp][exchange] = this_ticker[exchange]
        #self.object[timestamp][exchange] = Ticker(timestamp,exchange,bid,ask,bid_volume,ask_volume)

    def add_order_book_results(self,timestamp,exchange,buying,selling):
        this_order_book = {}
        this_order_book[exchange] = OrderBook(timestamp,exchange,buying,selling)
        if timestamp not in list(self.object.keys()):
            self.object[timestamp] = {}

        self.object[timestamp][exchange] = this_order_book[exchange]

    def compare_previous_order_book(self):

        timestamps = sorted(list(self.object.keys()))

        if len(timestamps) < 2:
            raise Exception("Only one data point exists please add another data point")

        # Current Timestamp of Data
        current_timestamp = timestamps[-1]
        # Previous Timestamp of Data
        previous_timestamp = timestamps[-2]
        # If an API call fails we won't have the same number of exchanges in both Timestamps - this will make us only compare where we have data for both exchanges
        exchange_intersection = sorted(list(set(list(self.object[current_timestamp].keys())).intersection(set(list(self.object[previous_timestamp].keys())))))

        # Current buy data points
        current_buy_prices = []
        current_buy_amounts = []
        current_buy_exchanges = []
        # Current sell data points
        current_sell_prices = []
        current_sell_amounts = []
        current_sell_exchanges = []

        # Pull data out to be sorted
        unsorted_buy_data_point = []
        unsorted_sell_data_point = []
        for exchange in exchange_intersection:
            buy_price = self.object[current_timestamp][exchange].get_cheapest_buy()[1]
            buy_amount = self.object[current_timestamp][exchange].get_cheapest_buy()[0]
            sell_price = self.object[current_timestamp][exchange].get_costliest_sell()[1]
            sell_amount = self.object[current_timestamp][exchange].get_costliest_sell()[0]
            unsorted_buy_data_point.append(buy_price + "|" + str(buy_amount) + "|" + exchange)
            unsorted_sell_data_point.append(sell_price + "|" + str(sell_amount) + "|" + exchange)

        # sort the data and record it
        for data in reversed(sorted(unsorted_buy_data_point)):
            price, amount, exchange = data.split("|")
            current_buy_prices.append(price)
            current_buy_amounts.append(amount)
            current_buy_exchanges.append(exchange)

        # sort the data and record it
        for data in sorted(unsorted_sell_data_point):
            price, amount, exchange = data.split("|")
            current_sell_prices.append(price)
            current_sell_amounts.append(amount)
            current_sell_exchanges.append(exchange)

        # previous buy data points
        previous_buy_prices = []
        previous_buy_amounts = []
        previous_buy_exchanges = []
        # previous sell data points
        previous_sell_prices = []
        previous_sell_amounts = []
        previous_sell_exchanges = []

        # Pull data out to be sorted
        unsorted_buy_data_point = []
        unsorted_sell_data_point = []
        for exchange in exchange_intersection:
            buy_price = self.object[previous_timestamp][exchange].get_cheapest_buy()[1]
            buy_amount = self.object[previous_timestamp][exchange].get_cheapest_buy()[0]
            sell_price = self.object[previous_timestamp][exchange].get_costliest_sell()[1]
            sell_amount = self.object[previous_timestamp][exchange].get_costliest_sell()[0]
            unsorted_buy_data_point.append(buy_price + "|" + str(buy_amount) + "|" + exchange)
            unsorted_sell_data_point.append(sell_price + "|" + str(sell_amount) + "|" + exchange)

        # sort the data and record it
        for data in reversed(sorted(unsorted_buy_data_point)):
            price, amount, exchange = data.split("|")
            previous_buy_prices.append(price)
            previous_buy_amounts.append(amount)
            previous_buy_exchanges.append(exchange)

        # sort the data and record it
        for data in sorted(unsorted_sell_data_point):
            price, amount, exchange = data.split("|")
            previous_sell_prices.append(price)
            previous_sell_amounts.append(amount)
            previous_sell_exchanges.append(exchange)

        #print(str(current_buy_amounts[-1]))
        dot_loc = str(current_buy_amounts[-1]).find('.')
        pf = PrettyFormatting(9)#dot_loc)
        btc_price = PrettyFormatting(2)

        print("\n   Buying:")
        for i in range(len(current_buy_prices)):
            message = ""
            tab = "\t"
            if current_buy_exchanges[i] == 'kraken':
                tab += "\t"

            message += " " + pf.add_spaces(current_buy_exchanges[i]) + self.cc.cc(current_buy_exchanges[i],'exchange')
            message += pf.middle_zero(current_buy_amounts[i])
            message += btc_price.middle_zero(current_buy_prices[i])
            diff, color = pf.diff_two(self.object[previous_timestamp][current_buy_exchanges[i]].get_cheapest_buy()[1],current_buy_prices[i])
            message += " " + self.cc.cc(diff,color)

            print(message)

        print("\n  Selling:")
        for i in reversed(range(len(current_sell_prices))):
            message = ""
            tab = "\t"
            if current_sell_exchanges[i] == 'kraken':
                tab += "\t"

            message += " " + pf.add_spaces(current_sell_exchanges[i]) + self.cc.cc(current_sell_exchanges[i], 'exchange')
            message += pf.middle_zero(current_sell_amounts[i])
            message += btc_price.middle_zero(current_sell_prices[i])
            diff, color = pf.diff_two(self.object[previous_timestamp][current_sell_exchanges[i]].get_costliest_sell()[1], current_sell_prices[i])
            message += " " + self.cc.cc(diff, color)

            print(message)

        buy_prices = []
        buy_amounts = []
        buy_wall = {}
        print("\n Buy Walls:")
        for exchange in exchange_intersection:
            for i in range(7,0,-1):
                if exchange == 'tradeogre':
                    price = str(self.object[current_timestamp][exchange].buying[i][0])
                else:
                    price = str(format(self.object[current_timestamp][exchange].buying[i][0], '.8f'))

                if price in buy_prices:
                    index = buy_prices.index(price)
                    buy_amounts[index] += float(self.object[current_timestamp][exchange].buying[i][1])
                else:
                    buy_prices.append(price)
                    buy_amounts.append(float(self.object[current_timestamp][exchange].buying[i][1]))

                amount = float(self.object[current_timestamp][exchange].buying[i][1])

                if price in list(buy_wall.keys()):
                    buy_wall[price] = buy_wall[price] + amount
                else:
                    buy_wall[price] = amount
            ##      Amount       Price
            # self.selling[0][1], format(self.selling[0][0], '.8f')
        #for i in range(len(buy_prices)):
        #    print(" " + buy_prices[i] + pf.middle_zero(str(buy_amounts[i])))

        for price in reversed(sorted(list(buy_wall.keys()))):
            if price in list(self.previous_buy_wall.keys()):
                diff, color = pf.diff_two(str(self.previous_buy_wall[price]),str(buy_wall[price]))
            else:
                diff = "       0"
                color = 'grey'
            # 14815690.07141842
            find_dot = str(buy_wall[price]).find('.')
            if len(str(buy_wall[price])[find_dot:]) > 9:
                temp_wall = str(buy_wall[price])[:find_dot] + '.' + str(buy_wall[price])[find_dot + 1:find_dot + 9]
            else:
                temp_wall = str(buy_wall[price])

            message = "\t  " + pf.middle_zero(temp_wall)
            message += " " + price
            message += " " +self.cc.cc(str(diff), color)

            print(message)

        self.previous_buy_wall = buy_wall

        sell_prices = []
        sell_amounts = []
        sell_wall = {}
        print("\n Sell Walls:")
        for exchange in exchange_intersection:
            for i in range(0, 7):
                if exchange == 'tradeogre':
                    price = str(self.object[current_timestamp][exchange].selling[i][0])
                else:
                    price = str(format(self.object[current_timestamp][exchange].selling[i][0], '.8f'))

                if price in sell_prices:
                    index = sell_prices.index(price)
                    sell_amounts[index] += float(self.object[current_timestamp][exchange].selling[i][1])
                else:
                    sell_prices.append(price)
                    sell_amounts.append(float(self.object[current_timestamp][exchange].selling[i][1]))

                amount = float(self.object[current_timestamp][exchange].selling[i][1])

                if price in list(sell_wall.keys()):
                    sell_wall[price] = sell_wall[price] + amount
                else:
                    sell_wall[price] = amount
            ##      Amount       Price
            # self.selling[0][1], format(self.selling[0][0], '.8f')
        #for i in range(len(sell_prices)):
        #    print(" " + sell_prices[i] + pf.middle_zero(str(sell_amounts[i])))

        for price in reversed(sorted(list(sell_wall.keys()))):
            if price in list(self.previous_sell_wall.keys()):
                diff, color = pf.diff_two(str(self.previous_sell_wall[price]),str(sell_wall[price]))
            else:
                diff = "       0"
                color = 'grey'
            #14815690.07141842
            find_dot = str(sell_wall[price]).find('.')
            if len(str(sell_wall[price])[find_dot:]) > 9:
                temp_wall = str(sell_wall[price])[:find_dot] + '.' + str(sell_wall[price])[find_dot+1:find_dot+9]
            else:
                temp_wall = str(sell_wall[price])

            message = "\t  " + pf.middle_zero(temp_wall)
            message += " " + price
            message += " " +self.cc.cc(str(diff), color)

            print(message)
        self.previous_sell_wall = sell_wall

        # Catch when an API call fails
        exchange_difference = list(set(self.previous_order_book_exchanges).difference(set(exchange_intersection)))
        if len(exchange_difference) < len(self.previous_order_book_exchanges) and len(exchange_difference) != 0:
            print("")
            for exchange in exchange_difference:
                print(" " + self.cc.cc(exchange,'exchange') + " API could not be reached and was excluded")

        self.previous_order_book_exchanges = exchange_intersection

    def momentum(self):

        exchange_aliases = {'tradeogre':'TO','binance':'BN','bittrex':'BT','poloniex':'PO','kraken':'KR'}

        timestamps = sorted(list(self.object.keys()))
        # RVN
        pf_no_exchange = PrettyFormatting(44)
        pf_exchange = PrettyFormatting(44)
        pf = PrettyFormatting(36)
        # DOGE
        #pf_no_exchange = PrettyFormatting(50)
        #pf_exchange = PrettyFormatting(50)
        #pf = PrettyFormatting(30)

        if len(timestamps) < 2:
            raise Exception("Only one data point exists please add another data point")

        # Current Timestamp of Data
        current_timestamp = timestamps[-1]
        # Previous Timestamp of Data
        previous_timestamp = timestamps[-2]
        # If an API call fails we won't have the same number of exchanges in both Timestamps - this will make us only compare where we have data for both exchanges
        exchange_intersection = sorted(list(set(list(self.object[current_timestamp].keys())).intersection(set(list(self.object[previous_timestamp].keys())))))

        # Current buy data points
        current_buy_prices = []
        current_buy_amounts = []
        current_buy_exchanges = []
        # Current sell data points
        current_sell_prices = []
        current_sell_amounts = []
        current_sell_exchanges = []

        buy_price_timestamp = {}
        sell_price_timestamp = {}

        # Pull data out to be sorted
        unsorted_buy_data_point = []
        unsorted_sell_data_point = []
        for exchange in exchange_intersection:
            buy_price = self.object[current_timestamp][exchange].get_cheapest_buy()[1]
            buy_amount = self.object[current_timestamp][exchange].get_cheapest_buy()[0]
            sell_price = self.object[current_timestamp][exchange].get_costliest_sell()[1]
            sell_amount = self.object[current_timestamp][exchange].get_costliest_sell()[0]
            unsorted_buy_data_point.append(buy_price + "|" + str(buy_amount) + "|" + exchange)
            unsorted_sell_data_point.append(sell_price + "|" + str(sell_amount) + "|" + exchange)

        # sort the data and record it
        for data in reversed(sorted(unsorted_buy_data_point)):
            price, amount, exchange = data.split("|")
            current_buy_prices.append(price)
            current_buy_amounts.append(amount)
            current_buy_exchanges.append(exchange)

            if current_timestamp not in list(self.buy_prices.keys()):
                self.buy_prices[current_timestamp] = {}
            self.buy_prices[current_timestamp][exchange] = price
            self.track_buy_prices.add_price(exchange,current_timestamp,price)

        # sort the data and record it
        for data in sorted(unsorted_sell_data_point):
            price, amount, exchange = data.split("|")
            current_sell_prices.append(price)
            current_sell_amounts.append(amount)
            current_sell_exchanges.append(exchange)

            if current_timestamp not in list(self.sell_prices.keys()):
                self.sell_prices[current_timestamp] = {}
            self.sell_prices[current_timestamp][exchange] = price
            self.track_sell_prices.add_price(exchange, current_timestamp, price)

        # previous buy data points
        previous_buy_prices = []
        previous_buy_amounts = []
        previous_buy_exchanges = []
        # previous sell data points
        previous_sell_prices = []
        previous_sell_amounts = []
        previous_sell_exchanges = []

        # Pull data out to be sorted
        unsorted_buy_data_point = []
        unsorted_sell_data_point = []
        for exchange in exchange_intersection:
            buy_price = self.object[previous_timestamp][exchange].get_cheapest_buy()[1]
            buy_amount = self.object[previous_timestamp][exchange].get_cheapest_buy()[0]
            sell_price = self.object[previous_timestamp][exchange].get_costliest_sell()[1]
            sell_amount = self.object[previous_timestamp][exchange].get_costliest_sell()[0]
            unsorted_buy_data_point.append(buy_price + "|" + str(buy_amount) + "|" + exchange)
            unsorted_sell_data_point.append(sell_price + "|" + str(sell_amount) + "|" + exchange)

            if previous_timestamp not in list(self.buy_prices.keys()):
                self.buy_prices[previous_timestamp] = {}
            self.buy_prices[previous_timestamp][exchange] = price

        # sort the data and record it
        for data in reversed(sorted(unsorted_buy_data_point)):
            price, amount, exchange = data.split("|")
            previous_buy_prices.append(price)
            previous_buy_amounts.append(amount)
            previous_buy_exchanges.append(exchange)

        # sort the data and record it
        for data in sorted(unsorted_sell_data_point):
            price, amount, exchange = data.split("|")
            previous_sell_prices.append(price)
            previous_sell_amounts.append(amount)
            previous_sell_exchanges.append(exchange)

        # print(str(current_buy_amounts[-1]))
        dot_loc = str(current_buy_amounts[-1]).find('.')
        pf = PrettyFormatting(9)  # dot_loc)
        btc_price = PrettyFormatting(2)

        sell_prices = []
        sell_amounts = []
        sell_wall = {}
        for exchange in exchange_intersection:
            for i in range(len(self.object[current_timestamp][exchange].selling)):
                if exchange == 'tradeogre':
                    price = str(self.object[current_timestamp][exchange].selling[i][0])
                else:
                    price = str(format(self.object[current_timestamp][exchange].selling[i][0], '.8f'))

                if price in sell_prices:
                    index = sell_prices.index(price)
                    sell_amounts[index] += float(self.object[current_timestamp][exchange].selling[i][1])
                else:
                    sell_prices.append(price)
                    sell_amounts.append(float(self.object[current_timestamp][exchange].selling[i][1]))

                amount = float(self.object[current_timestamp][exchange].selling[i][1])

                if price in list(sell_wall.keys()):
                    sell_wall[price] = sell_wall[price] + amount
                else:
                    sell_wall[price] = amount

        buy_prices = []
        buy_amounts = []
        buy_wall = {}
        for exchange in exchange_intersection:
            for i in range(len(self.object[current_timestamp][exchange].buying)):
                if exchange == 'tradeogre':
                    price = str(self.object[current_timestamp][exchange].buying[i][0])
                else:
                    price = str(format(self.object[current_timestamp][exchange].buying[i][0], '.8f'))

                if price in buy_prices:
                    index = buy_prices.index(price)
                    buy_amounts[index] += float(self.object[current_timestamp][exchange].buying[i][1])
                else:
                    buy_prices.append(price)
                    buy_amounts.append(float(self.object[current_timestamp][exchange].buying[i][1]))

                amount = float(self.object[current_timestamp][exchange].buying[i][1])

                if price in list(buy_wall.keys()):
                    buy_wall[price] = buy_wall[price] + amount
                else:
                    buy_wall[price] = amount

        #self.object[previous_timestamp][exchange].get_cheapest_buy()[1]
        #self.object[previous_timestamp][exchange].get_costliest_sell()[1]


        prices_list = list(set(buy_wall.keys()).union(set(sell_wall.keys())))

        largest_price = sorted(current_buy_prices)[0]
        smallest_price = sorted(current_sell_prices)[-1]
        build_key_list = []
        for price in prices_list:
            # Should this stay hard coded?
            if(float(smallest_price) - 0.00000020 <= float(price) and float(largest_price) + 0.00000020 >= float(price)):
                build_key_list.append(price)

        #data_timestamps = []
        #for timestamp in sorted(list(self.buy_prices.keys()))[-5:-1]:
        #    data_timestamps.append(timestamps)

#        buys = {}
#        buys_price_key = {}
#        sells = {}
#        sells_price_key = {}
#        for price in reversed(sorted(build_key_list)):
#            for exchange in exchange_intersection:
#                for timestamp in sorted(list(self.buy_prices.keys()))[-5:-1]:
#
#                    if timestamp not in buys.keys():
#                        buys[timestamp] = {}
#
#                    if self.buy_prices[timestamp][exchange] not in list(self.buy_prices[timestamp].keys()):
#                        buys_price_key[self.buy_prices[timestamp]][exchange] = {}
#
#                    buys[timestamp][exchange] = self.buy_prices[timestamp]
#                    buys_price_key[self.buy_prices[timestamp]][exchange] = timestamp
#
#                for timestamp in sorted(list(self.sell_prices.keys()))[-5:-1]:
#
#                    if timestamp not in sells.keys():
#                        sells[timestamp] = {}
#
#                    # self.sell_prices[timestamp]
#                    if self.sell_prices[timestamp][exchange] not in list(self.sell_prices[timestamp].keys()):
#                        sells_price_key[self.sell_prices[timestamp]][exchange] = {}
#
#                    sells[timestamp][exchange] = self.sell_prices[timestamp]
#                    sells_price_key[self.sell_prices[timestamp]][exchange] = timestamp
#
#                    #previous_timestamp_index = data_timestamp.index(timestamp)
#
#                    #if previous_timestamp_index != -1:
#                    #    if buys[data_timestamp[previous_timestamp_index]][exchange] == buy_prices[]

        for price in reversed(sorted(build_key_list)):
            message = ""
            for exchange in exchange_intersection:
                i = current_buy_exchanges.index(exchange)

                previous_buy_boolean = False
                for timestamp in sorted(list(self.buy_prices.keys()))[-5:-1]:
                    if self.buy_prices[timestamp][exchange] == price:
                        previous_buy_boolean = True
                        this_buy_timestamp = timestamp
                        break

                if current_buy_prices[i] == price:
                    message += " " + self.cc.cc(exchange_aliases[current_buy_exchanges[i]],self.track_buy_prices.get_price_color(exchange,price))
                elif self.track_buy_prices.check_price(exchange,price):
                    message += " " + self.cc.cc(exchange_aliases[current_buy_exchanges[i]],self.track_buy_prices.get_price_color(exchange,price))
                else:
                    message += "   "

            message += " " + price

            for exchange in exchange_intersection:
                i = current_sell_exchanges.index(exchange)

                previous_sell_boolean = False
                for timestamp in sorted(list(self.sell_prices.keys()))[-5:-1]:
                    if self.sell_prices[timestamp][exchange] == price:
                        previous_sell_boolean = True
                        break

                if current_sell_prices[i] == price:
                    message += " " + self.cc.cc(exchange_aliases[current_sell_exchanges[i]],
                                                self.track_sell_prices.get_price_color(exchange, price))
                elif self.track_sell_prices.check_price(exchange, price):
                    message += " " + self.cc.cc(exchange_aliases[current_sell_exchanges[i]],
                                                self.track_sell_prices.get_price_color(exchange, price))
                else:
                    message += "   "

            print(message)

    def get_keys(self):
        return list(self.object.keys())

    def get_ticker(self):
        return self.object

    def get_object(self):
        return self.object

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

class OrderBook:
    def __init__(self,timestamp,exchange,selling,buying):
        self.selling = selling
        self.buying = buying
        self.timestamp = timestamp
        self.exchange = exchange

    def get_cheapest_buy(self):

        if self.exchange == 'tradeogre':
            return self.buying[0][1] ,self.buying[0][0]
        else:
            #      Amount             Price
            return self.buying[0][1] ,format(self.buying[0][0],'.8f')

    def get_costliest_sell(self):

        if self.exchange == 'tradeogre':
            return self.selling[0][1], self.selling[0][0]
        else:
            #      Amount              Price
            return self.selling[0][1] ,format(self.selling[0][0],'.8f')

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

    def get_cc_trend_count(self):
        return self.trend_count

    def get_cc_color(self):
        return self.current_color

    def get_cc_direction_total(self):
        return self.direction_total

class Price:
    def __init__(self):#,main,alt):
        #self.exchange = exchange
        #self.main = main
        #self.alt = alt
        self.kraken_timestamps = []
        self.kraken_prices = []

        self.tradeogre_timestamps = []
        self.tradeogre_prices = []

        self.binance_timestamps = []
        self.binance_prices = []

        self.bittrex_timestamps = []
        self.bittrex_prices = []

        self.poloniex_timestamps = []
        self.poloniex_prices = []

    def add_price(self,exchange,timestamp,price):
        if exchange == 'kraken':
            if timestamp not in self.kraken_timestamps:
                if len(self.kraken_prices == 0):
                    self.kraken_timestamps.append(timestamp)
                    self.kraken_prices.append(price)
                elif price in self.kraken_prices:
                    index = self.kraken_prices.index(price)
                    self.kraken_timestamps.pop(index)
                    self.kraken_prices.pop(index)
                    self.kraken_timestamps.append(timestamp)
                    self.kraken_prices.append(price)
                elif price != self.kraken_prices[-1]:
                    self.kraken_timestamps.append(timestamp)
                    self.kraken_prices.append(price)
        elif exchange == 'tradeogre':
            if timestamp not in self.tradeogre_timestamps:
                if len(self.tradeogre_prices) == 0:
                    self.tradeogre_timestamps.append(timestamp)
                    self.tradeogre_prices.append(price)
                elif price in self.tradeogre_prices:
                    index = self.tradeogre_prices.index(price)
                    self.tradeogre_timestamps.pop(index)
                    self.tradeogre_prices.pop(index)
                    self.tradeogre_timestamps.append(timestamp)
                    self.tradeogre_prices.append(price)
                elif price != self.tradeogre_prices[-1]:
                    self.tradeogre_timestamps.append(timestamp)
                    self.tradeogre_prices.append(price)
        if exchange == 'binance':
            if timestamp not in self.binance_timestamps:
                if len(self.binance_prices) == 0:
                    self.binance_timestamps.append(timestamp)
                    self.binance_prices.append(price)
                elif price in self.binance_prices:
                    index = self.binance_prices.index(price)
                    self.binance_timestamps.pop(index)
                    self.binance_prices.pop(index)
                    self.binance_timestamps.append(timestamp)
                    self.binance_prices.append(price)
                elif price != self.binance_prices[-1]:
                    self.binance_timestamps.append(timestamp)
                    self.binance_prices.append(price)
        if exchange == 'bittrex':
            if timestamp not in self.bittrex_timestamps:
                if len(self.bittrex_prices) == 0:
                    self.bittrex_timestamps.append(timestamp)
                    self.bittrex_prices.append(price)
                elif price in self.bittrex_prices:
                    index = self.bittrex_prices.index(price)
                    self.bittrex_timestamps.pop(index)
                    self.bittrex_prices.pop(index)
                    self.bittrex_timestamps.append(timestamp)
                    self.bittrex_prices.append(price)
                elif price != self.bittrex_prices[-1]:
                    self.bittrex_timestamps.append(timestamp)
                    self.bittrex_prices.append(price)
        if exchange == 'poloniex':
            if timestamp not in self.poloniex_timestamps:
                if len(self.poloniex_prices) == 0:
                    self.poloniex_timestamps.append(timestamp)
                    self.poloniex_prices.append(price)
                elif price in self.poloniex_prices:
                    index = self.poloniex_prices.index(price)
                    self.poloniex_timestamps.pop(index)
                    self.poloniex_prices.pop(index)
                    self.poloniex_timestamps.append(timestamp)
                    self.poloniex_prices.append(price)
                elif price != self.poloniex_prices[-1]:
                    self.poloniex_timestamps.append(timestamp)
                    self.poloniex_prices.append(price)

    def get_price_color(self,exchange,price):
        if exchange == 'kraken' and price in self.kraken_prices:
            price_index = self.kraken_prices.index(price)
            current_timestamp = self.kraken_timestamps[price_index]
            if price_index > 0:
                previous_timestamp = self.kraken_timestamps[price_index-1]
                previous_price = self.kraken_prices[price_index-1]
            else:
                previous_timestamp = self.kraken_timestamps[price_index]
                previous_price = self.kraken_prices[price_index]

            if price > previous_price:
                return 'green'
            elif price < previous_price:
                return 'red'
            else:
                return 'white'
        elif exchange == 'tradeogre':
            price_index = self.tradeogre_prices.index(price)
            current_timestamp = self.tradeogre_timestamps[price_index]
            if price_index > 0:
                previous_timestamp = self.tradeogre_timestamps[price_index - 1]
                previous_price = self.tradeogre_prices[price_index - 1]
            else:
                previous_timestamp = self.tradeogre_timestamps[price_index]
                previous_price = self.tradeogre_prices[price_index]

            if price > previous_price:
                return 'green'
            elif price < previous_price:
                return 'red'
            else:
                return 'white'
        elif exchange == 'binance':
            price_index = self.binance_prices.index(price)
            current_timestamp = self.binance_timestamps[price_index]
            if price_index > 0:
                previous_timestamp = self.binance_timestamps[price_index - 1]
                previous_price = self.binance_prices[price_index - 1]
            else:
                previous_timestamp = self.binance_timestamps[price_index]
                previous_price = self.binance_prices[price_index]

            if price > previous_price:
                return 'green'
            elif price < previous_price:
                return 'red'
            else:
                return 'white'
        elif exchange == 'bittrex':
            price_index = self.bittrex_prices.index(price)
            current_timestamp = self.bittrex_timestamps[price_index]
            if price_index > 0:
                previous_timestamp = self.bittrex_timestamps[price_index - 1]
                previous_price = self.bittrex_prices[price_index - 1]
            else:
                previous_timestamp = self.bittrex_timestamps[price_index]
                previous_price = self.bittrex_prices[price_index]

            if price > previous_price:
                return 'green'
            elif price < previous_price:
                return 'red'
            else:
                return 'white'
        if exchange == 'poloniex':
            price_index = self.poloniex_prices.index(price)
            current_timestamp = self.poloniex_timestamps[price_index]
            if price_index > 0:
                previous_timestamp = self.poloniex_timestamps[price_index - 1]
                previous_price = self.poloniex_prices[price_index - 1]
            else:
                previous_timestamp = self.poloniex_timestamps[price_index]
                previous_price = self.poloniex_prices[price_index]

            if price > previous_price:
                return 'green'
            elif price < previous_price:
                return 'red'
            else:
                return 'white'

    def check_timestamp(self,exchange,timestamp):
        if exchange == 'kraken':
            return timestamp in self.kraken_timestamps
        elif exchange == 'tradeogre':
            return timestamp in self.tradeogre_timestamps
        elif exchange == 'binance':
            return timestamp in self.binance_timestamps
        elif exchange == 'bittrex':
            return timestamp in self.bittrex_timestamps
        if exchange == 'poloniex':
            return timestamp in self.poloniex_timestamps

    def get_price_from_timestamp(self,exchange,timestamp):
        """
        Get price for a timestamp
        """
        index = self.timestamps.index(timestamp)
        if index < 0:
            return index
        else:
            return self.prices[index]

        if exchange == 'kraken':
            index = self.kraken_timestamps.index(timestamp)
            return self.kraken_prices[index]
        elif exchange == 'tradeogre':
            index = self.tradeogre_timestamps.index(timestamp)
            return self.tradeogre_prices[index]
        elif exchange == 'binance':
            index = self.binance_timestamps.index(timestamp)
            return self.binance_prices[index]
        elif exchange == 'bittrex':
            index = self.bittrex_timestamps.index(timestamp)
            return self.bittrex_prices[index]
        elif exchange == 'poloniex':
            index = self.poloniex_timestamps.index(timestamp)
            return self.poloniex_prices[index]
        else:
            raise Exception(" Exchange " + exchange + " is not currently supported in tracking.py")

    def check_price(self,exchange,price):
        if exchange == 'kraken':
            return price in self.kraken_prices
        elif exchange == 'tradeogre':
            return price in self.tradeogre_prices
        elif exchange == 'binance':
            return price in self.binance_prices
        elif exchange == 'bittrex':
            return price in self.bittrex_prices
        elif exchange == 'poloniex':
            return price in self.poloniex_prices
        else:
            raise Exception(" Exchange " + exchange + " is not currently supported in tracking.py")
