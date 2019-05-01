#!/usr/bin/python

# Script that retrieves the mapping of the vm property instanceUuid and maps it out to the VM Friendly name
# script to be run from vxrail manager

import sys
# Add Pyvmomi PATH on VxRail Manager
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")
from pyVmomi import vim, vmodl
from pyVim import connect

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



def main():
    global content
    global si

    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        # connection string


        # connection string

        si = connect.SmartConnectNoSSL(host=args.vc,
                                       user=args.user,
                                       pwd=password)

        content = si.RetrieveServiceContent()
        # we close the vc connection
        atexit.register(connect.Disconnect, si)

        print(content)
        # we close the vc connection
        atexit.register(connect.Disconnect, si)

        cluster = si.content.rootFolder.childEntity[0].hostFolder.childEntity[1]
        print(cluster) # returns the moref for the cluster

#        getvSANConfig = vim.cluster.VsanVcClusterConfigSystem.VsanClusterGetConfig(cluster=cluster)
        vsancluster = vim.cluster.VsanVcClusterConfigSystem(cluster)

        config = vim.cluster.VsanVcClusterConfigSystem.VsanClusterGetConfig(_this=vsancluster,cluster=cluster)



        print(getvSANConfig)

    except Exception  as err:

        print('Error in main(): ', err)


main()

# Implementation

# todo - Retrieve vSAN version via API

