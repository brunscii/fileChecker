'''Author: Chris Carlin

ToDo:
>check if only source and no destination and check for appropriate flags (1,5,256,t,log)
>add a logging feature
>add a way to read the logs for a resume feature

'''

from os import chdir, walk
from os import path
from os.path import exists
from pathlib import Path
import shutil
from subprocess import call
from argparse import ArgumentParser
import hashlib
import datetime


parser = ArgumentParser(description='Backup and Archival Tool')
copyType = parser.add_mutually_exclusive_group()
hashCheckType = parser.add_mutually_exclusive_group()

parser.add_argument('source',                   type = str, nargs='?',                      help='the source of the operation')
parser.add_argument('destination',              type = str, nargs='?',                      help='the destination of the operation')
parser.add_argument('-t',   "--t",              action = "store_true",                      help = "timestamps all of the files in the destination to show they are up to date after the backup")
parser.add_argument('-ext', "--ext",            type = str, action = "append",  nargs = '+',help = "filters an extention type(s) to be copied from the source to the destination")
parser.add_argument('-log', "--log",            type =str,  action = "append",  nargs='+',  help = "create a log file for the copies or a list of files missing in case of the nocopy command")
 
copyType.add_argument('-cp',    "--cp",         action = "store_true",                      help = "copy the file using the command lines cp command")
copyType.add_argument('-r',     '--r',          action = "store_true",                      help = "replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!")
copyType.add_argument('-b',     "--b",          action = "store_true",                      help = "backup by creating a folder with a copy of the source in the new source folder")
copyType.add_argument('-robo',  "--robo",       action = "store_true",                      help = "copy the file using the command lines robo command")
copyType.add_argument('-n',     "--nocopy",     action = "store_true",                      help = "just make a list of missing files")
copyType.add_argument('-a',     '--a',          action = 'store_true',                      help = 'creates a zip file of the source folder')

