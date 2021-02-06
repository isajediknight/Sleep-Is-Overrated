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

from pseudothreading import *

from tracking import *
# < ---  End  Custom Classes Import --- >

# Time all the things!
runtime = Benchmark()

# Text Coloration
cc = ColoredText(['exchange'],['38;5;214m'])

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

for run_counter in range(0,2):

    # Define threads to run
    # 'order book'
    thread1 = thread('kraken', main, alt, 'ticker')
    thread2 = thread('binance', main, alt, 'ticker');
    thread3 = thread('bittrex', main, alt, 'ticker');
    thread4 = thread('tradeogre', main, alt, 'ticker');

    # Run the threads!
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    timestamp = str(datetime.datetime.now().utcnow().timestamp())
    bid, ask, bid_volume, ask_volume = thread1.get_thread_results()
    data.add_ticker_results(timestamp,'kraken',bid,ask,bid_volume,ask_volume)

    bid, ask, bid_volume, ask_volume = thread2.get_thread_results()
    data.add_ticker_results(timestamp, 'binance', bid, ask, bid_volume, ask_volume)

    bid, ask, bid_volume, ask_volume = thread3.get_thread_results()
    data.add_ticker_results(timestamp, 'bittrex', bid, ask, bid_volume, ask_volume)

    bid, ask, bid_volume, ask_volume = thread4.get_thread_results()
    data.add_ticker_results(timestamp, 'tradeogre', bid, ask, bid_volume, ask_volume)

    temp = data.get_ticker()[timestamp]['binance'].get_bid()
    print(temp+"\t"+thread1.get_elapsed_time().human_readable_string())
    temp = data.get_ticker()[timestamp]['bittrex'].get_bid()
    print(temp+"\t"+thread2.get_elapsed_time().human_readable_string())
    temp = data.get_ticker()[timestamp]['tradeogre'].get_bid()
    print(temp+"\t"+thread3.get_elapsed_time().human_readable_string())
    temp = data.get_ticker()[timestamp]['kraken'].get_bid()
    print(temp+"\t"+thread4.get_elapsed_time().human_readable_string())
    print("")

    del thread1
    del thread2
    del thread3
    del thread4

#print(cc.cc("Kraken:",'exchange'))
#print(str(thread1.get_thread_results())+"\n")
#print(cc.cc("Binance:",'exchange'))
#print(str(thread2.get_thread_results())+"\n")
#print(cc.cc("Bittrex:",'exchange'))
#print(str(thread3.get_thread_results())+"\n")
#print(cc.cc("TradeOgre:",'exchange'))
#print(str(thread4.get_thread_results())+"\n")

runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())