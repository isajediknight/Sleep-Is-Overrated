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

cc = ColoredText()

# Get parameters from commandline
parameters = Parse()
parameters.add_expectation('-crypto-main', 'string', True, False)
parameters.add_expectation('-crypto-alt', 'string', True, False)
parameters.parse_commandline()
parameters.validate_requirements()

# Read in exchanges and API keys
exchange_keys = {}
readfile = open(INPUTS_DIR + 'untitled.pyc', 'r')
for line in readfile:
    temp_exchange,temp_key,temp_secret = list(line.strip().split(','))
    exchange_keys[temp_exchange] = Credentials(temp_exchange,temp_key,temp_secret)
    #print(temp_exchange + "\t" + temp_key + "\t" + temp_secret)
readfile.close()

# Define Supported Crypto Pairs
crypto_pair = CryptoPairs('tradeogre',parameters.get_parameter('-crypto-main').value,parameters.get_parameter('-crypto-alt').value)
#print(parameters.get_parameter_names())
#crypt_pair = parameters.get_parameter('-crypto-pair').value

prev_binance_buy_percent = 0.0
prev_tradeogre_buy_percent = 0.0
prev_kraken_buy_percent = 0.0
prev_bittrex_buy_percent = 0.0
prev_tradeogre_buy_total = 0
prev_tradeogre_sell_total = 0
prev_binance_buy_total = 0
prev_binance_sell_total = 0
prev_kraken_buy_total = 0
prev_kraken_sell_total = 0
prev_bittrex_buy_total = 0
prev_bittrex_sell_total = 0
prev_total_buy = 0
prev_total_sell = 0
prev_binance_buy_percent = 0.0
prev_tradeogre_buy_percent = 0.0
prev_kraken_buy_percent = 0.0
prev_bittrex_buy_percent = 0.0
prev_binance_sell_percent = 0.0
prev_tradeogre_sell_percent = 0.0
prev_kraken_sell_percent = 0.0
prev_bittrex_sell_percent = 0.0


