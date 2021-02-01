import datetime,time,os,sys,requests,json

if(sys.platform.lower().startswith('linux')):
    OS_TYPE = 'linux'
elif(sys.platform.lower().startswith('mac')):
    OS_TYPE = 'macintosh'
elif(sys.platform.lower().startswith('win')):
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
if((OS_TYPE == 'windows')):
    # Clear Screen Windows
    os.system('cls')
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'\\'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\outputs\\'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\inputs\\'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\scripts\\'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\github\\'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\classes\\'
elif((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    # Clear Screen Linux / Mac
    os.system('clear')
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'/'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/outputs/'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/inputs/'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/scripts/'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/github/'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/classes/'

# OS Compatibility for importing Class Files
if((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    sys.path.insert(0,'../classes/')
    sys.path.insert(0,MODULES_DIR)
elif((OS_TYPE == 'windows')):
    sys.path.insert(0,'..\\classes\\')
    sys.path.insert(0,MODULES_DIR)

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

runtime = Benchmark()

# Get parameters from commandline
parameters = Parse()
parameters.add_expectation('-crypto-main', 'string', True, False)
parameters.add_expectation('-crypto-alt', 'string', True, False)
parameters.parse_commandline()
parameters.validate_requirements()

# Read in exchanges and API keys
exchange = {}
readfile = open(INPUTS_DIR + 'untitled.pyc', 'r')
for line in readfile:
    temp_exchange,temp_key,temp_secret = list(line.strip().split(','))
    exchange[temp_exchange] = Credentials(temp_exchange,temp_key,temp_secret)
    #print(temp_exchange + "\t" + temp_key + "\t" + temp_secret)
readfile.close()

# Define Supported Crypto Pairs
crypto_pair = CryptoPairs('tradeogre',parameters.get_parameter('-crypto-main').value,parameters.get_parameter('-crypto-alt').value)
#print(parameters.get_parameter_names())
#crypt_pair = parameters.get_parameter('-crypto-pair').value

api_tradeogre = TradeOgre(exchange['tradeogre'].get_key(),exchange['tradeogre'].get_secret())
#print(str(api_tradeogre.order_book(crypt_pair)))

tradeogre_json_result = api_tradeogre.order_book(crypto_pair.get_corrected_pair_for_exchange())
tradeogre_buy = tradeogre_json_result['buy']
tradeogre_sell = tradeogre_json_result['sell']

tradeogre_buy_total = float(0)
for key in list(tradeogre_buy.keys()):
    tradeogre_buy_total += float(tradeogre_buy[key])

tradeogre_sell_total = float(0)
for key in list(tradeogre_sell.keys()):
    tradeogre_sell_total += float(tradeogre_sell[key])

print("TradeOgre")
print("Buy Total:\t" + str(tradeogre_buy_total))
print("Sell Total:\t" + str(tradeogre_sell_total))

#key = input("Key: ")
#secret = input("Secret: ")
#session = requests.Session()
#session.auth = ('-u',key+':'+secret.strip())#+'@'
#connection_validation = session.get('https://tradeogre.com/api/v1')#'+key+':'+secret+'
#print(str(connection_validation.status_code))
#session.close()



#from ccxt import base
#from ccxt import static_dependencies

#hitbtc   = ccxt.hitbtc({'verbose': True})
#bitmex   = ccxt.bitmex()
#huobipro = ccxt.huobipro()
#exmo     = ccxt.exmo({
#    'apiKey': 'YOUR_PUBLIC_API_KEY',
#    'secret': 'YOUR_SECRET_PRIVATE_KEY',
#})
#kraken = ccxt.kraken({
#    'apiKey': 'YOUR_PUBLIC_API_KEY',
#    'secret': 'YOUR_SECRET_PRIVATE_KEY',
#})

exchange_id = 'binance'
crypto_pair.set_exchange(exchange_id)
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': exchange[exchange_id].get_key(),
    'secret': exchange[exchange_id].get_secret(),
    'timeout': 30000,
    'enableRateLimit': True,
})
exchange.verbose = False
# dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
binance_dict_result = exchange.fetch_order_book(crypto_pair.get_corrected_pair_for_exchange())#'BTC/USDT')
#print(list(depth.keys()))
binance_buy = binance_dict_result['bids']
binance_sell = binance_dict_result['asks']

#print(binance_dict_result['bids'])

binance_buy_total = float(0)
for price,total in binance_buy:
    binance_buy_total += float(total)

binance_sell_total = float(0)
for price,total in binance_sell:
    binance_sell_total += float(total)

print("Binance")
print("Buy Total:\t" + str(binance_buy_total))
print("Sell Total:\t" + str(binance_sell_total))

del exchange
del exchange_class
exchange_id = 'kraken'
crypto_pair.set_exchange(exchange_id)
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
#    'apiKey': exchange[exchange_id].get_key(),
#    'secret': exchange[exchange_id].get_secret(),
    'timeout': 30000,
    'enableRateLimit': True,
})
exchange.verbose = False
# dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
kraken_dict_result = exchange.fetch_order_book(crypto_pair.get_corrected_pair_for_exchange())#'BTC/USDT')
#print(list(depth.keys()))
kraken_buy = kraken_dict_result['bids']
kraken_sell = kraken_dict_result['asks']

