#!/usr/bin/python



from pyVmomi import vim, vmodl
from pyVim import connect
import argparse
import getpass
import atexit


# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")



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
        atexit.register(connect.Disconnect, si)

        while True:
            global selection
            vx = findvxrm()
            print('Continue ?')
            cont = input('Type Y or N: ')
            if cont == 'Y':
                for vxrm_ip, esxi in vx.items():
                    print(f'VXRM Found with IP: {vxrm_ip} running on ESXi: {esxi} \n')

                selection = input(
                    'Type the IP of VxRM to Connect to or type "all" to run the same API on ALL VxRM : ')
                if selection in vx:

                    print('Checking VxRail Manager: ', selection)

                    api = api_list(selection)

                    if api is not None:

                        call_api(api[0], api[2])

                    else:
                        break
                elif selection == 'all':
                    run_same_api()

            else:
                print('\nExiting Program ...')
                sys.exit(1)

    except Exception  as err:

        print('Error in main(): ', err)


main()




# todo - add a connect function to VC using argparse
# todo - main goal of the tool is to gather config information from the cluster
# todo - Goal 1: Get Cluster Configuration



