class CryptoPairs:
    def __init__(self,exchange='tradeogre', main='BTC', alt='DOGE'):
        main = main.upper()
        alt = alt.upper()
        exchange = exchange.lower()

        self.main = main
        self.alt = alt
        self.exchange = exchange

    def set_exchange(self,exchange):
        self.exchange = exchange

    def set_main(self,main):
        self.main = main

    def set_alt(self,alt):
        self.alt = alt

    def get_corrected_pair_for_exchange(self):
        if self.exchange == 'tradeogre':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'BTC-DOGE'
            elif self.main == 'BTC' and self.alt == 'RYO':
                return 'BTC-RYO'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)
        elif self.exchange == 'binance':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)
        elif self.exchange == 'kraken':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)
        elif self.exchange == 'bittrex':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)
        else:
            raise Exception(" Exchange " + self.exchange + " is not currently supported")

    def get_corrected_pair(self,exchange='tradeogre'):
        """
        I realized that sending in the exchange was needed for threading than using a class variable
        """
        if exchange == 'tradeogre':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'BTC-DOGE'
            elif self.main == 'BTC' and self.alt == 'RYO':
                return 'BTC-RYO'
            else:
                raise Exception(" No pair defined for " + exchange + " with " + self.main + " and " + self.alt)
        elif exchange == 'binance':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + exchange + " with " + self.main + " and " + self.alt)
        elif exchange == 'kraken':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + exchange + " with " + self.main + " and " + self.alt)
        elif exchange == 'bittrex':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            else:
                raise Exception(" No pair defined for " + exchange + " with " + self.main + " and " + self.alt)
        else:
            raise Exception(" Exchange " + exchange + " is not currently supported")

    def supported_exchange(self,exchange):
        return exchange.lower() in ['tradeogre','binance','kraken','bittrex']

    def supported_crypto_main(self,main):
        return main.upper() in ['BTC']

    def supported_crypto_alt(self,alt):
        return alt.upper() in ['DOGE']