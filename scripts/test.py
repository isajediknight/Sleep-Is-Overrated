import datetime,time,os,sys,json,threading

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

from crypto_metrics import *

from command_line_arguments import *

from pretty_formatting import *
# < ---  End  Custom Classes Import --- >

runtime = Benchmark()

# Get parameters from commandline
parameters = Parse()
parameters.add_expectation('-crypto-main', 'string', True, False)
parameters.add_expectation('-crypto-alt', 'string', True, False)
parameters.parse_commandline()
parameters.validate_requirements()

#master = Metrics(parameters.get_parameter('-crypto-main').value, parameters.get_parameter('-crypto-alt').value)
#buying, selling = master.call_order_book('kraken')
#print(buying)
#print("")
#print(selling)

pf = PrettyFormatting(40)
pf_no_exchanges = PrettyFormatting(50)

print(pf_no_exchanges.add_spaces('0.00000095') + '0.00000095')
print(pf_no_exchanges.add_spaces('0.00000096') + '0.00000096')
print(pf_no_exchanges.add_spaces('0.00000097') + '0.00000097')
print(pf_no_exchanges.add_spaces('0.00000098') + '0.00000098')

message = ""
exchanges = 'tradeogre bittrex '
message += pf.add_spaces(exchanges)
message += exchanges
message += "0.00000099"
print(message)
message = ""
print(pf_no_exchanges.add_spaces('0.00000100') + '0.00000100')
print(pf_no_exchanges.add_spaces('0.00000101') + '0.00000101')
print(pf_no_exchanges.add_spaces('0.00000102') + '0.00000102')


runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())