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
from time import gmtime, strftime
import sys
import hexdump
import argparse
from argparse import RawTextHelpFormatter
import os
import fnmatch
import plistlib

def ParseSFL(MRUFile):
    
    try:
        plistfile = open(MRUFile, "rb")
        plist = ccl_bplist.load(plistfile)
        plist_objects = ccl_bplist.deserialise_NsKeyedArchiver(plist, parse_whole_structure=True)

        if plist_objects["root"]["NS.objects"][1]["NS.keys"][0] == "com.apple.LSSharedFileList.MaxAmount":
            numberOfItems = plist_objects["root"]["NS.objects"][1]["NS.objects"][0]
            print "Max number of recent items in this plist: " + str(numberOfItems)

        if plist_objects["root"]["NS.keys"][2] == "items":
            items = plist_objects["root"]["NS.objects"][2]["NS.objects"] 
            for n,item in enumerate(items):
                try:
                    name = item["name"]
                except:
                    name = "No 'name' Key"

                print"    [Item Number: " + str(n) +  " | Order: " + str(item["order"]) + "] Name:'" + name + "' (URL:'" + item["URL"]['NS.relative'] + "'')"
                
                #UNCOMMENT FOR UNIQUE IDENTIFIER HEXDUMP
                #print "----------------------------------------------------------------------------"
                #print "Hexdump of Unique Identifier: "
                #print hexdump.hexdump(item["uniqueIdentifier"]["NS.uuidbytes"])
                #print "----------------------------------------------------------------------------"
                if args.blob == True:
                    try:
                        print "----------------------------------------------------------------------------"
                        print "Hexdump of Bookmark BLOB: "
                        hexdump_blob =  hexdump.hexdump(item["bookmark"])
                        print hexdump_blob
                        print "----------------------------------------------------------------------------"
                    except:
                        print "No 'bookmark' Key"
    except:
        print "Cannot open file: " + MRUFile
    
def ParseLSShardFileListPlist(MRUFile):
    try:
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
    except:
        print "Cannot open file: " + MRUFile
     
def ParseRecentItemsPlist(MRUFile):

    try:
        plistfile = open(MRUFile, "rb")
        plist = ccl_bplist.load(plistfile)
        try:
            print "Recent Applications (Max number of recent items in this key: " + str(plist["RecentApplications"]["MaxAmount"]) + ")"
            print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
            for n,item in enumerate(plist["RecentApplications"]["CustomListItems"]):
                print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
                if args.blob == True:
                    print "----------------------------------------------------------------------------"
                    print "Hexdump of Bookmark BLOB: "
                    print hexdump.hexdump(item["Bookmark"])
                    print "----------------------------------------------------------------------------"
        except:
            print "No Recent Applications"
            
        try:
            print "Recent Documents (Max number of recent items in this key: " + str(plist["RecentDocuments"]["MaxAmount"]) + ")"
            print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
            for n,item in enumerate(plist["RecentDocuments"]["CustomListItems"]):
                print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
                if args.blob == True:
                    print "----------------------------------------------------------------------------"
                    print "Hexdump of Bookmark BLOB: "
                    print hexdump.hexdump(item["Bookmark"])
                    print "----------------------------------------------------------------------------"
        except:
            print "No Recent Documents"
        
        try:
            print "Recent Servers (Max number of recent items in this key: " + str(plist["RecentServers"]["MaxAmount"]) + ")"   
            print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
            for n,item in enumerate(plist["RecentServers"]["CustomListItems"]):
                print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'"
                if args.blob == True:
                    print "----------------------------------------------------------------------------"
                    print "Hexdump of Bookmark BLOB: "
                    print hexdump.hexdump(item["Bookmark"])
                    print "----------------------------------------------------------------------------"
        except:
            print 'No Recent Servers'

        try:    
            print "Recent Hosts (Max number of recent items in this key: " + str(plist["Hosts"]["MaxAmount"]) + ")"   
            print "MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
            for n,item in enumerate(plist["Hosts"]["CustomListItems"]):
                print "    [Item Number: " + str(n) + "] '" + item["Name"] + "'" + " - URL: " + item["URL"] + "'"
        except:
            print "No Recent Hosts"
    except:
        print "Cannot open file: " + MRUFile
    
def ParseFinderPlist(MRUFile):

    try:
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
    except:
        print "Cannot open file: " + MRUFile

