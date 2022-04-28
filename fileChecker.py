'''Author: Chris Carlin

To do: 
> add a MD5/SHA-1 hash checker to see if the copied files are the same file or to see if the files are the same before coppying
> add persistence through a temp file that shows the files being copied and that has been copied in case of unexpected shutdowns
> show the persistence file that will show any possibly uncoipied files and ask if you want to proceed on run...possibly a status run
> add multi threading to copy multiple files at a time
> add a user interface that shows the file changes in a git type of way
> add some kind of a service based automation to perform scheduled backups
> display the list of files that are going to be copied and ask permissions, maybe do a -y type of system
> add the ability to copy files in linux or windows by choosing the copy method
> add a option switch that will allow future expandability
    -y yes copy all of the files on ask pronpt
    -r replace the files that are in the destination with the current files from source
    -b backup the source to the destination by creating a copy folder that will be named <source-date>
    -1 do a SHA-1 checksum to determine if the files in the source are the same as in the destination
    -5 do a MD5 checksum to detiermine if the files in the source are the same as in the destination
    -256 do a SHA-256 checksum to determine if the files in the source are the same as in the destination
    -t time stamp everthing in the destination to show that it is up to date --touch
    -ext only copy files of a certain extention type
    -log log status messages into a log file with name <source-dest-date>
    -robo use robocopy
    -cp us cp
    

'''

import argparse
from io import DEFAULT_BUFFER_SIZE
from os import chdir, walk
from os.path import exists
import shutil
from subprocess import call
from argparse import ArgumentParser
import sys
import time
import hashlib
import datetime


parser = ArgumentParser()
parser.add_argument('names',nargs='*')
parser.add_argument('-cp',"--cp",action = "store_true",help = "copy the file using the command lines cp command")
parser.add_argument('-r','--r',action = "store_true",help = "replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!")
parser.add_argument('-b',"--b",action = "store_true",help = "backup by creating a folder with a copy of the source in the new source folder")
parser.add_argument('-1',"--1",action = "store_true",help = "uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
parser.add_argument('-5',"--5",action = "store_true",help = "uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files")
parser.add_argument('-256',"--256",action = "store_true",help = "uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
parser.add_argument('-t',"--t",action = "store_true",help = "timestamps all of the files in the destination to show they are up to date after the backup")
parser.add_argument('-ext',"--ext",type = str,action = "append",nargs = '+',help = "filters an extention type(s) to be copied from the source to the destination")
parser.add_argument('-log',"--log",type=str,action = "append",nargs='+',help = "create a log file for the copies or a list of files missing in case of the nocopy command")
parser.add_argument('-robo',"--robo",action = "store_true",help = "copy the file using the command lines robo command")
parser.add_argument('-nocopy',"--nocopy",action = "store_true",help = "just make a list of missing files")
parser.add_argument('-a', '--a',action='store_true',help='creates a zip file of the source folder')


source = "asdf"
dest = "asdf"

#checks path1 against path2 for missing files in path2 that exist in path1
#returns missing files in format of (dir,file)
def missingFilesList(path1, path2):
    missingFiles = []
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

    #parseArgs()

def fileChooser(msg):
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
    print("SHA1: {0}".format(sha1.hexdigest()))
    time.sleep(5.0)
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

def backup(s = "", destination = "", name = ""):
    
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
                elif x =="exit":
                    return False
                
    #create a archive file or a folder containing a copy of verything in the source
    print(name)
    
    #create the backup to the appropriate destination and folder name
    
    try :
        shutil.copytree(src=source,dst=(dest+'\\'+name))
    except FileExistsError:
        print("Backup name already exists\n")
        backup(source,dest)


    return True
 
def archive(s = "", destination = "", name = "",filt = False):
    
    global source
    global dest
    global parser
    args = parser.parse_args()
    #Error checking to make sure the source/dest exists
    getFolders(s,destination)
    
    #if no name is passed in
    if name == "" :
        if input("Use {} as the default name for this archive?".format(str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop())).lower() == "y" :
            name = str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop()
        else:
            while True :
                name = input("Enter a backup name then: ")
                x = input("are you sure?").lower()
                if x == "y":
                    break
                elif x =="exit":
                    return False
                
    #create a archive file or a folder containing a copy of verything in the source
    print(name)
    
    #create the backup to the appropriate destination and folder name
    filts = []
    if filt:
        for e in args.ext:
            filts.append('.'+e)

    try :
        chdir(dest)
        #shutil.ignore_patterns()
        print(shutil.make_archive(base_name=name,root_dir=dest,base_dir=source,format='zip'))
        input("Press any key...")
    except FileExistsError:
        print("archive name already exists\n")
        backup(source,dest)


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
              "5.| replace all files in a folder with those from a source")

    choice = input("Enter a number: ")
    #add a loop that repeats and asks for input if not given a number between 1-5 and 0 to exit
    #filter the input for the menu

    while True :
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
                
        #must not be a real option so grab input again
        choice = input("Enter a number please: ")
    
def timeStamp(destination):
    
    return True
    #add code to run touch on all of the files in the destination folder

def main():
    global source
    global dest
    
    #check the arguments for switch cases 
    #sha_1("C:\\Users\\meatw\\Desktop\\school\\PONG\\ball.cpp")
    global parser
    exFilter = False
    args = parser.parse_args()
    
    if len(args.names)>=2:
        if exists(args.names[0]):
            source = args.names[0]
        elif not source:
            source=fileChooser("Enter a source name: ")
        if exists(args.names[1]):
            dest = args.names[1]
        elif not dest:
            dest=fileChooser("Enter a destination name: ")
    elif len(args.names) == 1:
        if exists(args.names[0]):
            source = args.names[0]


    '''if args.ext:
        exFilter = True
        for i in args.ext : 
            print(i)
        input("ASDASDASDASD")'''
    if args.b == True :
        print("Backup mode initialized:\n")
        backup(source,dest)
        return True
    if args.a == True :
        print("Archive mode initialized:\n")
        archive(source,dest,exFilter)
        return True
    
    if len(args.names) == 0: #no arguments passed to the program
        menu()
    
    return True
    #copyToMissing(missingFilesList(source, dest), dest)
    #add some form of flag checking to call appropriate flags
if __name__ == "__main__":
    main()
