#!/usr/bin/python

 # Script that retrieves the mapping of the vm property instanceUuid and maps it out to the VM Friendly name
 # script to be run from vxrail manager

import sys

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import argparse
import getpass
import atexit
import ssl
 # Import the vSAN API python bindings and utilities.
 import vsanmgmtObjects
import vsanapiutils


 # disable warnings from SSL Check when connecting to VC
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


 # Function to change the vSAN SP of all the VMs in the Cluster
def ChangevSANSP():

     return None


def main():
    global content
    global si

    context = None

    if sys.version_info[:3] > (2, 7, 8):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:
        # connection string

        # connection string

        #        si = connect.SmartConnectNoSSL(host=args.vc,
        #                                       user=args.user,
        #                                       pwd=password,
        #                                       sslContext=context)

        si = SmartConnect(host=args.vc,
                          user=args.user,
                          pwd=password,
                          sslContext=context)

        content = si.RetrieveServiceContent()
        # we close the vc connection
        atexit.register(Disconnect, si)


         print(content)
         # we close the vc connection

         cluster = si.content.rootFolder.childEntity[0].hostFolder.childEntity[0]
         print(cluster) # returns the moref for the cluster




         vcMos = vsanapiutils.GetVsanVcMos(si._stub, context=context)
         vccs = vcMos['vsan-cluster-config-system']
         vsanCluster = vccs.VsanClusterGetConfig(cluster=cluster)


         print(vsanCluster)

     except Exception  as err:

         print('Error in main(): ', err)


main()
