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

from os import walk
from os.path import exists
from shutil import copyfile
from subprocess import call
import sys
import time
import hashlib
import datetime

#valid arguments that the program can take
VALID_ARGUMENTS = ("y","r","b","1","5","256","t","ext","log","robo","cp")
#flags for the arguments to set or unset
copyAll = False
replaceAll = False
back = False
sha_1 = False
md5 = False
sha_256 = False
timeStamp = False
extentionFilter = False
log = False
robo = True
cp = False
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
        
def getFolders():
    
    global source
    global dest

    #check the source and destination folders for validity and choose new targets in case of issue
    if exists(source):
        print("Source: " + source)
    else :
        print("Invalid source path")
        source =fileChooser()
    if exists(dest):
        print("Destination: " + dest)
    else :
        print("Invalid destination path")
        dest = fileChooser()

    #parseArgs()

def parseArgs():
    #check the remaining arguments and set them if they are in the list of arguments to be accepted
    for case in sys.argv:
        if case in VALID_ARGUMENTS:
            setArg(case)

def fileChooser():
    while True :
        f = input("Enter a filename: ")
        if exists(f) :
            if(input("Are you sure y/n: ").lower() == "y"):
                return f
    
def setArg(argument):

    global copyAll
    global md5
    global sha_1
    global sha_256
    global robo
    global back
    global replaceAll
    global timeStamp
    global cp
    global extentionFilter

    if argument.lower() == "y" : 
        copyAll = True
        print("CopyAll")
    if argument.lower() == "r" : 
        replaceAll = True
        print("ReplaceAll")
    if argument.lower() == "b" : 
        back = True
        print("Backup")
        time.sleep(3.0)
    if argument == "1" or argument == 1 :
        sha_1 = True
    if argument.lower() == "t" :
        timeStamp = True
    if argument.lower() == "5" or argument == 5 :
        md5 = True
    if argument.lower() == "256" or argument == 256 :
        sha_256 = True
    if argument.lower() == "ext" :
        extentionFilter = True
    if argument.lower() == "log" :
        log = True
    if argument.lower() == "robo" : 
        robo = True
    if argument.lower() == "cp" :
        cp = True

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

def backup(source = "", destination = "", name = ""):
    
    #Error checking to make sure the source/dest exists
    if not exists(source):
        source = fileChooser()
    if not exists(destination):
        destination = fileChooser()

    #if no name is passed in
    if name == "" :
        if input("Use {} as the default name for this backup?".format(str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop())).lower() == "y" :
            name = str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + source.rsplit("\\").pop()
        else:
            while True :
                name = input("Enter a backup name then: ")
                if input("are you sure?").lower() == "y":
                    break
                
    #create a archive file or a folder containing a copy of verything in the source
    print(name)

    #create the backup to the appropriate destination and folder name
    copyToMissingRobo(fileList(source),destination + "\\" + name)

    return True
    
def fileList(folderName):
    files = []
    for(dirpath, dirname, filenames) in walk(folderName) :
        for f in filenames:
            files.append((dirpath,f))
    return files

def menu():
    global source
    global dest
    global copyAll
    global md5
    global sha_1
    global sha_256
    global robo
    global back
    global replaceAll
    global timeStamp
    global cp
    global extentionFilter

    #check the flags to see if the menu is needed
    if back == True:
        print("whaddup")
        backup(source,dest,"asdffg")
        input("hello?")
        return True


    #parseArgs()
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
            if(input("Are You Sure?").lower()=="y"):
                #add the call to replace all files here
                return True
                
        #must not be a real option so grab input again
        choice = input("Enter a number please: ")
    
def main():
    global source
    global dest
    global back
    #check the arguments for switch cases 
    #sha_1("C:\\Users\\meatw\\Desktop\\school\\PONG\\ball.cpp")
    parseArgs()

    if back == True :
        print("shiiiiz")

    if len(sys.argv) == 1: #no arguments passed to the program
        menu()
    elif len(sys.argv >=2 and exists(sys.argv[1]) and not exists(sys.argv[2])): #only source given
        getFolders()
        menu()
    elif len(sys.argv >= 3 and exists(sys.argv[1]) and exists(sys.argv[2])):#source and destination given and acceptable
        source = sys.argv[1]
        dest = sys.argv[2]
        menu()
    else:#either the source and dest are not valid 
        getFolders()
        menu()
    return True
    #copyToMissing(missingFilesList(source, dest), dest)
    #add some form of flag checking to call appropriate flags
if __name__ == "__main__":
    main()
