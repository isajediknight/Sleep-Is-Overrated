
import datetime,time,os,sys,requests,json,threading

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

from crypto_metrics import *
# < ---  End  Custom Classes Import --- >

class thread(threading.Thread):
    def __init__(self, exchange, main, alt):

        self.exchange = exchange
        self.main = main
        self.alt = alt

        self.crypto_pair = CryptoPairs('tradeogre', main, alt)

        # Read in exchanges and API keys
        self.exchange_keys = {}
        readfile = open(INPUTS_DIR + 'untitled.pyc', 'r')
        for line in readfile:
            temp_exchange, temp_key, temp_secret = list(line.strip().split(','))
            self.exchange_keys[temp_exchange] = Credentials(temp_exchange, temp_key, temp_secret)
            # print(temp_exchange + "\t" + temp_key + "\t" + temp_secret)
        readfile.close()

        # helper function to execute the threads

        threading.Thread.__init__(self)

    def run(self):
        master = Metrics(self.main, self.alt)

        if self.exchange == 'tradeogre':
            buying, selling = master.call_order_book('tradeogre')

            self.buy_total = float(0)
            for key in list(buying.keys()):
                self.buy_total += float(buying[key])

            self.sell_total = float(0)
            for key in list(selling.keys()):
                self.sell_total += float(selling[key])

            print("TradeOgre")
            print("Buying: " + str(self.buy_total))
            print("Selling: " + str(self.sell_total))
        elif self.exchange == 'kraken':

            #order_book_dict_result = exchange.fetch_order_book(self.crypto_pair.get_corrected_pair_for_exchange())  # 'BTC/USDT')

            #buying = kraken_dict_result['bids']
            #selling = kraken_dict_result['asks']

            buying, selling = master.call_order_book('kraken')

            self.buy_total = float(0)
            for price, total, unknown in buying:
                self.buy_total += float(total)

            self.sell_total = float(0)
            for price, total, unknown in selling:
                self.sell_total += float(total)

            print("Kraken")
            print("Buying: " + str(self.buy_total))
            print("Selling: " + str(self.sell_total))
        elif self.exchange == 'binance':

            buying, selling = master.call_order_book('binance')

            self.buy_total = float(0)
            for price, total in buying:
                self.buy_total += float(total)

            self.sell_total = float(0)
            for price, total in selling:
                self.sell_total += float(total)

            print("Binance")
            print("Buying: " + str(self.buy_total))
            print("Selling: " + str(self.sell_total))

        elif self.exchange == 'bittrex':

            buying, selling = master.call_order_book('bittrex')

            self.buy_total = float(0)
            for price, total in buying:
                self.buy_total += float(total)

            self.sell_total = float(0)
            for price, total in selling:
                self.sell_total += float(total)

            print("Bittrex")
            print("Buying: " + str(self.buy_total))
            print("Selling: " + str(self.sell_total))

        else:
            raise Exception(" Exchange " + self.exchange + " is not currently supported")