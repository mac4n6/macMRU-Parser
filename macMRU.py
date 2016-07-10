#!/usr/bin/python
'''
Copyright (c) 2016, Station X Labs, LLC
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Station X Labs, LLC nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL STATION  X LABS, LLC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import ccl_bplist
from time import localtime, gmtime, strftime
import binascii
import sys
import hexdump
import argparse
from argparse import RawTextHelpFormatter
import os
import fnmatch

def ParseSFL(MRUFile):
    
    plistfile = open(MRUFile, "rb")
    plist = ccl_bplist.load(plistfile)
    plist_objects = ccl_bplist.deserialise_NsKeyedArchiver(plist, parse_whole_structure=True)

    if plist_objects["root"]["NS.objects"][1]["NS.keys"][0] == "com.apple.LSSharedFileList.MaxAmount":
        numberOfItems = plist_objects["root"]["NS.objects"][1]["NS.objects"][0]
        print "Max number of recent items in this plist: " + str(numberOfItems)

    if plist_objects["root"]["NS.keys"][2] == "items":
        items = plist_objects["root"]["NS.objects"][2]["NS.objects"] 
        for n,item in enumerate(items):
            print"    [Item Number: " + str(n) +  " | Order: " + str(item["order"]) + "] Name:'" + item["name"] + "' (URL:'" + item["URL"]['NS.relative'] + "'')"
            
            #UNCOMMENT FOR UNIQUE IDENTIFIER HEXDUMP
            #print "----------------------------------------------------------------------------"
            #print "Hexdump of Unique Identifier: "
            #print hexdump.hexdump(item["uniqueIdentifier"]["NS.uuidbytes"])
            #print "----------------------------------------------------------------------------"

            if args.blob == True:
                print "----------------------------------------------------------------------------"
                print "Hexdump of Bookmark BLOB: "
                hexdump_blob =  hexdump.hexdump(item["bookmark"])
                print hexdump_blob
                print "----------------------------------------------------------------------------"

def ParseLSShardFileListPlist(MRUFile):

    plistfile = open(MRUFile, "rb")
    plist = ccl_bplist.load(plistfile)

    print "Max number of recent items in this plist:: " + str(plist["RecentDocuments"]["MaxAmount"])
    print "[MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["RecentDocuments"]["CustomListItems"]):
        print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
        
        if args.blob == True:
            print "----------------------------------------------------------------------------"
            print "Hexdump of Bookmark BLOB: "
            print hexdump.hexdump(item["Bookmark"])
            print "----------------------------------------------------------------------------"
        
def ParseRecentItemsPlist(MRUFile):

    plistfile = open(MRUFile, "rb")
    plist = ccl_bplist.load(plistfile)

    print "Recent Applications (Max number of recent items in this key: " + str(plist["RecentApplications"]["MaxAmount"]) + ")"
    print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["RecentApplications"]["CustomListItems"]):
        print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
        if args.blob == True:
            print "----------------------------------------------------------------------------"
            print "Hexdump of Bookmark BLOB: "
            print hexdump.hexdump(item["Bookmark"])
            print "----------------------------------------------------------------------------"
        
    print "Recent Documents (Max number of recent items in this key: " + str(plist["RecentDocuments"]["MaxAmount"]) + ")"
    print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["RecentDocuments"]["CustomListItems"]):
        print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
        if args.blob == True:
            print "----------------------------------------------------------------------------"
            print "Hexdump of Bookmark BLOB: "
            print hexdump.hexdump(item["Bookmark"])
            print "----------------------------------------------------------------------------"
    
    print "Recent Servers (Max number of recent items in this key: " + str(plist["RecentServers"]["MaxAmount"]) + ")"   
    print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["RecentServers"]["CustomListItems"]):
        print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
        if args.blob == True:
            print "----------------------------------------------------------------------------"
            print "Hexdump of Bookmark BLOB: "
            print hexdump.hexdump(item["Bookmark"])
            print "----------------------------------------------------------------------------"
        
    print "Recent Hosts (Max number of recent items in this key: " + str(plist["Hosts"]["MaxAmount"]) + ")"   
    print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["Hosts"]["CustomListItems"]):
        print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'" + " - URL: " + item["URL"] + "'"

def ParseFinderPlist(MRUFile):
    plistfile = open(MRUFile, "rb")
    plist = ccl_bplist.load(plistfile)

    print "[MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
    for n,item in enumerate(plist["FXRecentFolders"]):
        print "    [Item Number: " + str(n) + "] '" + item["name"] + "'"
        
        if args.blob == True:
            print "----------------------------------------------------------------------------"
            print "Hexdump of Bookmark BLOB: "
            print hexdump.hexdump(item["file-bookmark"])
            print "----------------------------------------------------------------------------"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='\
    Parse the Mac MRU (Most Recently Used) Plist Files \
    \n\n\tMac MRU File Locations: \
    \n\t- /Users/<username>/Library/Preferences/<bundle_id>.LSShardFileList.plist\
    \n\t- /Users/<username>/Library/Preferences/com.apple.finder.plist\
    \n\t- [10.10-] /Users/<username>/Library/Preferences/com.apple.recentitems.plist\
    \n\t- [10.11+] /Users/<username>/Library/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments/<bundle_id>.sfl\
    \n\t- [10.11+] /Users/<username>/Library/Library/Application Support/com.apple.sharedfilelist/RecentApplications.sfl\
    \n\t- [10.11+] /Users/<username>/Library/Library/Application Support/com.apple.sharedfilelist/RecentDocuments.sfl\
    \n\t- [10.11+] /Users/<username>/Library/Library/Application Support/com.apple.sharedfilelist/RecentServers.sfl\
    \n\t- [10.11+] /Users/<username>/Library/Library/Application Support/com.apple.sharedfilelist/RecentHosts.sfl\
    \n \
    \n\tVersion: 1.0\
    \n\tUpdated: 07/10/2016\
    \n\tAuthor: Sarah Edwards | @iamevltwin | mac4n6.com | oompa@csh.rit.edu\
    \n\
    \n\tDependencies:\
    \n\t\thexdump.py: https://pypi.python.org/pypi/hexdump\
    \n\t\tccl_bplist.py: https://github.com/cclgroupltd/ccl-bplist'
        , prog='macMRU.py'
        , formatter_class=RawTextHelpFormatter)
    parser.add_argument('--blob', action='store_true', help="Include hex dump of Bookmark BLOBs in standard output")
    parser.add_argument('MRU_DIR')
    args = parser.parse_args()

    MRUDirectory = args.MRU_DIR

    print "###### MacMRU Parser v1.0 ######"

    for root, dirs, filenames in os.walk(MRUDirectory):
        for f in filenames:
            try: 
                if f.endswith(".sfl") and not fnmatch.fnmatch(f,'*Favorite*.sfl') and not fnmatch.fnmatch(f,'*Project*.sfl')  :
                    MRUFile = os.path.join(root,f)
                    print "=============================================================================="
                    print "Parsing: " + MRUFile
                    ParseSFL(MRUFile)
                    print "=============================================================================="
                elif f.endswith(".LSSharedFileList.plist"):
                    MRUFile = os.path.join(root,f)
                    print "=============================================================================="
                    print "Parsing: " + MRUFile
                    ParseLSShardFileListPlist(MRUFile)
                    print "=============================================================================="
                elif f == "com.apple.finder.plist":
                    MRUFile = os.path.join(root,f)
                    print "=============================================================================="
                    print "Parsing: " + MRUFile
                    ParseFinderPlist(MRUFile)
                    print "=============================================================================="
                elif f == "com.apple.recentitems.plist":
                    MRUFile = os.path.join(root,f)
                    print "=============================================================================="
                    print "Parsing: " + MRUFile
                    ParseRecentItemsPlist(MRUFile)
                    print "=============================================================================="
            except:
                pass