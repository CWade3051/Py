#!/usr/bin/python
"""
 
    Description: osxautoruns.py - Lists applications set to auto-launch either during os startup or during login
    Platform:    Mac OS X, Python 2.x
    Copywrite:   (C)2010 Joel Yonts, Malicious Streams
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    See companion file, Licenses.txt, for a copy of the GNU General Public License
    or a copy is available at <http://www.gnu.org/licenses/>.
 
"""
__version__ = '0.6a'
 
import plistlib
import sys
import os
import operator
#import config
import Foundation
 
# Section: CONFIGURATION -------------------------------------------
PLIST_EXT=".plist"
USERDIR="/Users"
 
STARTUP_PLISTS=["/System/Library/LaunchDaemons",
                    "/Library/LaunchDaemons",
                    "/System/Library/LaunchAgents",
                    "/Library/LaunchAgents",
                    "/Library/StartupItems",
                    "/Library/Preferences/loginwindow.plist",
                    "~/Library/LaunchAgents",
                    "~/Library/Preferences/loginitems.plist",
                    "~/Library/Preferences/loginwindow.plist"]
 
LOGIN_PLIST="/Library/Preferences/loginwindow.plist"
 
USER_CONFIG_DIR="/private/var/db/dslocal/nodes/Default/users"
USER_DIR_BLACKLIST=["/var/empty", "/dev/null"]
USER_SHELL_BLACKLIST=["/usr/bin/false"]
 
