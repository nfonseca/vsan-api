#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Put something here
"""

__author__ = 'DELL EMC'

import sys
# add the path for Pyvmomi on VxRail Manager
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")
import ssl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import argparse
import getpass
#import the VSAN API python bindings
import vsanmgmtObjects
import vsanapiutils

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for VSAN SDK sample application')
   parser.add_argument('-s', '--host', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   parser.add_argument('--cluster', dest='clusterName', metavar="CLUSTER",
                      default='VSAN-Cluster')
   args = parser.parse_args()
   return args



def getClusterInstance(clusterName, serviceInstance):
   content = serviceInstance.RetrieveContent()
   searchIndex = content.searchIndex
   datacenters = content.rootFolder.childEntity
   for datacenter in datacenters:
      cluster = searchIndex.FindChild(datacenter.hostFolder, clusterName)
      if cluster is not None:
         return cluster
   return None


#Start program
def main():
   args = GetArgs()
   if args.password:
      password = args.password
   else:
      password = getpass.getpass(prompt='Enter password for host %s and '
                                        'user %s: ' % (args.host,args.user))

   #For python 2.7.9 and later, the defaul SSL conext has more strict
   #connection handshaking rule. We may need turn of the hostname checking
   #and client side cert verification
   context = None
   if sys.version_info[:3] > (2,7,8):
      context = ssl.create_default_context()
      context.check_hostname = False
      context.verify_mode = ssl.CERT_NONE

   si = SmartConnect(host=args.host,
                     user=args.user,
                     pwd=password,
                     port=int(args.port),
                     sslContext=context)

   atexit.register(Disconnect, si)

   #for detecting whether the host is VC or ESXi
   aboutInfo = si.content.about


   if aboutInfo.apiType == 'VirtualCenter':
      majorApiVersion = aboutInfo.apiVersion.split('.')[0]
      if int(majorApiVersion) < 6:
         print('The Virtual Center with version %s (lower than 6.0) is not supported.'
               % aboutInfo.apiVersion)
         return -1

      #Here is an example of how to access VC side VSAN Health Service API
      vcMos = vsanapiutils.GetVsanVcMos(si._stub, context=context)

      # Instantiates an object of the class vsan-cluster-health-system
      vsanclusterconfig = vcMos['vsan-cluster-config-system']




   if aboutInfo.apiType == 'HostAgent':
      majorApiVersion = aboutInfo.apiVersion.split('.')[0]
      if int(majorApiVersion) < 6:
         print('The ESXi with version %s (lower than 6.0) is not supported.'
               % aboutInfo.apiVersion)
         return -1

      #Here is an example of how to access ESXi side VSAN Performance Service API
      esxMos = vsanapiutils.GetVsanEsxMos(si._stub, context=context)

      # Get vsan health system
      vpm = esxMos['vsan-performance-manager']

      nodeInfo = vpm.VsanPerfQueryNodeInformation()[0]


if __name__ == "__main__":
   main()



#todo fetch list of clusrter and add a selection

