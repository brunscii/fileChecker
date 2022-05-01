'''Author: Chris Carlin

ToDo:

>fix the double menu with no source and destination - return true after
>check if only source and no destination and check for appropriate flags (1,5,256,t,log)
>add a logging feature
>add a way to read the logs for a resume feature
>add a check in the menu for after the copy type is entered
>
    

'''

from os import chdir, walk
import os
from os.path import exists
from pathlib import Path
import shutil
from subprocess import call
from argparse import ArgumentParser
import sys
import time
import hashlib
import datetime


parser = ArgumentParser(description='Fancy Copy and Paste')
copyType = parser.add_mutually_exclusive_group()
hashCheckType = parser.add_mutually_exclusive_group()

parser.add_argument('source',type=str,nargs='?',help='the source of the operation')
parser.add_argument('destination',type=str,nargs='?',help='the destination of the operation')
parser.add_argument('-t',"--t",action = "store_true",help = "timestamps all of the files in the destination to show they are up to date after the backup")
parser.add_argument('-ext',"--ext",type = str,action = "append",nargs = '+',help = "filters an extention type(s) to be copied from the source to the destination")
parser.add_argument('-log',"--log",type=str,action = "append",nargs='+',help = "create a log file for the copies or a list of files missing in case of the nocopy command")
 
copyType.add_argument('-cp',"--cp",action = "store_true",help = "copy the file using the command lines cp command")
copyType.add_argument('-r','--r',action = "store_true",help = "replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!")
copyType.add_argument('-b',"--b",action = "store_true",help = "backup by creating a folder with a copy of the source in the new source folder")
copyType.add_argument('-robo',"--robo",action = "store_true",help = "copy the file using the command lines robo command")
copyType.add_argument('-n',"--nocopy",action = "store_true",help = "just make a list of missing files")
copyType.add_argument('-a', '--a',action='store_true',help='creates a zip file of the source folder')

