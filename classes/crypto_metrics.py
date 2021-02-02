import datetime,time,os,sys,requests,json

if (sys.platform.lower().startswith('linux')):
    OS_TYPE = 'linux'
elif (sys.platform.lower().startswith('mac')):
    OS_TYPE = 'macintosh'
elif (sys.platform.lower().startswith('win')):
    OS_TYPE = 'windows'
else:
    OS_TYPE = 'invalid'

# Get our current directory
OUTPUT_FILE_DIRECTORY = os.getcwd()

def find_all(a_str, sub):
    """
    Returns the indexes of {sub} where they were found in {a_str}.  The values
    returned from this function should be made into a list() before they can
    be easily used.
    Last Update: 03/01/2017
    By: LB023593
    """

    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

# Create variables for all the paths
if ((OS_TYPE == 'windows')):
    # Clear Screen Windows
    directories = list(find_all(OUTPUT_FILE_DIRECTORY, '\\'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\outputs\\'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\inputs\\'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\scripts\\'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\github\\'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\classes\\'
elif ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    # Clear Screen Linux / Mac
    directories = list(find_all(OUTPUT_FILE_DIRECTORY, '/'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/outputs/'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/inputs/'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/scripts/'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/github/'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/classes/'

# OS Compatibility for importing Class Files
if ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    sys.path.insert(0, '../classes/')
    sys.path.insert(0, MODULES_DIR)
elif ((OS_TYPE == 'windows')):
    sys.path.insert(0, '..\\classes\\')
    sys.path.insert(0, MODULES_DIR)

# < --- Begin Custom Classes Import --- >
# Custom Colors for printing to the screen
from custom_colors import *

from benchmark import *

from access import *

from crypto_pairs import *

from command_line_arguments import *
# < ---  End  Custom Classes Import --- >

# < --- Begin Module Classes Import --- >
from tradeogre import *

import ccxt
from ccxt import binance
# < ---  End  Model Classes Import  --- >

class Metrics:
    def __init__(self,main='BTC',alt='DOGE'):

        # Read in exchanges and API keys
        self.exchange_keys = {}
        readfile = open(INPUTS_DIR + 'untitled.pyc', 'r')
        for line in readfile:
            temp_exchange, temp_key, temp_secret = list(line.strip().split(','))
            self.exchange_keys[temp_exchange] = Credentials(temp_exchange, temp_key, temp_secret)
            # print(temp_exchange + "\t" + temp_key + "\t" + temp_secret)
        readfile.close()

        self.crypto_main = main
        self.crypto_alt = alt

        self.crypto_pair = CryptoPairs('tradeogre', main, alt)

    def call_order_book(self,exchange='tradeogre'):

        if(exchange in list(self.exchange_keys.keys())):
            if exchange == 'tradeogre':
                self.crypto_pair.set_exchange('tradeogre')
                api_tradeogre = TradeOgre(self.exchange_keys['tradeogre'].get_key(), self.exchange_keys['tradeogre'].get_secret())
                tradeogre_json_result = api_tradeogre.order_book(self.crypto_pair.get_corrected_pair_for_exchange())
                #tradeogre_buy = tradeogre_json_result['buy']
                #tradeogre_sell = tradeogre_json_result['sell']
                return tradeogre_json_result['buy'],tradeogre_json_result['sell']
            elif exchange == 'binance':
                exchange_id = exchange
                self.crypto_pair.set_exchange(exchange_id)
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({
                    'apiKey': exchange_keys[exchange_id].get_key(),
                    'secret': exchange_keys[exchange_id].get_secret(),
                    'timeout': 30000,
                    'enableRateLimit': True,
                })
                exchange.verbose = False
                # dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
                binance_dict_result = exchange.fetch_order_book(crypto_pair.get_corrected_pair_for_exchange())  # 'BTC/USDT')
                #binance_buy = binance_dict_result['bids']
                #binance_sell = binance_dict_result['asks']
                return binance_dict_result['bids'], binance_dict_result['asks']
            elif exhange == 'bittrex':
                exchange_id = exhange
                crypto_pair.set_exchange(exchange_id)
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({
                    #    'apiKey': exchange_keys[exchange_id].get_key(),
                    #    'secret': exchange_keys[exchange_id].get_secret(),
                    'timeout': 30000,
                    'enableRateLimit': True,
                })
                exchange.verbose = False
                # dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
                bittrex_dict_result = exchange.fetch_order_book(
                    crypto_pair.get_corrected_pair_for_exchange())  # 'BTC/USDT')
                # print(list(depth.keys()))
                #bittrex_buy = bittrex_dict_result['bids']
                #bittrex_sell = bittrex_dict_result['asks']
                return bittrex_dict_result['bids'], bittrex_dict_result['asks']
            elif exchange == 'kraken':
                exchange_id = 'kraken'
                crypto_pair.set_exchange(exchange_id)
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({
                    #    'apiKey': exchange_keys[exchange_id].get_key(),
                    #    'secret': exchange_keys[exchange_id].get_secret(),
                    'timeout': 30000,
                    'enableRateLimit': True,
                })
                exchange.verbose = False
                # dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
                kraken_dict_result = exchange.fetch_order_book(
                    crypto_pair.get_corrected_pair_for_exchange())  # 'BTC/USDT')
                # print(list(depth.keys()))
                #kraken_buy = kraken_dict_result['bids']
                #kraken_sell = kraken_dict_result['asks']
                return kraken_dict_result['bids'],kraken_dict_result['asks']
            else:
                print("Exchange " + exhcange + " has not been properly added to ../classes/crypto_metrics.py")
        else:
            raise Exception(" Exchange " + exchange + " information is not present in the keys file: " + INPUTS_DIR + 'untitled.pyc')


