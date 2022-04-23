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

#valid arguments that the program can take
VALID_ARGUMENTS = ("y","r","b","1","5","256","t","ext","log","robo","cp")
#flags for the arguments to set or unset
copyAll = False
replaceAll = False
backup = False
sha_1 = False
md5 = False
sha_256 = False
timeStamp = False
extentionFilter = False
log = False
robo = True
cp = False
source = " \asdf"
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
def copyToMissing(files, dest):
    for (dir, fileName) in files:
        time.sleep(2.5)
        call(["robocopy", dir, dest, fileName])
        

#check the arguments in argv to make sure they are valid and return a count
def parseArg():
    
    global source
    global dest

    #check if there is enough arguments to assume the source and destination files to be checked later
    if len(sys.argv) >= 3 :
        source = sys.argv[1]
        dest = sys.argv[2]
    elif len(sys.argv) > 2:
        source = sys.argv[1]
        dest = fileChooser()
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
    global backup
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
        backup = True
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
    return md5




def main():

    #check the arguments for switch cases 
    #sha_1("C:\\Users\\meatw\\Desktop\\school\\PONG\\ball.cpp")
    if len(sys.argv) == 1 :
        print("# | Option \n" +
              "1.| MD1 hash of a file \n" +
              "2.| SHA1 hash of a file \n" +
              "3.| SHA256 hash of a file\n" +
              "4.| backup to a folder and create new copies of the files in the destination folder \n" +
              "5.| replace all files in a folder with those from a source")
        choice = input("Enter a number: ")
        if choice == "1" :
            print(md5(fileChooser()))
    return True
    #copyToMissing(missingFilesList(source, dest), dest)
    #add some form of flag checking to call appropriate flags
if __name__ == "__main__":
    main()

#else:
    #copyToMissing(missingFilesList(), "E:\\Video\\Vids\\missingFiles" )