def ParseMSOffice2016Plist(MRUFile):

    try:
        plistfile = plistlib.readPlist(MRUFile)
            #print "[MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"
        for n,item in enumerate(plistfile):
            print "    [Item: " + item + "]"
            try:
                print "        UUID: " + plistfile[item]["kUUIDKey"]
            except:
                print "        UUID: No 'kUUIDKey' Key"

            if args.blob == True:

                print "----------------------------------------------------------------------------"
                print "Hexdump of Bookmark BLOB: "
                bookmarkdata = plistfile[item]["kBookmarkDataKey"]
                for attr, value in bookmarkdata.__dict__.iteritems():
                    print hexdump.hexdump(value)
                    print "----------------------------------------------------------------------------"
    except:
        print "Cannot open file: " + MRUFile

def ParseMSOffice2011Plist(MRUFile):

    try:
        plistfile = open(MRUFile, "rb")
        plist = ccl_bplist.load(plistfile)

        print "[MRUs are listed from Newest to Oldest (ie: Item 0 - Item 9)]"

        def FunkyMSTime(raw_accessdate):
            global accessdate
            thebytes = raw_accessdate.encode("hex")[4:12]
            macosts =  int("".join(reversed([thebytes[i:i+2] for i in range(0, len(thebytes), 2)])),16)
            epochtime = gmtime(macosts - 2082844800)
            accessdate = strftime("%m-%d-%Y %H:%M:%S", epochtime)

        print "Microsoft Word MRUs:"
        for n,item in enumerate(plist["14\File MRU\MSWD"]):

            raw_accessdate = item["Access Date"]
            FunkyMSTime(raw_accessdate)

            print "    [Item Number: " + str(n) + "] - Access Date(UTC): " + accessdate + ""

            if args.blob == True:
                print "----------------------------------------------------------------------------"
                print "Hexdump of File Alias BLOB: "
                print hexdump.hexdump(item["File Alias"])
                print "----------------------------------------------------------------------------"   
                
        print "Microsoft Excel MRUs:"
        for n,item in enumerate(plist["14\File MRU\XCEL"]):

            raw_accessdate = item["Access Date"]
            FunkyMSTime(raw_accessdate)

            print "    [Item Number: " + str(n) + "] - Access Date(UTC): " + accessdate + ""

            if args.blob == True:

                print "----------------------------------------------------------------------------"
                print "Hexdump of File Alias BLOB: "
                print hexdump.hexdump(item["File Alias"])
                print "----------------------------------------------------------------------------" 

        print "Microsoft Powerpoint MRUs:"
        for n,item in enumerate(plist["14\File MRU\PPT3"]):

            raw_accessdate = item["Access Date"]
            FunkyMSTime(raw_accessdate)

            print "    [Item Number: " + str(n) + "] - Access Date(UTC): " + accessdate + ""

            if args.blob == True:

                print "----------------------------------------------------------------------------"
                print "Hexdump of File Alias BLOB: "
                print hexdump.hexdump(item["File Alias"])
                print "----------------------------------------------------------------------------"
    except:
        print "Cannot open file: " + MRUFile 

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
    \n\t- MS Office 2011 - /Users/<username>/Library/Preferences/com.microsoft.office.plist\
    \n\t- MS Office 2016 - /Users/<username>/Library/Containers/com.microsoft.<app>/Data/Library/Preferences/com.microsoft.<app>.securebookmarks.plist \
    \n \
    \n\tVersion: 1.1\
    \n\tUpdated: 08/15/2016\
    \n\tAuthor: Sarah Edwards | @iamevltwin | mac4n6.com | oompa@csh.rit.edu\
    \n\
    \n\tDependencies:\
    \n\t\thexdump.py: https://pypi.python.org/pypi/hexdump\
    \n\t\tccl_bplist.py: https://github.com/cclgroupltd/ccl-bplist'
        , prog='macMRU.py'
        , formatter_class=RawTextHelpFormatter)
    parser.add_argument('--blob', action='store_true', help="Include hex dump of Bookmark BLOBs in standard output (can very ver")
    parser.add_argument('MRU_DIR')
    args = parser.parse_args()

    MRUDirectory = args.MRU_DIR

    print "###### MacMRU Parser v1.1 ######"

    for root, dirs, filenames in os.walk(MRUDirectory):
        for f in filenames:
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
            elif f.endswith(".securebookmarks.plist"):
                MRUFile = os.path.join(root,f)
                print "=============================================================================="
                print "Parsing: " + MRUFile
                ParseMSOffice2016Plist(MRUFile)
                print "==============================================================================" 
            elif f == "com.microsoft.office.plist":
                MRUFile = os.path.join(root,f)
                print "=============================================================================="
                print "Parsing: " + MRUFile
                ParseMSOffice2011Plist(MRUFile)
                print "=============================================================================="