api_tradeogre = TradeOgre(exchange_keys['tradeogre'].get_key(),exchange_keys['tradeogre'].get_secret())
number_of_runs = 0
while(number_of_runs < 100):

    #print(str(api_tradeogre.order_book(crypt_pair)))

    #api_tradeogre = TradeOgre(exchange_keys['tradeogre'].get_key(), exchange_keys['tradeogre'].get_secret())
    crypto_pair.set_exchange('tradeogre')
    tradeogre_json_result = api_tradeogre.order_book(crypto_pair.get_corrected_pair_for_exchange())
    tradeogre_buy = tradeogre_json_result['buy']
    tradeogre_sell = tradeogre_json_result['sell']

    tradeogre_buy_total = float(0)
    for key in list(tradeogre_buy.keys()):
        tradeogre_buy_total += float(tradeogre_buy[key])

    tradeogre_sell_total = float(0)
    for key in list(tradeogre_sell.keys()):
        tradeogre_sell_total += float(tradeogre_sell[key])

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
        'apiKey': exchange_keys[exchange_id].get_key(),
        'secret': exchange_keys[exchange_id].get_secret(),
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

    del exchange
    del exchange_class
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

    del exchange
    del exchange_class
    exchange_id = 'bittrex'
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

    total_buy = bittrex_buy_total + tradeogre_buy_total + kraken_buy_total + binance_buy_total
    total_sell = bittrex_sell_total + tradeogre_sell_total + kraken_sell_total + binance_sell_total

    binance_buy_percent = ((binance_buy_total/total_buy) * 100)
    tradeogre_buy_percent = ((tradeogre_buy_total/total_buy) * 100)
    kraken_buy_percent = ((kraken_buy_total/total_buy) * 100)
    bittrex_buy_percent = ((bittrex_buy_total/total_buy) * 100)

    binance_sell_percent = ((binance_sell_total / float(total_sell)) * 100)
    tradeogre_sell_percent = ((tradeogre_sell_total / float(total_sell)) * 100)
    kraken_sell_percent = ((kraken_sell_total / float(total_sell)) * 100)
    bittrex_sell_percent = ((bittrex_sell_total / float(total_sell)) * 100)

    if ((OS_TYPE == 'windows')):
        # Clear Screen Windows
        os.system('cls')
    elif ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
        # Clear Screen Linux / Mac
        os.system('clear')

    print("\nRun: " + str(number_of_runs)+"\n")

    message = ""
    print("TradeOgre")
    if tradeogre_buy_total == prev_tradeogre_buy_total:
        message = cc.cc(str(tradeogre_buy_total - prev_tradeogre_buy_total), 'grey')
    elif (tradeogre_buy_total > prev_tradeogre_buy_total):
        message = cc.cc(str(tradeogre_buy_total - prev_tradeogre_buy_total), 'green')
    else:
        message = cc.cc(str(prev_tradeogre_buy_total - tradeogre_buy_total), 'red')
    print("Buy Total:\t" + str(tradeogre_buy_total) + "\t" + message)
    if tradeogre_sell_total == prev_tradeogre_sell_total:
        message = cc.cc(str(tradeogre_sell_total - prev_tradeogre_sell_total), 'grey')
    elif (tradeogre_sell_total > prev_tradeogre_sell_total):
        message = cc.cc(str(tradeogre_sell_total - prev_tradeogre_sell_total), 'green')
    else:
        message = cc.cc(str(prev_tradeogre_sell_total - tradeogre_sell_total), 'red')
    print("Sell Total:\t" + str(tradeogre_sell_total) + "\t" + message)
    print("")

    print("Binance")
    if binance_buy_total == prev_binance_buy_total:
        message = cc.cc(str(binance_buy_total - prev_binance_buy_total), 'grey')
    elif (binance_buy_total > prev_binance_buy_total):
        message = cc.cc(str(binance_buy_total - prev_binance_buy_total), 'green')
    else:
        message = cc.cc(str(prev_binance_buy_total - binance_buy_total), 'red')
    print("Buy Total:\t" + str(binance_buy_total) + "\t\t" + message)
    if binance_sell_total == prev_binance_sell_total:
        message = cc.cc(str(binance_sell_total - prev_binance_sell_total), 'grey')
    elif (binance_sell_total > prev_binance_sell_total):
        message = cc.cc(str(binance_sell_total - prev_binance_sell_total), 'green')
    else:
        message = cc.cc(str(prev_binance_sell_total - binance_sell_total), 'red')
    print("Sell Total:\t" + str(binance_sell_total) + "\t\t" + message)
    print("")

    print("Kraken")
    if kraken_buy_total == prev_kraken_buy_total:
        message = cc.cc(str(kraken_buy_total - prev_kraken_buy_total), 'grey')
    elif (kraken_buy_total > prev_kraken_buy_total):
        message = cc.cc(str(kraken_buy_total - prev_kraken_buy_total), 'green')
    else:
        message = cc.cc(str(prev_kraken_buy_total - kraken_buy_total), 'red')
    print("Buy Total:\t" + str(kraken_buy_total) + "\t" + message)
    if kraken_sell_total == prev_kraken_sell_total:
        message = cc.cc(str(kraken_sell_total - prev_kraken_sell_total), 'grey')
    elif (kraken_sell_total > prev_kraken_sell_total):
        message = cc.cc(str(kraken_sell_total - prev_kraken_sell_total), 'green')
    else:
        message = cc.cc(str(prev_kraken_sell_total - kraken_sell_total), 'red')
    print("Sell Total:\t" + str(kraken_sell_total) + "\t" + message)
    print("")

    print("Bittrex")
    if bittrex_buy_total == prev_bittrex_buy_total:
        message = cc.cc(str(bittrex_buy_total - prev_bittrex_buy_total), 'grey')
    elif (bittrex_buy_total > prev_bittrex_buy_total):
        message = cc.cc(str(bittrex_buy_total - prev_bittrex_buy_total), 'green')
    else:
        message = cc.cc(str(prev_bittrex_buy_total - bittrex_buy_total), 'red')
    print("Buy Total:\t" + str(bittrex_buy_total) + "\t" + message)
    if bittrex_sell_total == prev_bittrex_sell_total:
        message = cc.cc(str(bittrex_sell_total - prev_bittrex_sell_total), 'grey')
    elif (bittrex_sell_total > prev_bittrex_sell_total):
        message = cc.cc(str(bittrex_sell_total - prev_bittrex_sell_total), 'green')
    else:
        message = cc.cc(str(prev_bittrex_sell_total - bittrex_sell_total), 'red')
    print("Sell Total:\t" + str(bittrex_sell_total) + "\t" + message)
    print("")

    big_message = "Binance: "
    print("Buying")
    print("Binance: " + str(binance_buy_percent)[:4] + "%\tTradeogre: " + str(tradeogre_buy_percent)[:4] + "%\tKraken: " + str(kraken_buy_percent)[:4] + "%" + "\tBittrex: " + str(bittrex_buy_percent)[:4] + "%")
    if( float(str(binance_buy_percent)[:4]) > float(str(prev_binance_buy_percent)[:4]) ):
        temp = float(str(binance_buy_percent)[:4]) - float(str(prev_binance_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%",'green')
    elif( float(str(binance_buy_percent)[:4]) < float(str(prev_binance_buy_percent)[:4]) ):
        temp = float(str(prev_binance_buy_percent)[:4]) - float(str(binance_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%",'red')
    else:
        big_message += cc.cc(str(float(str(binance_buy_percent)[:4]))+"%",'grey')
    big_message += "\tTradeogre: "
    if (float(str(tradeogre_buy_percent)[:4]) > float(str(prev_tradeogre_buy_percent)[:4])):
        temp = float(str(tradeogre_buy_percent)[:4]) - float(str(prev_tradeogre_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(tradeogre_buy_percent)[:4]) < float(str(prev_tradeogre_buy_percent)[:4])):
        temp = float(str(prev_tradeogre_buy_percent)[:4]) - float(str(tradeogre_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(tradeogre_buy_percent)[:4]))+"%", 'grey')
    big_message += "\tKraken: "
    if (float(str(kraken_buy_percent)[:4]) > float(str(prev_kraken_buy_percent)[:4])):
        temp = float(str(kraken_buy_percent)[:4]) - float(str(prev_kraken_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(kraken_buy_percent)[:4]) < float(str(prev_kraken_buy_percent)[:4])):
        temp = float(str(prev_kraken_buy_percent)[:4]) - float(str(kraken_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(kraken_buy_percent)[:4]))+"%", 'grey')
    big_message += "\tBittrex: "
    if (float(str(bittrex_buy_percent)[:4]) > float(str(prev_bittrex_buy_percent)[:4])):
        temp = float(str(bittrex_buy_percent)[:4]) - float(str(prev_bittrex_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(bittrex_buy_percent)[:4]) < float(str(prev_bittrex_buy_percent)[:4])):
        temp = float(str(prev_bittrex_buy_percent)[:4]) - float(str(bittrex_buy_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(bittrex_buy_percent)[:4]))+"%", 'grey')
    print(big_message)

    big_message = "Binance: "
    print("\nSelling")
    print("Binance: " + str(binance_sell_percent)[:4] + "%\tTradeogre: " + str(tradeogre_sell_percent)[:4] + "%\tKraken: " + str(kraken_sell_percent)[:4] + "%\tBittrex: " + str(bittrex_sell_percent)[:4] + "%")
    if (float(str(binance_sell_percent)[:4]) > float(str(prev_binance_sell_percent)[:4])):
        temp = float(str(binance_sell_percent)[:4]) - float(str(prev_binance_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(binance_sell_percent)[:4]) < float(str(prev_binance_sell_percent)[:4])):
        temp = float(str(prev_binance_sell_percent)[:4]) - float(str(binance_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(binance_sell_percent)[:4]))+"%", 'grey')
    big_message += "\tTradeogre: "
    if (float(str(tradeogre_sell_percent)[:4]) > float(str(prev_tradeogre_sell_percent)[:4])):
        temp = float(str(tradeogre_sell_percent)[:4]) - float(str(prev_tradeogre_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(tradeogre_sell_percent)[:4]) < float(str(prev_tradeogre_sell_percent)[:4])):
        temp = float(str(prev_tradeogre_sell_percent)[:4]) - float(str(tradeogre_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(tradeogre_sell_percent)[:4]))+"%", 'grey')
    big_message += "\tKraken: "
    if (float(str(kraken_sell_percent)[:4]) > float(str(prev_kraken_sell_percent)[:4])):
        temp = float(str(kraken_sell_percent)[:4]) - float(str(prev_kraken_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(kraken_sell_percent)[:4]) < float(str(prev_kraken_sell_percent)[:4])):
        temp = float(str(prev_kraken_sell_percent)[:4]) - float(str(kraken_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(kraken_sell_percent)[:4]))+"%", 'grey')
    big_message += "\tBittrex: "
    if (float(str(bittrex_sell_percent)[:4]) > float(str(prev_bittrex_sell_percent)[:4])):
        temp = float(str(bittrex_sell_percent)[:4]) - float(str(prev_bittrex_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'green')
    elif (float(str(bittrex_sell_percent)[:4]) < float(str(prev_bittrex_sell_percent)[:4])):
        temp = float(str(prev_bittrex_sell_percent)[:4]) - float(str(bittrex_sell_percent)[:4])
        big_message += cc.cc(str(float(str(temp)[:4]))+"%", 'red')
    else:
        big_message += cc.cc(str(float(str(bittrex_sell_percent)[:4]))+"%", 'grey')
    print(big_message)

    prev_binance_buy_percent = binance_buy_percent
    prev_tradeogre_buy_percent = tradeogre_buy_percent
    prev_kraken_buy_percent = kraken_buy_percent
    prev_bittrex_buy_percent = bittrex_buy_percent
    prev_tradeogre_buy_total = tradeogre_buy_total
    prev_tradeogre_sell_total = tradeogre_sell_total
    prev_binance_buy_total = binance_buy_total
    prev_binance_sell_total = binance_sell_total
    prev_kraken_buy_total = kraken_buy_total
    prev_kraken_sell_total = kraken_sell_total
    prev_bittrex_buy_total = bittrex_buy_total
    prev_bittrex_sell_total = bittrex_sell_total
    prev_total_buy = total_buy
    prev_total_sell = total_sell
    prev_binance_buy_percent = binance_buy_percent
    prev_tradeogre_buy_percent = tradeogre_buy_percent
    prev_kraken_buy_percent = kraken_buy_percent
    prev_bittrex_buy_percent = bittrex_buy_percent
    prev_binance_sell_percent = binance_sell_percent
    prev_tradeogre_sell_percent = tradeogre_sell_percent
    prev_kraken_sell_percent = kraken_sell_percent
    prev_bittrex_sell_percent = bittrex_sell_percent

    number_of_runs += 1



#print("Selling Total:")
#print(str())

runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())