hashCheckType.add_argument('-1',"--sha1",action = "store_true",help = "uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
hashCheckType.add_argument('-5',"--md5",action = "store_true",help = "uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files")
hashCheckType.add_argument('-256',"--sha256",action = "store_true",help = "uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")

source='asdf'
dest = "asdf"

#checks path1 against path2 for missing files in path2 that exist in path1
#returns missing files in format of (dir,file)
def missingFilesList(path1, path2):
    missingFiles = []
    if not exists(path1):
        path1 = fileChooser("Enter a source: ")
        global source
        source = path1
    if not exists(path2):
        path2 = fileChooser("Enter a destination: ")
        global dest
        dest = path2
    if exists(path1) and exists(path2) :
        print(path1)

        print(path2)

        f1 = []
        for(dirpath, dirnames, filenames) in walk(path1):
            for name in filenames:
                f1.append((dirpath,name))
        f2 = []
        for(dirpath, dirnames, filenames) in walk(path2):
            for name in filenames:
                f2.append((dirpath,name))

        for (dirPath1, fileName1) in f1:
            found = False
            for (dirPath2, fileName2) in f2:
                if fileName1 == fileName2:
                    found = True
            if found == False:
                missingFiles.append((dirPath1,fileName1))
   
    return missingFiles

#This is a function to copy the missing files to the destination
def copyToMissingRobo(files, dest):
    for (dir, fileName) in files:
        #time.sleep(2.5)
        call(["robocopy", dir, dest, fileName])
        
def getFolders(s,d):
    
    global source
    global dest

    #check the source and destination folders for validity and choose new targets in case of issue
    if exists(s):
        print("Source: " + s)
        source = s
    else :
        print("{}is an invalid source path".format(s))
        source =fileChooser("Enter a source: ")
    if exists(d):
        print("Destination: " + d)
        dest = d
    else :
        print("{} is an invalid destination path".format(d))
        dest = fileChooser("Enter a destination: ")

def fileChooser(msg='Enter a filename: '):
    while True :
        f = input(msg)
        if exists(f) :
            if(input("Are you sure y/n: ").lower() == "y"):
                return f
    
def sha_1(filename) :
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha1.update(data)
    return sha1.hexdigest()

def md5(filename) :
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            md5.update(data)
    print("MD5: {0}".format(md5.hexdigest()))
    time.sleep(5.0)
    return md5.hexdigest()

def sha_256(filename) :
    sha256 = hashlib.sha256()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha256.update(data)
    print("SHA256: {0}".format(sha256.hexdigest()))
    time.sleep(5.0)
    return sha256.hexdigest()

def extFilter(src,names):
    return names

def backup(s = "", destination = "", name = "",copyVer='default',hashCheck='none',options=[]):
    
    global source
    global dest
    
    #Error checking to make sure the source/dest exists
    getFolders(s,destination)
    
    #if no name is passed in
    if name == "" :
        if input("Use {} as the default name for this backup?".format(str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop())).lower() == "y" :
            name = str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop()
        else:
            while True :
                name = input("Enter a backup name then: ")
                x = input("are you sure?").lower()
                if x == "y":
                    break
                
    #create a archive file or a folder containing a copy of verything in the source
    print(name)
    #use the copytree as default
    if copyVer=='default':      
        print('default:\n')
        try :
            shutil.copytree(src=source,dst=os.path.join(dest,name))
        except FileExistsError:
            print("Backup name already exists\n")
            backup(source,dest)
    #nocopy command
    elif copyVer == 'nocopy':   
        print('nocopy:\n')
        filePrint = lambda path,file: print(os.path.join(path,file))
        for (p,f) in missingFilesList(source,dest):
            filePrint(p,f)
    #backup protocol
    elif copyVer == 'backup':   
        try :
            shutil.copytree(src=source,dst=os.path.join(dest,name))
        except FileExistsError:
            print("Backup name already exists\n")
            backup(source,dest)
    #archive by creating a zip
    elif copyVer == 'archive':  
        try :
            chdir(dest)
            #shutil.ignore_patterns()
            print(shutil.make_archive(base_name=name,root_dir=dest,base_dir=source,format='zip'))
            input("Press any key...")
        except FileExistsError:
            print("archive name already exists\n")
            backup(source,dest)
    #robocopy
    elif copyVer == 'robo':
        copyToMissingRobo(missingFilesList(source,dest),dest)
    return True
 
def fileList(folderName):
    files = []
    for(dirpath, dirname, filenames) in walk(folderName) :
        for f in filenames:
            files.append((dirpath,f))
    return files

def menu():

    print("# | Option \n" +
              "=====================\n" +
              "1.| MD5 hash of a file \n" +
              "2.| SHA1 hash of a file \n" +
              "3.| SHA256 hash of a file\n" +
              "4.| backup to a folder and create new copies of the files in the destination folder \n" +
              "5.| replace all files in a folder with those from a source\n" +
              "6.| timestamp all of the files in a directory\n")

    choice = input("Enter a number: ")
    #add a loop that repeats and asks for input if not given a number between 1-5 and 0 to exit
    #filter the input for the menu

    while True : #option catcher
        if choice == "0" :
            return False
        if choice == "1" : #md5 option
            print(md5(fileChooser()))
            time.sleep(15)
            return True
        if choice == "2" : #sha1 option
            print(sha_1(fileChooser()))
            time.sleep(15)
            return True
        if choice == "3" : #sha256 option
            print("Working on it")
            time.sleep(5)
            return True
        if choice == "4" : #backup option
            print("working on it --- new features warning")
            backup(source,dest)
            return True
        if choice == "5" : #replace all option
            print("This will replace all files in the destination.\nAre you sure this is what you want?")
            archive(source,dest)
                #add the call to replace all files here
            return True
        if choice == "6" : #timestamp the destination folder
            timeStamp(dest)
            return True
        #must not be a real option so grab input again
        choice = input("Enter a number please: ")
        
#time stamps all of the files and folders in a directory
def timeStamp(destination):
    if exists(destination):        
        for path,file in fileList(destination):
            Path(path).touch()
            Path(os.path.join(path,file)).touch()
    else:
        timeStamp(fileChooser('Enter a destination: '))
    return True

def main():
    global source
    global dest
    global parser
    
    args = parser.parse_args()
    if args.source:
        if exists(args.source):
            source = args.source
        else:
            source=fileChooser("Enter a source name: ")
    else:
        menu()
        return True
        
    if args.destination: #means we had a source that was valid or attempted and a destination that was entered
        if exists(args.destination):
            dest = args.destination
        else:      
            dest=fileChooser("Enter a destination name: ")
    else: #no destination entered - Check for single file flags and if none then 
        if args.sha1:
            if os.path.isdir(source):
                for dir,filename in fileList(source):
                    fname = os.path.join(dir,filename).format("%-20s",)
                    s1 = sha_1(os.path.join(dir,filename))
                    print(f"{fname : <10} SHA1: {s1}")
                input("....")
            else:
                print(sha_1(source))
                input("....")

    if args.b:
        print("Backup mode initialized:\n")
        backup(source,dest,copyVer='backup')
        #return True
    if args.a:
        print("Archive mode initialized:\n")
        backup(source,dest,copyVer='archive')
        #return True
    if args.nocopy:
        backup(source,dest,copyVer='nocopy',name='none')
    if args.t :
        timeStamp(dest)
    if len(source) == 0: #no arguments passed to the program
        menu()
    
    return True
    #copyToMissing(missingFilesList(source, dest), dest)
    #add some form of flag checking to call appropriate flags
if __name__ == "__main__":
    main()
