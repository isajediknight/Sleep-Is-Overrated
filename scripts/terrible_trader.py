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
pf = PrettyFormatting(18)

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
buying, selling = thread1.get_thread_results()
data.add_order_book_results(timestamp,'kraken',buying, selling)#,thread1.get_buy_total(), thread1.get_sell_total())

buying, selling = thread2.get_thread_results()
data.add_order_book_results(timestamp, 'binance', buying, selling)#, thread2.get_buy_total(), thread2.get_sell_total())

buying, selling = thread3.get_thread_results()
data.add_order_book_results(timestamp, 'bittrex', buying, selling)#, thread3.get_buy_total(), thread3.get_sell_total())

buying, selling = thread4.get_thread_results()
data.add_order_book_results(timestamp, 'tradeogre', buying, selling)#, thread4.get_buy_total(), thread4.get_sell_total())

buying, selling = thread5.get_thread_results()
data.add_order_book_results(timestamp, 'poloniex', buying, selling)#, thread5.get_buy_total(), thread5.get_sell_total())

del thread1
del thread2
del thread3
del thread4
del thread5

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
buying, selling = thread1.get_thread_results()
data.add_order_book_results(timestamp,'kraken',buying, selling)#,thread1.get_buy_total(), thread1.get_sell_total())

buying, selling = thread2.get_thread_results()
data.add_order_book_results(timestamp, 'binance', buying, selling)#, thread2.get_buy_total(), thread2.get_sell_total())

buying, selling = thread3.get_thread_results()
data.add_order_book_results(timestamp, 'bittrex', buying, selling)#, thread3.get_buy_total(), thread3.get_sell_total())

buying, selling = thread4.get_thread_results()
data.add_order_book_results(timestamp, 'tradeogre', buying, selling)#, thread4.get_buy_total(), thread4.get_sell_total())

buying, selling = thread5.get_thread_results()
data.add_order_book_results(timestamp, 'poloniex', buying, selling)#, thread5.get_buy_total(), thread5.get_sell_total())

runs = 0
while(runs < 10):
    if ((OS_TYPE == 'windows')):
        # Clear Screen Windows
        os.system('cls')
    elif ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
        # Clear Screen Linux / Mac
        os.system('clear')

    data.compare_previous_order_book()

    del thread1
    del thread2
    del thread3
    del thread4
    del thread5

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
    try:
        buying, selling = thread1.get_thread_results()
        data.add_order_book_results(timestamp, 'kraken', buying,selling)  # ,thread1.get_buy_total(), thread1.get_sell_total())
    except:
        print("Error kraken")

    try:
        buying, selling = thread2.get_thread_results()
        data.add_order_book_results(timestamp, 'binance', buying,selling)  # , thread2.get_buy_total(), thread2.get_sell_total())
    except:
        print("Error binance")

    try:
        buying, selling = thread3.get_thread_results()
        data.add_order_book_results(timestamp, 'bittrex', buying,selling)  # , thread3.get_buy_total(), thread3.get_sell_total())
    except:
        print("Error bittrex")

    try:
        buying, selling = thread4.get_thread_results()
        data.add_order_book_results(timestamp, 'tradeogre', buying,selling)  # , thread4.get_buy_total(), thread4.get_sell_total())
    except:
        print("Error tradeogre")

    try:
        buying, selling = thread5.get_thread_results()
        data.add_order_book_results(timestamp, 'poloniex', buying,selling)  # , thread5.get_buy_total(), thread5.get_sell_total())
    except:
        print("Error poloniex")

    runs += 1

if ((OS_TYPE == 'windows')):
    # Clear Screen Windows
    os.system('cls')
elif ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    # Clear Screen Linux / Mac
    os.system('clear')

data.compare_previous_order_book()

runtime.stop()
print("\n Program Runtime: " + runtime.human_readable_string())