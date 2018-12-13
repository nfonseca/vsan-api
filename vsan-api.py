#!/usr/bin/python



from pyVmomi import vim, vmodl
from pyVim import connect
import argparse
import getpass
import atexit
import logging
import sys


# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


# we set logging level
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s" # trick to print the function name
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logger = logging.getLogger(__name__) # we instantiate  a global logger for the main program




def GetArgs():
    """
    Supports the command-line arguments listed below.
    """

    parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
    parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
    parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
    parser.add_argument('-p', '--password', required=False, action='store', help='Password')
    args = parser.parse_args()
    return args

#

def main():




    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        # connection string

        si = connect.SmartConnectNoSSL(host=args.vc,
                                       user=args.user,
                                       pwd=password)

        content = si.RetrieveServiceContent()
        # we close the vc connection
        print(content)
        print(content+0)
        atexit.register(connect.Disconnect, si)



    except Exception  as err:

        logger.exception('Error Here!')


main()




# todo - add a connect function to VC using argparse
# todo - main goal of the tool is to gather config information from the cluster
# todo - Goal 1: Get Cluster Configuration



