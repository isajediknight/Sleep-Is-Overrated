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

from command_line_arguments import *
# < ---  End  Custom Classes Import --- >

# < --- Begin Module Classes Import --- >
from tradeogre import *
# < ---  End  Model Classes Import  --- >

runtime = Benchmark()

parameters = Parse()
parameters.add_expectation('-crypto-pair', 'string', True, False)
parameters.parse_commandline()
parameters.validate_requirements()

exchange = {}
readfile = open(INPUTS_DIR + 'untitled.pyc', 'r')
for line in readfile:
    temp_exchange,temp_key,temp_secret = list(line.strip().split(','))
    exchange[temp_exchange] = Credentials(temp_exchange,temp_key,temp_secret)
    #print(temp_exchange + "\t" + temp_key + "\t" + temp_secret)
readfile.close()

print(parameters.get_parameter_names())
crypt_pair = parameters.get_parameter('-crypto-pair').value

api_tradeogre = TradeOgre(exchange['tradeogre'].get_key(),exchange['tradeogre'].get_secret())
#print(str(api_tradeogre.order_book(crypt_pair)))

tradeogre_json_result = api_tradeogre.order_book(crypt_pair)
tradeogre_buy = tradeogre_json_result['buy']
tradeogre_sell = tradeogre_json_result['sell']

tradeogre_buy_total = float(0)
for key in list(tradeogre_buy.keys()):
    tradeogre_buy_total += float(tradeogre_buy[key])

tradeogre_sell_total = float(0)
for key in list(tradeogre_sell.keys()):
    tradeogre_sell_total += float(tradeogre_sell[key])

print("TradeOgre")
print("Buy Total: " + str(tradeogre_buy_total))
print("Sell Total: " + str(tradeogre_sell_total))

#key = input("Key: ")
#secret = input("Secret: ")
#session = requests.Session()
#session.auth = ('-u',key+':'+secret.strip())#+'@'
#connection_validation = session.get('https://tradeogre.com/api/v1')#'+key+':'+secret+'
#print(str(connection_validation.status_code))
#session.close()


runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())