hashCheckType.add_argument('-1',"--sha1",       action = "store_true",                      help = "uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
hashCheckType.add_argument('-5',"--md5",        action = "store_true",                      help = "uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files")
hashCheckType.add_argument('-256',"--sha256",   action = "store_true",                      help = "uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")

source='asdf'
dest = "asdf"



def missingFilesList(path1, path2):
    '''returns a tuple of dir,file that represent the path of the missing files
    returns missing files in format of (dir,file)missingFiles = []'''
    
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


def copyToMissingRobo(files, dest):
    '''This is a function to copy the missing files to the destination'''
    
    for (dir, fileName) in files:
        call(["robocopy", dir, dest, fileName])
        
def getFolders(s,d):
    '''grab the folders and check that they exist'''
    
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
    '''gets the name of a file and checks if it exists. If it does then it is returned'''
    
    while True :
        f = input(msg)
        if exists(f) :
            if(input("Are you sure y/n: ").lower() == "y"):
                return f
    
def sha_1(filename) :
    '''returns the hashcode in SHA1 for a file'''
    
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha1.update(data)
    return sha1.hexdigest()

def md5(filename) :
    '''returns the hashcode in MD5 for a file'''

    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            md5.update(data)
    return md5.hexdigest()

def sha_256(filename) :
    '''returns the hashcode in SHA256 for a file'''

    sha256 = hashlib.sha256()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha256.update(data)
    return sha256.hexdigest()

def getFileHashDict(foldername):
    '''returs a hash dictionary of hashcode : filename'''
    
    listOfFiles = {}
    #chdir(foldername)
    for dirpath,filename in fileList(foldername):
        fpath = path.join(dirpath,filename)
        listOfFiles[sha_1(fpath)] = fpath
        
    return listOfFiles

def checkMissingIntact(sourceDict, destDict, rootFolder ):
    '''Takes a dictionary of hash:path\\filename and returns a list of files missing from the hash list and the file structure.
    if the hash matches but the file is in a different structure in the destination than in the source then it will be considered missing
    '''
    
    missingFiles = []
    for f in sourceDict:
        if not f in destDict:
            missingFiles.append(sourceDict[f])
        else:
            head,tail = path.split(rootFolder)
            h,t = path.split(sourceDict[f])
            head = str.split(head).pop()
            h = str.split(h).pop()
            if head != h:
                missingFiles.append(sourceDict[f])

    return missingFiles

def extFilter(src,inc):
    '''returns a tuple of (path,file) from the src path that incudes the extension contained in inc'''
    
    files = fileList(src)
    #since the files list is a tuple (path,file) and splitext is (file,ext) then ([1])[1]
    return filter(lambda f: path.splitext(f[1])[1] == inc,files)

def backup(s = "", destination = "", name = "",copyVer='default',hashCheck='none',options=[]):
    '''performs a backup depending on the copying style, whether or not a hash check is performed'''
    
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


    #check for a hashCheck value and if none then 
    if not hashCheck:
        #use the copytree as default
        if copyVer=='default':      
            print('default:\n')
            try :
                shutil.copytree(src=source,dst=path.join(dest,name))
            except FileExistsError:
                print("Backup name already exists\n")
                backup(source,dest)
        #nocopy command
        elif copyVer == 'nocopy':
            print('nocopy:\n')
            filePrint = lambda path,file: print(path.join(path,file))
            for (p,f) in missingFilesList(source,dest):
                filePrint(p,f)
        #backup protocol
        elif copyVer == 'backup':   
            try :
                shutil.copytree(src=source,dst=path.join(dest,name))
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
    else:
        #use the copytree as default but get a list of files using that hash filter then copy those files to the destination
        if copyVer=='default':      
            print('default:\n')
 
def getMissingFilesByHash(sourceDict,destDict):
    '''non strict check for missing files by hash'''
    
    missingFiles = []
    for f in destDict:
        if not f in destDict:
            missingFiles.append(sourceDict[f])
    return missingFiles
    
def fileList(folderName):
    '''return a tuple of path,filename in a folder'''
    
    files = []
    for(dirpath, dirname, filenames) in walk(folderName) :
        for f in filenames:
            files.append((dirpath,f))
    return files

def getCopyType():
    '''checks for the type of copy to perform in the menu options'''
    
    opt = [(1,"Robo",None),
            (2,"Archive",None),
            (3,"Replace",None)]
    choice = menu1(opt)
    if choice == 1:
        return 'robo'
    if choice == 2:
        return 'archive'
    if choice == 3:
        return 'replace'

    return False

def md5_wrapper():
    return print(md5(fileChooser("Enter a file: ")))

def sha1_wrapper():
    return print(sha_1(fileChooser("Enter a file: ")))

def sha256_wrapper():
    return print(sha_256(fileChooser("Enter a file: ")))

def backup_wrapper():
    return backup(source,dest,getCopyType)

def archive_wrapper():
    return backup(source,dest,'archive')

def timestamp_wrapper():
    return timeStamp(source)

def menu1(options=None):
    '''passes the options that are passed into the function to be printed. If no options are given then the defaults are used'''
    
    if not options: #no options are given so assume the basic menu
        options = [(1,"MD5 hash of a file",md5_wrapper),
                   (2,"SHA1 hash of a file",sha1_wrapper),
                   (3,"SHA256 hash of a file",sha256_wrapper),
                   (4,"backup to a folder and create new copies",backup_wrapper),
                   (5,"replace all files in a folder with those from a source",archive_wrapper),
                   (6,"timestamp all of the files",timestamp_wrapper)]
    if options:
        print("# | Option")
        for num,desc, a in options:
            print(f"{num} | {desc}")
        choice = input("Enter a number: ")
        while True:
            if choice == '0':
                return False
            if int(choice) <= len(options) and int(choice) >0:
                for num,desc,fun in options:
                    if num == int(choice) and fun:
                        fun()
                        return True
                    elif num == int(choice) and not fun:
                        return int(choice)
                    
def timeStamp(destination):
    '''time stamps all of the files and folders in a directory'''
    
    if exists(destination):        
        for p,file in fileList(destination):
            #Path(path).touch()
            Path(path.join(p,file)).touch()
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
        menu1()
        return True
        
    if args.destination: #means we had a source that was valid or attempted and a destination that was entered
        if exists(args.destination):
            dest = args.destination
        else:      
            dest=fileChooser("Enter a destination name: ")
    else: #no destination entered - Check for single file flags and if none then 
        if args.sha1:
            if path.isdir(source):#given a folder show all of the hashes for the files in it
                for dir,filename in fileList(source):
                    fname = path.join(dir,filename)
                    s1 = sha_1(path.join(dir,filename))
                    print(f"{fname:^8} SHA1: {s1}")
                input("....")
            else: #give the hash of a single file
                print(sha_1(source))
                input("....")

        if args.sha256:
            if path.isdir(source):#given a folder show all of the hashes for the files in it
                for dir,filename in fileList(source):
                    fname = path.join(dir,filename)
                    s1 = sha_256(path.join(dir,filename))
                    print(f"{fname:^8} SHA256: {s1}")
                input("....")
            else: #give the hash of a single file
                print(sha_256(source))
                input("....")

        if args.md5:
            if path.isdir(source):#given a folder show all of the hashes for the files in it
                for dir,filename in fileList(source):
                    fname = path.join(dir,filename)
                    s1 = md5(path.join(dir,filename))
                    print(f"{fname:^8} MD5: {s1}")
                input("....")
            else: #give the hash of a single file
                print(md5(source))
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
    if len(args.names) == 0: #no arguments passed to the program
        menu1()
    
    return True
    #copyToMissing(missingFilesList(source, dest), dest)
    #add some form of flag checking to call appropriate flags

if __name__ == "__main__":
    main()
