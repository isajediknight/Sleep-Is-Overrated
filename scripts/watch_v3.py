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
thread1 = thread('kraken', main, alt, 'ticker')
thread2 = thread('binance', main, alt, 'ticker');
thread3 = thread('bittrex', main, alt, 'ticker');
thread4 = thread('tradeogre', main, alt, 'ticker');
thread5 = thread('poloniex', main, alt, 'ticker');

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

track_trending = {}
track_trending['kraken'] = {}
track_trending['binance'] = {}
track_trending['bittrex'] = {}
track_trending['tradeogre'] = {}
track_trending['poloniex'] = {}
track_trending['kraken']['bid'] = Trending()
track_trending['kraken']['ask'] = Trending()
track_trending['binance']['bid'] = Trending()
track_trending['binance']['ask'] = Trending()
track_trending['bittrex']['bid'] = Trending()
track_trending['bittrex']['ask'] = Trending()
track_trending['tradeogre']['bid'] = Trending()
track_trending['tradeogre']['ask'] = Trending()
track_trending['poloniex']['bid'] = Trending()
track_trending['poloniex']['ask'] = Trending()

for run_counter in range(0,4):

    # Define threads to run
    # 'order book'
    thread1 = thread('kraken', main, alt, 'ticker')
    thread2 = thread('binance', main, alt, 'ticker');
    thread3 = thread('bittrex', main, alt, 'ticker');
    thread4 = thread('tradeogre', main, alt, 'ticker');
    thread5 = thread('poloniex', main, alt, 'ticker');

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

    # OS Compatibility for importing Class Files
    if ((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
        os.system('clear')
    elif ((OS_TYPE == 'windows')):
        os.system('cls')

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

    prev_timestamp = sorted(data.get_keys())[-2]
    prev_results_bid = []
    prev_results_bid.append(data.get_ticker()[prev_timestamp]['kraken'].get_bid() + "|kraken")
    prev_results_bid.append(data.get_ticker()[prev_timestamp]['binance'].get_bid() + "|binance")
    prev_results_bid.append(data.get_ticker()[prev_timestamp]['bittrex'].get_bid() + "|bittrex")
    prev_results_bid.append(data.get_ticker()[prev_timestamp]['tradeogre'].get_bid() + "|tradeogre")
    prev_results_bid.append(data.get_ticker()[prev_timestamp]['poloniex'].get_bid() + "|poloniex")

    current_results_bid = []
    current_results_bid.append(data.get_ticker()[timestamp]['kraken'].get_bid() + "|kraken")
    current_results_bid.append(data.get_ticker()[timestamp]['binance'].get_bid() + "|binance")
    current_results_bid.append(data.get_ticker()[timestamp]['bittrex'].get_bid() + "|bittrex")
    current_results_bid.append(data.get_ticker()[timestamp]['tradeogre'].get_bid() + "|tradeogre")
    current_results_bid.append(data.get_ticker()[timestamp]['poloniex'].get_bid() + "|poloniex")

    prev_results_ask = []
    prev_results_ask.append(data.get_ticker()[prev_timestamp]['kraken'].get_ask() + "|kraken")
    prev_results_ask.append(data.get_ticker()[prev_timestamp]['binance'].get_ask() + "|binance")
    prev_results_ask.append(data.get_ticker()[prev_timestamp]['bittrex'].get_ask() + "|bittrex")
    prev_results_ask.append(data.get_ticker()[prev_timestamp]['tradeogre'].get_ask() + "|tradeogre")
    prev_results_ask.append(data.get_ticker()[prev_timestamp]['poloniex'].get_ask() + "|poloniex")

    current_results_ask = []
    current_results_ask.append(data.get_ticker()[timestamp]['kraken'].get_ask() + "|kraken")
    current_results_ask.append(data.get_ticker()[timestamp]['binance'].get_ask() + "|binance")
    current_results_ask.append(data.get_ticker()[timestamp]['bittrex'].get_ask() + "|bittrex")
    current_results_ask.append(data.get_ticker()[timestamp]['tradeogre'].get_ask() + "|tradeogre")
    current_results_ask.append(data.get_ticker()[timestamp]['poloniex'].get_ask() + "|poloniex")

    sorted_exchange_order_bid = []
    sorted_price_order_bid = []
    for exchange_order in sorted(current_results_bid):
        sorted_exchange_order_bid.append(exchange_order.split("|")[1])
        sorted_price_order_bid.append(exchange_order.split("|")[0])

    sorted_exchange_order_ask = []
    sorted_price_order_ask = []
    for exchange_order in reversed(sorted(current_results_ask)):
        sorted_exchange_order_ask.append(exchange_order.split("|")[1])
        sorted_price_order_ask.append(exchange_order.split("|")[0])

    print("\n Run: " + str(run_counter) + " / "+str(50)+"\t\t\t\t" + alt + "\n")

    print(" Buy:")
    for exchange in sorted_exchange_order_ask:
        old = data.get_ticker()[prev_timestamp][exchange].get_ask()
        new = data.get_ticker()[timestamp][exchange].get_ask()
        diff, color = format_diff_output.diff_two(old, new)
        if exchange == 'kraken':
            tab = "\t\t"
        else:
            tab = "\t"
        message = " " + cc.cc(exchange, 'exchange') + tab + cc.cc(diff, color) + "\t" + new
        track_trending[exchange]['ask'].compute_trend(color,int(diff))
        message += format_diff_output.add_spaces(track_trending[exchange]['ask'].get_cc_trend_count())
        message += " " + cc.cc(str(track_trending[exchange]['ask'].get_cc_trend_count()),track_trending[exchange]['ask'].get_cc_color())
        message += " " + format_diff_output.add_spaces(track_trending[exchange]['ask'].get_cc_direction_total())
        message += cc.cc(str(track_trending[exchange]['ask'].get_cc_direction_total()),track_trending[exchange]['ask'].get_cc_color())
        print(message)

    print("\n Sell:")
    for exchange in reversed(sorted_exchange_order_bid):
        old = data.get_ticker()[prev_timestamp][exchange].get_bid()
        new = data.get_ticker()[timestamp][exchange].get_bid()
        diff, color = format_diff_output.diff_two(old, new)
        if exchange == 'kraken':
            tab = "\t\t"
        else:
            tab = "\t"
        message = " " + cc.cc(exchange, 'exchange') + tab + cc.cc(diff, color) + "\t" + new
        track_trending[exchange]['bid'].compute_trend(color,int(diff))
        message += format_diff_output.add_spaces(track_trending[exchange]['bid'].get_cc_trend_count())
        message += " " + cc.cc(str(track_trending[exchange]['bid'].get_cc_trend_count()),track_trending[exchange]['bid'].get_cc_color())
        message += " " + format_diff_output.add_spaces(track_trending[exchange]['bid'].get_cc_direction_total())
        message += cc.cc(str(track_trending[exchange]['bid'].get_cc_direction_total()),track_trending[exchange]['bid'].get_cc_color())
        print(message)

    #print("\n " + cc.cc(sorted_exchange_order_bid[-1],'exchange')  + " "+ str(sorted_price_order_bid[-1]))
    #print( " > " + cc.cc(sorted_exchange_order_ask[-1],'exchange')  + " "+ str(sorted_price_order_ask[-1]))
    #print( " = " + str(float(sorted_price_order_bid[-1]) > float(sorted_price_order_ask[-1])))
    #                           sell                               buy
    if float(sorted_price_order_bid[-1]) > float(sorted_price_order_ask[-1]):
        print("\n")
        print(cc.cc(" Arbitrage Detected!",'attention'))
        my_string = ""
        sell_exchange = sorted_exchange_order_bid[-1]
        buy_exchange = sorted_exchange_order_ask[-1]
        print("\n Buy:")
        print(" " + cc.cc(buy_exchange,'exchange') + "   \t\t" + sorted_price_order_ask[-1] + "\n")
        print(" Sell:")
        counter = 0
        for bid in sorted_price_order_bid:
            if sorted_price_order_bid[-1] == bid:
                print(" " + cc.cc(sorted_exchange_order_bid[counter], 'exchange') + "   \t\t" + bid)
            counter += 1
        diff, color = format_diff_output.diff_two(sorted_price_order_ask[-1], sorted_price_order_bid[-1])
        print("\n Profit: \t\t     " + cc.cc(diff, color))

    #temp = data.get_ticker()[timestamp]['binance'].get_bid()
    #print(temp+"\t"+thread1.get_elapsed_time().human_readable_string())
    #temp = data.get_ticker()[timestamp]['bittrex'].get_bid()
    #print(temp+"\t"+thread2.get_elapsed_time().human_readable_string())
    #temp = data.get_ticker()[timestamp]['tradeogre'].get_bid()
    #print(temp+"\t"+thread3.get_elapsed_time().human_readable_string())
    #temp = data.get_ticker()[timestamp]['kraken'].get_bid()
    #print(temp+"\t"+thread4.get_elapsed_time().human_readable_string())
    #print("")

    del thread1
    del thread2
    del thread3
    del thread4
    del thread5

#print(cc.cc("Kraken:",'exchange'))
#print(str(thread1.get_thread_results())+"\n")
#print(cc.cc("Binance:",'exchange'))
#print(str(thread2.get_thread_results())+"\n")
#print(cc.cc("Bittrex:",'exchange'))
#print(str(thread3.get_thread_results())+"\n")
#print(cc.cc("TradeOgre:",'exchange'))
#print(str(thread4.get_thread_results())+"\n")

runtime.stop()
print("\n Program Runtime: " + runtime.human_readable_string())