kraken_buy_total = float(0)
for price,total,unknown in kraken_buy:
    kraken_buy_total += float(total)

kraken_sell_total = float(0)
for price,total,unknown in kraken_sell:
    kraken_sell_total += float(total)

print("Kraken")
print("Buy Total:\t" + str(kraken_buy_total))
print("Sell Total:\t" + str(kraken_sell_total))

del exchange
del exchange_class
exchange_id = 'bittrex'
crypto_pair.set_exchange(exchange_id)
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
#    'apiKey': exchange[exchange_id].get_key(),
#    'secret': exchange[exchange_id].get_secret(),
    'timeout': 30000,
    'enableRateLimit': True,
})
exchange.verbose = False
# dict keys ['bids', 'asks', 'timestamp', 'datetime', 'nonce']
bittrex_dict_result = exchange.fetch_order_book(crypto_pair.get_corrected_pair_for_exchange())#'BTC/USDT')
#print(list(depth.keys()))
bittrex_buy = bittrex_dict_result['bids']
bittrex_sell = bittrex_dict_result['asks']

#print(kraken_buy)
#sys.exit()

#print(kraken_dict_result['bids'])

bittrex_buy_total = float(0)
for price,total in bittrex_buy:
    bittrex_buy_total += float(total)

bittrex_sell_total = float(0)
for price,total in bittrex_sell:
    bittrex_sell_total += float(total)

print("Bittrex")
print("Buy Total:\t" + str(bittrex_buy_total))
print("Sell Total:\t" + str(bittrex_sell_total))

total_buy = bittrex_buy_total + tradeogre_buy_total + kraken_buy_total + binance_buy_total
total_sell = bittrex_sell_total + tradeogre_sell_total + kraken_sell_total + binance_sell_total

binance_buy_percent = ((binance_buy_total/total_buy) * 100)
tradeogre_buy_percent = ((tradeogre_buy_total/total_buy) * 100)
kraken_buy_percent = ((kraken_buy_total/total_buy) * 100)
bittrex_buy_percent = ((bittrex_buy_total/total_buy) * 100)
print("Buying")
print("Binance: " + str(binance_buy_percent)[:4] + "%\tTradeogre: " + str(tradeogre_buy_percent)[:4] + "%\tKraken: " + str(kraken_buy_percent)[:4] + "%" + "%\tBittrex: " + str(bittrex_buy_percent)[:4] + "%")

binance_sell_percent = ((binance_sell_total/float(total_sell)) * 100)
tradeogre_sell_percent = ((tradeogre_sell_total/float(total_sell)) * 100)
kraken_sell_percent = ((kraken_sell_total/float(total_sell)) * 100)
bittrex_sell_percent = ((bittrex_sell_total/float(total_sell)) * 100)
print("Selling")
print("Binance: " + str(binance_sell_percent)[:4] + "%\tTradeogre: " + str(tradeogre_sell_percent)[:4] + "%\tKraken: " + str(kraken_sell_percent)[:4] + "%\tBittrex: " + str(bittrex_sell_percent)[:4] + "%")

#print("Selling Total:")
#print(str())

runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())