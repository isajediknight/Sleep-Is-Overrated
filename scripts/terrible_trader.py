import datetime,time,os,sys

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

from crypto_pairs import *

from command_line_arguments import *

from market_watch import *

from tracking import *

from pretty_formatting import *
# < ---  End  Custom Classes Import --- >

# Time all the things!
runtime = Benchmark()

# Text Coloration
cc = ColoredText(['exchange','attention'],['38;5;214m','38;5;226m'])

# Get parameters from commandline
parameters = Parse()

# Define what we're expecting to be passed in
parameters.add_expectation('-crypto-main', 'string', True, False)
parameters.add_expectation('-crypto-alt', 'string', True, False)

# Assign passed in values
parameters.parse_commandline()

# Check expectations were met
parameters.validate_requirements()

# World Reserve Crypto
main = parameters.get_parameter('-crypto-main').value
# Poor wanna be Crypto
alt = parameters.get_parameter('-crypto-alt').value

data = Tracking(main,alt)
format_diff_output = PrettyFormatting(5)

# Do one run
# Define threads to run
# 'order book'
thread1 = thread('kraken', main, alt, 'order book')
thread2 = thread('binance', main, alt, 'order book');
thread3 = thread('bittrex', main, alt, 'order book');
thread4 = thread('tradeogre', main, alt, 'order book');
thread5 = thread('poloniex', main, alt, 'order book');

# Run the threads!
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

# Wait for all threads to finish
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()

timestamp = str(datetime.datetime.now().utcnow().timestamp())
bid, ask, bid_volume, ask_volume = thread1.get_thread_results()
data.add_ticker_results(timestamp,'kraken',bid,ask,bid_volume,ask_volume)

bid, ask, bid_volume, ask_volume = thread2.get_thread_results()
data.add_ticker_results(timestamp, 'binance', bid, ask, bid_volume, ask_volume)

bid, ask, bid_volume, ask_volume = thread3.get_thread_results()
data.add_ticker_results(timestamp, 'bittrex', bid, ask, bid_volume, ask_volume)

bid, ask, bid_volume, ask_volume = thread4.get_thread_results()
data.add_ticker_results(timestamp, 'tradeogre', bid, ask, bid_volume, ask_volume)

bid, ask, bid_volume, ask_volume = thread5.get_thread_results()
data.add_ticker_results(timestamp, 'poloniex', bid, ask, bid_volume, ask_volume)

print("\n bid:\t" + format(ticker['DOGE/BTC']['bid'], '.8f'))
print(" bidVolume:\t" + str(ticker['DOGE/BTC']['bidVolume']))
print(" ask:\t" + format(ticker['DOGE/BTC']['ask'], '.8f'))
print(" askVolume:\t" + str(ticker['DOGE/BTC']['askVolume']))
print("")
print(buying)
print("")
#print(buying[ticker['DOGE/BTC']['bid']])
print(str(buying[0][1]) + " @ " + format(buying[0][0],'.8f'))
print(buying[-1])

print("Buying:")
for counter in range(5,-1,-1):
    print(str(buying[counter][1]) + " @ " + format(buying[counter][0],'.8f'))

print("")
print("Selling:")
for counter in range(0,5):
    print(str(selling[counter][1]) + " @ " + format(selling[counter][0],'.8f'))