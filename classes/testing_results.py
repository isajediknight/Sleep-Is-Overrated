# Default Modules
import os,sys

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
# < ---  End  Custom Classes Import --- >

class TestResults:

    # Only way I know to counter the total instances of this Class
    total_counter = []
    pass_counter = []
    fail_counter = []

    def __init__(self,description,result,check='Boolean logic sent in as a string which was evaluated to see if this passed or failed'):
        """
        description
            Datatype: String
            What are we testing?

        unit_test
            Datatype: Int
            Which Unit Test

        test_sub_number
            Datatype: Int
            Within this Unit Test which test is this

        result
            Datatype: Boolean
            Was the test successful?
        """
        self.total_counter.append(0)
        self.result = result
        self.description = description
        self.test_total_number = len(self.total_counter)
        self.check = check

        if(result):
            self.pass_counter.append(0)
        else:
            self.fail_counter.append(0)

    def return_pass_or_fail_string(self):
        """
        String Colored Text for if the test passed or failed
        """

        color_test = ColoredText(['datatype'], ['38;5;30m'])

        if(self.result):
            display = color_test.cc('Passed', 'green')
        else:
            display = color_test.cc('Failed', 'red')

        return " [ " + display + " ] "

    def return_pass_or_fail_test_number_string(self):
        """
        String Colored Text for if the test passed or failed
        """

        color_test = ColoredText(['datatype'], ['38;5;30m'])

        if(self.result):
            display = ((6 - len(str(self.test_total_number))) * " ") + color_test.cc(str(self.test_total_number), 'green')
        else:
            display = ((6 - len(str(self.test_total_number))) * " ") + color_test.cc(str(self.test_total_number), 'red')

        return " [ " + display + " ] "

    def set_result(self,result):
        """
        I know this is terrible but it's quick and dirty to track our passes and fails
        """
        if(self.result == result):
            pass
        elif((result == True) and (self.result == False)):
            self.pass_counter.append(0)
            self.fail_counter.pop()
        else:
            self.fail_counter.append(0)
            self.pass_counter.pop()
        self.result = result

    def get_result(self):
        return self.result

    def set_description(self,description):
        self.description = description

    def get_description(self):
        return self.description

    def set_test_sub_number(self,test_sub_number):
        self.test_sub_number = test_sub_number

    def get_test_sub_number(self):
        return self.test_sub_number

    def get_check(self):
        return self.check