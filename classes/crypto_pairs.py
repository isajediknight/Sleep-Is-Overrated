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

    # Do not support XHV, RYO
    # binance
    # bittrex
    # kraken

    # Do Not support ETC
    # tradeogre

    def get_corrected_pair_for_exchange(self):
        if self.exchange == 'tradeogre':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'BTC-DOGE'
            elif self.main == 'BTC' and self.alt == 'RYO':
                return 'BTC-RYO'
            elif self.main == 'BTC' and self.alt == 'XMR':
                return 'BTC-XMR'
            elif self.main == 'BTC' and self.alt == 'ETH':
                return 'BTC-ETH'
            elif self.main == 'BTC' and self.alt == 'LTC':
                return 'BTC-LTC'
            elif self.main == 'BTC' and self.alt == 'XHV':
                return 'BTC-XHV'
            elif self.main == 'BTC' and self.alt == 'DASH':
                return 'BTC-DASH'
            elif self.main == 'BTC' and self.alt == 'RVN':
                return 'BTC-RVN'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)
        else:
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            elif self.main == 'BTC' and self.alt == 'XMR':
                return 'XMR/BTC'
            elif self.main == 'BTC' and self.alt == 'ETH':
                return 'ETH/BTC'
            elif self.main == 'BTC' and self.alt == 'LTC':
                return 'LTC/BTC'
            elif self.main == 'BTC' and self.alt == 'ETC':
                return 'ETC/BTC'
            elif self.main == 'BTC' and self.alt == 'DASH':
                return 'DASH/BTC'
            elif self.main == 'BTC' and self.alt == 'RVN':
                return 'RVN/BTC'
            #elif self.main == 'BTC' and self.alt == 'XHV':
            #    return 'XHV/BTC'
            else:
                raise Exception(" No pair defined for " + self.exchange + " with " + self.main + " and " + self.alt)

    def get_corrected_pair(self,exchange='tradeogre'):
        """
        I realized that sending in the exchange was needed for threading than using a class variable
        """
        if exchange == 'tradeogre':
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'BTC-DOGE'
            elif self.main == 'BTC' and self.alt == 'RYO':
                return 'BTC-RYO'
            elif self.main == 'BTC' and self.alt == 'XMR':
                return 'BTC-XMR'
            elif self.main == 'BTC' and self.alt == 'ETH':
                return 'BTC-ETH'
            elif self.main == 'BTC' and self.alt == 'LTC':
                return 'BTC-LTC'
            elif self.main == 'BTC' and self.alt == 'XHV':
                return 'BTC-XHV'
            elif self.main == 'BTC' and self.alt == 'DASH':
                return 'BTC-DASH'
            elif self.main == 'BTC' and self.alt == 'RVN':
                return 'BTC-RVN'
            else:
                raise Exception(" No pair defined for " + exchange + " with " + self.main + " and " + self.alt)
        else:
            if self.main == 'BTC' and self.alt == 'DOGE':
                return 'DOGE/BTC'
            elif self.main == 'BTC' and self.alt == 'XMR':
                return 'XMR/BTC'
            elif self.main == 'BTC' and self.alt == 'ETH':
                return 'ETH/BTC'
            elif self.main == 'BTC' and self.alt == 'LTC':
                return 'LTC/BTC'
            elif self.main == 'BTC' and self.alt == 'ETC':
                return 'ETC/BTC'
            elif self.main == 'BTC' and self.alt == 'DASH':
                return 'DASH/BTC'
            elif self.main == 'BTC' and self.alt == 'RVN':
                return 'RVN/BTC'

    def supported_exchange(self,exchange):
        return exchange.lower() in ['tradeogre','binance','kraken','bittrex','poloniex']

    def supported_crypto_main(self,main):
        return main.upper() in ['BTC']

    def supported_crypto_alt(self,alt):
        return alt.upper() in ['DOGE']