# Section: PRIMARY CLASS DEFINITION -------------------------------------------
class AutoRuns:
     
    def __init__(self, verbose, user, mntPoint=""):
 
 
        self.target_user = user
                 
        if mntPoint == "":
            self.live_response = True
            print "Analysis Type: Live Analysis"
        else:
            self.live_response = False
            print "Analysis Type: Mounted System"
             
        if verbose == True:
            self.verbose = True
        else:
            self.verbose = False
         
        # Build Comphrensive List of Startup Plist Paths
        self.startup_plists =STARTUP_PLISTS
         
        # Retrieve Full User if using SUDO perms, otherwise just get current user
        self.user_list=self._getUserList(mntPoint)
             
        self._expandUserPaths(mntPoint)
        self._expandPlistDirs(mntPoint)
     
        self.startupItems=self._parsePlists()
 
        self.startup_plists.sort()
        self.startupItems.sort(key=operator.itemgetter('User'))
 
    def _userExists(self, username):
        """ Determines if a specified user exists on the system.
         
        @type raw_data: string
        @param row_data: Username to be checked for existence
         
        @return: boolean
        """
        userExists = False
         
        for user, homdir in self.user_list:
            if username == user:
                userExists =True
                 
        return userExists
     
    def _getCurrentUser(self):
        """ Return current user name and home directory
         
        @type raw_data: string
        @param row_data: Mountpoint (if any) for OS X image.  Default is /
         
        @return: list containing name,home directory for each valid user
        """
        try:
            logname = os.environ.get('LOGNAME')
            homedir = os.environ.get('HOME')
            return [[logname, homedir]]
        except:
            return []
     
    def _getUserList(self, mntPoint):
        """ Build a valid user list by reading configuration file(s).  
        Function also uses black lists to remove system accounts.
         
        @type raw_data: string
        @param row_data: Mountpoint (if any) for OS X image.  Default is /
         
        @return: list containing name,home directory for each valid user
        """
        error_state = False
        error_msgs =[]
 
        user_list =[]
        if mntPoint!= "" and mntPoint.endswith('/')==False:
            mntPoint=mntPoint+os.sep
             
        user_config_dir=mntPoint+USER_CONFIG_DIR
        if os.access(user_config_dir, os.R_OK)==True:
            for user_config in os.listdir(user_config_dir):
                 
                user_config_plist=self._readRawPlist(user_config_dir+os.sep+user_config)
                if user_config_plist != None:
                    #print user_config_plist
                    if user_config_plist.has_key("name") == True and user_config_plist.has_key("home") == True and user_config_plist.has_key("shell"):
                        username=user_config_plist['name'][0]
                        homedir=user_config_plist['home'][0]
                        shell=user_config_plist['shell'][0]
                        if USER_DIR_BLACKLIST.count(homedir)==0 and USER_SHELL_BLACKLIST.count(shell)==0:
                            user_list.append([username, homedir])
                else:
                    if self.verbose == True:
                        error_msgs.append("Error reading: %s%s%s" % (user_config_dir, os.sep, user_config))
                         
                    error_state = True
                     
        else:
            if self.verbose == True:
                error_msgs.append("Error accessing: "+str(user_config_dir))
                 
            error_state = True
                     
        if error_state == True and self.live_response == True:
            user_list =self._getCurrentUser()
            if user_list[0][0] != self.target_user:
                if self.verbose == True:
                    print "===> WARNING: Error accessing user configurations:"
                    for msg in error_msgs:
                        print "\t"+msg
                else:
                    print "===> WARNING: Error accessing user configurations (Use -V option for details)."      
                         
                print "===> WARNING: Only global (SYSTEM Level) and current user startup items will be displayed."
                print "===> WARNING: Use of elevated (SUDO) permissions may provide access to startup items for all users.\n\n"
                 
 
 
                     
        if error_state == True and self.live_response == False:
            if self.verbose == True:
                print "===> WARNING: Error accessing user configurations:"
                for msg in error_msgs:
                    print "\t"+msg
            else:
                print "===> WARNING: Error accessing user configurations (Use -V option for details)."  
            print "===> WARNING: Only global (SYSTEM Level) startup items will be displayed."
            print "===> WARNING: Use of elevated (SUDO) permissions may provide access to user startup items.\n\n"
 
        return user_list
         
        # --- Section: Parse Plists and Build Startup Items List -------
    def _OLD_readPlist(self, filename):  # Does not support binary plists
        """ Read and Parse the specified plist.  
        This function is currently not used because the libraries inability to deal with all plist types (Binary Plists).
         
        @type raw_data: string
        @param row_data: Full path to plist file
         
        @return: list containing plist data
        """
 
        plist=plistlib.readPlist(filename)
        return plist
     
    def _readRawPlist(self, plistFile):
        """ Read and Parse the specified plist file.  
        This function uses the Foundation class to achieve compatibility with all plist types (This does break cross-platform compatibility).
         
        @type raw_data: string
        @param row_data: Full path to plist file
         
        @return: dictionary containing plist data
        """
        # Use Foundation class to extract plist data (Foundation used instead of plistlib due to support for binary plists)
        plistNSData = Foundation.NSData.dataWithContentsOfFile_(plistFile)
        plistData, format, error = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistNSData, Foundation.NSPropertyListMutableContainersAndLeaves, None, None)
         
        return plistData
     
    def _parsePlists(self):
        """ Extract relevant plist fields from the internally built list of startup plists.  
        This function calls _readRawPlist to load plist data.
         
        @type raw_data: None
        @param row_data: None
         
        @return: dictionary containing startup items
        """
         
        startupItems =[]
        for user, plistName in self.startup_plists:
            pEntry ={}
            pEntry['User']=user
            pEntry['Fname']=plistName
            plistData = self._readRawPlist(plistName)
            #print plistData
             
            try:
                # Begin Label String
                if plistData.has_key("Label")==True:
                    pEntry["Label"]=plistData["Label"]
                # End Label String
             
                # Begin Program String
                progStr=""  
                if plistData.has_key("Program") == True:
                    progStr=str(plistData["Program"])
                         
                if plistData.has_key("ProgramArguments") == True:
                    # If program exists then eliminate the arg of ProgramArguments if it matches basename(Program)
                    for entry in plistData["ProgramArguments"]:
                        if os.path.basename(progStr) != entry: # Remove first program arg if already specified by "Program"
                            if len(progStr) > 0:
                                progStr=progStr+" "
 
                            progStr=progStr+str(entry)
 
                # This section is designed to support the alternate formate of the loginwindow.plist format.
                # This could have been handled more elegantly but would have forced a rewrite of several functions. 
                if plistName.endswith(LOGIN_PLIST):
                    if plistData.has_key("AutoLaunchedApplicationDictionary") == True:
                        for entry in plistData["AutoLaunchedApplicationDictionary"]:
                            pEntry["Program"]=entry["Path"]
                            pEntry["Disabled"]=False
                            startupItems.append(pEntry.copy())
 
                    pEntry=None
 
                else:
                    if len(progStr) >0:
                        pEntry["Program"]=progStr
                    # End Program String
                         
                    # Begin Disabled Status
                    if plistData.has_key("Disabled") == True:
                        pEntry["Disabled"]=plistData["Disabled"]
                    else:
                        pEntry["Disabled"]=False
                    # End Diabled Status    
 
            except:
                pEntry['Label'] = "ERROR"
                pEntry['Disabled'] = False
                pEntry['Program'] = "Error Parsing Plist(%s)" % (plistName)
             
            if pEntry != None:
                startupItems.append(pEntry)
             
        return startupItems
     
    # --- Section: Building List of Plists -------
    def _expandPlistDirs(self, mntPoint):
        """ Expand the plist entries to represent fullpaths to actual files.
        Startup plist configuration entries may contain a directory where plists can be found (/Library/LaunchDaemons) not full paths.
        This functions does the appropriate expansion to make the complete list.
         
        @type raw_data: string
        @param row_data: MointPoint (Default=/) of the OS X image to analyze
         
        @return: None, Updates internal startupitem list
        """
        expandedPaths=[]
 
        # Convert Plist Directories into Full Path of All Plists
        for user, plistPath in self.startup_plists:
            # Do not prepend only /, would result in a path starting with //
            if mntPoint == "/":
                mntPoint=""
                 
            plistPath=mntPoint+plistPath
         
            try:
                if os.path.isfile(plistPath) and plistPath.endswith(PLIST_EXT):
                    expandedPaths.append([user, plistPath])
                     
                elif os.path.isdir(plistPath):
                    for root, subFolders, files in os.walk(plistPath):
                        for file in files:
                            if file.endswith(PLIST_EXT):
                                fpath =os.path.join(root,file)
                                expandedPaths.append([user, fpath])
         
            except IOError:
                print "Error reading: "+ plistPath
                sys.exit(1)
                 
        self.startup_plists=expandedPaths
     
    def _expandUserPaths(self, mntPoint):
        """ Expand the plist entries to represent fullpaths to actual files.
        Startup plist configuration entries may use ~ short cuts to represent user directories.
        This functions does the appropriate substitutions and expansion to make the complete list.
         
        @type raw_data: string
        @param row_data: MointPoint (Default=/) of the OS X image to analyze
         
        @return: None, Updates internal startupitem list
        """
        listOfPlists =[]
         
        if mntPoint == "/":
            mntPoint=""
         
        userDirs = self.user_list
         
        for plistPath in self.startup_plists:
            if plistPath.startswith("~") == True:
                for user,homedir in userDirs:
                    listOfPlists.append([user, plistPath.replace("~", homedir)])
            else:
                listOfPlists.append(["SYSTEM", plistPath])
         
        self.startup_plists =listOfPlists   
 
    # ---- Section: UI & Formatting -------
    def _FormatedStartupItemsText(self, targetUser):
        """ Builds a text formatted list of startupitems for the specified user.
         
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
         
        @return: List containing formatted output
        """    
        rtnList =[]
 
        currentUser =""
        for cmd in self.getStartupItemsRaw(targetUser):
            if cmd.has_key('User') == True and cmd.has_key('Program') == True:
                if cmd['User'] != currentUser:
                    rtnList.append(cmd['User'])
                    currentUser = cmd['User']
                     
                cmdStr="\t"+cmd['Program']
                if cmd['Disabled'] == True:
                    cmdStr=cmdStr+"(Disabled)"
            else:
                cmdStr="\tError Reading Plist -- Fields 'User' and/or 'Program' does not exist\nEntry:" +str(cmd)
                 
            rtnList.append(cmdStr)
             
        return rtnList
     
    def _FormatedStartupListCSV(self, targetUser):  
        """ Builds a csv formatted list of startupitems for the specified user.
         
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
         
        @return: List containing formatted output
        """
        import csv
        import StringIO
         
        rtnList=StringIO.StringIO()
        startupItems = self.getStartupItemsRaw(targetUser)
 
        keys=startupItems[0].keys()
                 
        csvWriter = csv.DictWriter(rtnList, keys, restval="NO VALUE", delimiter=',', skipinitialspace=True, quotechar='\"', lineterminator="", quoting=csv.QUOTE_ALL)
 
        csvWriter.writerow(dict((nHeader,nHeader) for nHeader in keys))
         
        for entry in startupItems:
            csvWriter.writerow(entry)
             
        return rtnList.buflist
     
    # ---- Section: Public Accessor Functions -----
    def getStartupPlists(self, targetUser="ALL"):
        """ Return a text list of startup plists for the specified user.
        This information is a subset of the information return from startupItems.
         
        @type raw_data: string
        @param row_data: Only show startup plists related to specified user (Default is ALL)
         
        @return: List of text entries
        """
 
        rtnList =[]
         
        for owner, plist in self.startup_plists:
            if targetUser=='ALL' or owner == 'SYSTEM' or owner == targetUser:
                rtnList.append(plist)
                 
        return rtnList
 
     
    def getStartupCmds(self, user):
        """ Return a text list of startup commands for the specified user.
        This information is a subset of the information return from startupItems.
         
        @type raw_data: string
        @param row_data: Only show startup commands related to specified user (Default is ALL)
         
        @return: List of text entries
        """
        rtnList =[]
         
        for entry in self.getStartupItemsRaw(user):
            if entry.has_key('Program') == True:
                cmdStr=entry['Program']
                if entry.has_key('Disabled') == True and entry['Disabled'] == True:
                    cmdStr=cmdStr+" (Disabled)"
            else:
                cmdStr=str("Error Reading Plist -- Field 'Program' does not exist")
                 
            rtnList.append(cmdStr)
             
        return rtnList
     
    def getStartupItemsRaw(self, user="ALL"):
        """ Return a raw list of startupitems for the specified user.
         
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
         
        @return: List containing dictionary entries
        """
        rtnList = []
         
        if user=="ALL":
            return self.startupItems
        else:
            for entry in self.startupItems:
                if entry.has_key('User') == True:
                    if entry['User'] == 'SYSTEM' or entry['User'] == user:
                        rtnList.append(entry)
                else:
                    rtnList.append("Error Reading Plist -- Field 'User' does not exist")
                     
        return rtnList
             
    def getStartupItemsText(self, targetUser="ALL"):
        """ Return a text list of startupitems by called _FormatedStartupXXXX functions.
         
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
         
        @return: List containing text entries
        """
        itemList=self._FormatedStartupItemsText(targetUser)
        return itemList
     
    def getStartupItemsCSV(self, targetUser="ALL"):
        """ Return a csv list of startupitems by called _FormatedStartupXXXX functions.
         
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
         
        @return: List containing text entries
        """
        itemList =self._FormatedStartupListCSV(targetUser)  
        return itemList
     
    # --- Section: Output Methods
    def outputStartupList (self, format, targetUser="ALL", filename=None):
        """ Output the list of startup items.  Formatting & Output destination specified.
         
        @type raw_data: string
        @param row_data: Format to be used in generating output
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
        @type raw_data: string
        @param row_data: Output written to filename specified, None=stdout
         
        @return: None
        """
        if targetUser != "ALL" and targetUser != "System":
            if self._userExists(targetUser) == False:
                print "User: %s does not exist or incorrect permissions to access user information!\nPlease validate username and/or use elevated privileges" % (targetUser)
                sys.exit(1)
         
        if format == 'csv':
            itemList=self.getStartupItemsCSV(targetUser)
        elif format == 'raw':
            itemList=self.getStartupItemsRaw(targetUser)
        elif format == 'text':
            itemList=self.getStartupItemsText(targetUser)
        else:
            print "Invalid output format specified -o "+str(format)
            sys.exit(1)
             
        if filename == None:
            for entry in itemList:
                print entry
        else:
            try:
                fOut=open(filename, "w")
                for entry in itemList:
                    fOut.write(str(entry)+"\n")
                fOut.close()
            except:
                print "Error: Unable to write output to file -- "+str(filename)
                sys.exit(1)
                 
    def outputList (self, listType, targetUser="ALL", filename=None):
        """ Output the list of cmands or plists for a target user.  Formatting & Output destination specified.
         
        @type raw_data: string
        @param row_data: Format to be used in generating output
        @type raw_data: string
        @param row_data: Only show startup items related to specified user (Default is ALL)
        @type raw_data: string
        @param row_data: Output written to filename specified, None=stdout
         
        @return: None
        """
        if targetUser != "ALL" and targetUser != "System":
            if self._userExists(targetUser) == False:
                print "User: %s does not exist or incorrect permissions to access user information!\nPlease validate username and/or use elevated privileges" % (targetUser)
                sys.exit(1)
         
        if listType == 'plists':
            itemList =self.getStartupPlists(options.user)
             
        elif listType == 'cmds':
            itemList=self.getStartupCmds(options.user)
        else:
            print "Invalid List Type Specified: "+listType
            sys.exit(1)
             
        if filename == None:
            for entry in itemList:
                print entry
        else:
            try:
                fOut=open(filename, "w")
                for entry in itemList:
                    fOut.write(entry+"\n")
                fOut.close()
            except:
                print "Error: Unable to write output to file -- "+str(filename)
                sys.exit(1)
 
