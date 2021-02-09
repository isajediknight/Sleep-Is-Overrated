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

    def __init__(self, exchange, main, alt, api_call_type):

        self.exchange = exchange.lower()
        self.main = main.upper()
        self.alt = alt.upper()
        self.api_call_type = api_call_type.lower()

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

        self.thread_results = {}

        # Time all the things!
        self.runtime = Benchmark()

        if self.api_call_type == 'order book':

            if self.exchange == 'tradeogre':
                buying, selling = master.call_order_book('tradeogre')

                self.buy_total = float(0)
                for key in list(buying.keys()):
                    self.buy_total += float(buying[key])

                self.sell_total = float(0)
                for key in list(selling.keys()):
                    self.sell_total += float(selling[key])

                # Debugging
                #print("TradeOgre")
                #print("Buying: " + str(self.buy_total))
                #print("Selling: " + str(self.sell_total))

                # Save this data to return it
                self.thread_results[self.exchange] =  (self.buy_total, self.sell_total)

            elif self.exchange == 'kraken':

                buying, selling = master.call_order_book('kraken')

                self.buy_total = float(0)
                for price, total, unknown in buying:
                    self.buy_total += float(total)

                self.sell_total = float(0)
                for price, total, unknown in selling:
                    self.sell_total += float(total)

                # Debugging
                #print("Kraken")
                #print("Buying: " + str(self.buy_total))
                #print("Selling: " + str(self.sell_total))

                # Save this data to return it
                self.thread_results[self.exchange] =  (self.buy_total, self.sell_total)

            else:
                buying, selling = master.call_order_book(self.exchange)

                self.buy_total = float(0)
                for price, total in buying:
                    self.buy_total += float(total)

                self.sell_total = float(0)
                for price, total in selling:
                    self.sell_total += float(total)

                # Save this data to return it
                self.thread_results[self.exchange] =  (self.buy_total, self.sell_total)

        elif self.api_call_type == 'ticker':


            if self.exchange == 'tradeogre':
                self.thread_results[self.exchange] = master.call_fetch_ticker('tradeogre')
            else:
                self.thread_results[self.exchange] = master.call_fetch_ticker(self.exchange)[self.crypto_pair.get_corrected_pair(self.exchange)]

        else:
            raise Exception(" API Call " + self.api_call_type + " is not currently supported")

        self.runtime.stop()

    def get_thread_results(self):
        """
        There has to be a better way to do this...
        Getting data from the finished thread
        """
        if self.api_call_type == 'ticker':

            # non tradeogre needs to be changed to non scientific notation
            bid = self.thread_results[self.exchange]['bid']
            ask = self.thread_results[self.exchange]['ask']

            if self.exchange == 'tradeogre':

                bid_volume = self.thread_results[self.exchange]['volume']
                ask_volume = self.thread_results[self.exchange]['volume']
            else:
                bid = format(bid, '.8f')
                ask = format(ask, '.8f')
                bid_volume = self.thread_results[self.exchange]['bidVolume']
                ask_volume = self.thread_results[self.exchange]['askVolume']

            return bid,ask,bid_volume,ask_volume

        else:
            return self.thread_results

    def get_elapsed_time(self):
        """
        Return the Benchmark object
        """
        return self.runtime