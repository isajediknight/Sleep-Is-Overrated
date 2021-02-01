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

    def call_order_book(self,exchange='tradeogre'):

        if(exchange in list(self.exchange_keys.keys())):
            if
        else:
            raise Exception(" Exchange " + exchange + " information is not present in the keys file: " + INPUTS_DIR + 'untitled.pyc')