if __name__ == '__main__':
    import optparse
     
    usage = "usage: %prog -o <output type> [options]"
     
    parser = optparse.OptionParser()
    parser.set_usage(usage)
     
    parser.add_option("-o", "--output", dest="output",
                            help="Output format: csv, raw, text", metavar="<OUTPUT TYPE>", default=None)
     
    parser.add_option("-l", "--list", dest="list",
                            help="List supporting items: cmds, plists", metavar="<LIST TYPE>", default=None)
         
    parser.add_option("-m", "--mountpoint", dest="mountpoint",
                            help="Mac OS X Mount Point, Default = \"/\"", metavar="<MOUNT_POINT>", default="")
 
    parser.add_option("-f", "--file", dest="outfile",
                            help="Send output to specified file instead of stdout", metavar="<FILE>", default=None)
     
    parser.add_option("-u", "--user", dest="user",
                            help="Only show startup items for specified user (default = ALL)", metavar="<USERNAME>", default="ALL")
     
    parser.add_option("-V", "--verbose", action="store_true", dest="verbose",
                            help="Verbose Output", default=False)
     
    (options, args) = parser.parse_args()        
 
    if options.mountpoint != "":
        if os.path.exists(options.mountpoint) == False:
            print "Error invalid mount point: " + str(options.mountpoint)
            sys.exit(1)
 
    if options.list != None:
        aruns=AutoRuns(options.verbose, options.user, options.mountpoint)
        aruns.outputList(options.list, options.user, options.outfile)
 
    elif options.output != None:
        aruns=AutoRuns(options.verbose, options.user, options.mountpoint)
        aruns.outputStartupList(options.output, options.user, options.outfile)
 
    else:
        parser.print_help()
        print ""
        print "Usage Error -- Must specify output type"
        sys.exit(1)