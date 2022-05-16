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
class BAT:
    '''Author: Chris Carlin

    ToDo:

    >fix the double menu with no source and destination - return true after
    >check if only source and no destination and check for appropriate flags (1,5,256,t,log)
    >add a logging feature
    >add a way to read the logs for a resume feature
    >add a check in the menu for after the copy type is entered
    >
        

    '''


    def __init__(self):
        self.parser = ArgumentParser(description='Backup and Archival Tool')
        self.copyType = self.parser.add_mutually_exclusive_group()
        self.hashCheckType = self.parser.add_mutually_exclusive_group()

        self.parser.add_argument('source',type=str,nargs='?',help='the source of the operation')
        self.parser.add_argument('destination',type=str,nargs='?',help='the destination of the operation')
        self.parser.add_argument('-t',"--t",action = "store_true",help = "timestamps all of the files in the destination to show they are up to date after the backup")
        self.parser.add_argument('-ext',"--ext",type = str,action = "append",nargs = '+',help = "filters an extention type(s) to be copied from the source to the destination")
        self.parser.add_argument('-log',"--log",type=str,action = "append",nargs='+',help = "create a log file for the copies or a list of files missing in case of the nocopy command")
         
        self.copyType.add_argument('-cp',"--cp",action = "store_true",help = "copy the file using the command lines cp command")
        self.copyType.add_argument('-r','--r',action = "store_true",help = "replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!")
        self.copyType.add_argument('-b',"--b",action = "store_true",help = "backup by creating a folder with a copy of the source in the new source folder")
        self.copyType.add_argument('-robo',"--robo",action = "store_true",help = "copy the file using the command lines robo command")
        self.copyType.add_argument('-n',"--nocopy",action = "store_true",help = "just make a list of missing files")
        self.copyType.add_argument('-a', '--a',action='store_true',help='creates a zip file of the source folder')

        self.hashCheckType.add_argument('-1',"--sha1",action = "store_true",help = "uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
        self.hashCheckType.add_argument('-5',"--md5",action = "store_true",help = "uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files")
        self.hashCheckType.add_argument('-256',"--sha256",action = "store_true",help = "uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")

        self.source='asdf'
        self.dest = 'asdf'

    #checks path1 against path2 for missing files in path2 that exist in path1
    #returns missing files in format of (dir,file)
    def missingFilesList(self,path1, path2):
        '''returns a tuple of dir,file that represent the path of the missing files'''
        missingFiles = []
        if not exists(path1):
            path1 = fileChooser("Enter a source: ")
            global source
            source = path1
        if not exists(path2):
            path2 = fileChooser("Enter a destination: ")
            
            self.dest = path2
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
    def copyToMissingRobo(self,files, dest):
        for (dir, fileName) in files:
            #time.sleep(2.5)
            call(["robocopy", dir, dest, fileName])
            
    def getFolders(self,s,d):
        
        #check the source and destination folders for validity and choose new targets in case of issue
        if exists(s):
            print("Source: " + s)
            self.source = s
        else :
            print("{}is an invalid source path".format(s))
            self.source =self.fileChooser("Enter a source: ")
        if exists(d):
            print("Destination: " + d)
            self.dest = d
        else :
            print("{} is an invalid destination path".format(d))
            self.dest = self.fileChooser("Enter a destination: ")

    def fileChooser(self,msg='Enter a filename: '):
        while True :
            f = input(msg)
            if exists(f) :
                if(input("Are you sure y/n: ").lower() == "y"):
                    return f
        
    def sha_1(self,filename) :
        sha1 = hashlib.sha1()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                sha1.update(data)
        return sha1.hexdigest()

    def md5(self,filename) :
        md5 = hashlib.md5()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                md5.update(data)
        return md5.hexdigest()

    def sha_256(self,filename) :
        sha256 = hashlib.sha256()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                sha256.update(data)
        return sha256.hexdigest()

    def getFileHashDict(self,foldername):
        listOfFiles = {}
        #chdir(foldername)
        for dirpath,filename in self.fileList(foldername):
            fpath = path.join(dirpath,filename)
            listOfFiles[sha_1(fpath)] = fpath
            
        return listOfFiles

    def checkMissingIntact(self,sourceDict, destDict, rootFolder ):
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

    def extFilter(self,src,names):
        return names

    def backup(self,s = "", destination = "", name='',copyVer='default',hashCheck=None,options=[]):
        
        #Error checking to make sure the source/dest exists
        self.getFolders(s,destination)
        
        #if no name is passed in
        if name == '' :
            if input("Use {} as the default name for this backup?".format(str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + self.source.rsplit("\\").pop())).lower() == "y":
                name = str(datetime.date.today().strftime("%m-%d-%Y")) + "-" + self.source.rsplit("\\").pop()
            else:
                while True :
                    name = input("Enter a backup name then: ")
                    if input("are you sure?").lower() == "y":
                        break


        #check for a hashCheck value and if none then 
        if not hashCheck:
            print("kjhgkjhgkjhgkjgh")
            #use the copytree as default
            if copyVer=='default':
                print('default:\n')
                try :
                    print(os.path.join(self.dest,name))
                    shutil.copytree(src=self.source,dst=os.path.join(self.dest,name))
                except FileExistsError:
                    print("Backup name already exists\n")
                    backup(self.source,self.dest)
            #nocopy command
            elif copyVer == 'nocopy':
                print('nocopy:\n')
                filePrint = lambda path,file: print(os.path.join(path,file))
                for (p,f) in missingFilesList(self.source,self.dest):
                    filePrint(p,f)
            #backup protocol
            elif copyVer == 'backup':   
                try :
                    shutil.copytree(src=self.source,dst=os.path.join(str(self.dest),str(name)))
                except FileExistsError:
                    print("Backup name already exists\n")
                    backup(source,self.dest)
            #archive by creating a zip
            elif copyVer == 'archive':  
                try :
                    chdir(self.dest)
                    #shutil.ignore_patterns()
                    shutil.make_archive(base_name=name,root_dir=self.dest,base_dir=self.source,format='zip')
                    input("Press any key...")
                except FileExistsError:
                    print("archive name already exists\n")
                    backup(source,self.dest)
            #robocopy
            elif copyVer == 'robo':
                copyToMissingRobo(missingFilesList(self.source,self.dest),self.dest)
            return True
        else:
            #use the copytree as default but get a list of files using that hash filter then copy those files to the destination
            if copyVer=='default':      
                print('default:\n')
                
     
    def getMissingFilesByHash(self,source,dest,hashType):
        sourceFiles = os.listdir(source)
        destFiles = os.listdir(dest)

    def fileList(self,folderName):
        files = []
        for(dirpath, dirname, filenames) in walk(folderName) :
            for f in filenames:
                files.append((dirpath,f))
        return files

    def getCopyType(self):
        opt = [(1,"Robo",None),
                (2,"Archive",None),
                (3,"Replace",None),
                (4,"Default",None)]
        choice = self.menu1(opt)
        if choice == 1:
            return 'robo'
        if choice == 2:
            return 'archive'
        if choice == 3:
            return 'replace'

        return False

    def md5_wrapper(self):
        return self.print(self.md5(self.fileChooser("Enter a file: ")))
    def sha1_wrapper(self):
        return self.print(self.sha_1(self.fileChooser("Enter a file: ")))
    def sha256_wrapper(self):
        return self.print(self.sha_256(self.fileChooser("Enter a file: ")))
    def backup_wrapper(self):
        return self.backup(self.source,self.dest,copyVer=self.getCopyType())
    def archive_wrapper(self):
        return self.backup(self.source,self.dest,'archive')
    def timestamp_wrapper(self):
        return self.timestamp(self.source)

    def menu1(self,options=None):
        if not options: #no options are given so assume the basic menu
            options = [(1,"MD5 hash of a file",self.md5_wrapper),
                       (2,"SHA1 hash of a file",self.sha1_wrapper),
                       (3,"SHA256 hash of a file",self.sha256_wrapper),
                       (4,"backup to a folder and create new copies of the files in the destination folder",self.backup_wrapper),
                       (5,"replace all files in a folder with those from a source",self.archive_wrapper),
                       (6,"timestamp all of the files in a directory",self.timestamp_wrapper)]
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
            
    #time stamps all of the files and folders in a directory
    def timeStamp(self,destination):
        if exists(destination):        
            for path,file in fileList(destination):
                Path(path).touch()
                Path(os.path.join(path,file)).touch()
        else:
            timeStamp(fileChooser('Enter a destination: '))
        return True

    def main(self):
        
        
        args = self.parser.parse_args()
        if args.source:
            if exists(args.source):
                self.source = args.source
            else:
                self.source=fileChooser("Enter a source name: ")
        else:
            self.menu1()
            return True
            
        if args.destination: #means we had a source that was valid or attempted and a destination that was entered
            if exists(args.destination):
                self.dest = args.destination
            else:      
                self.dest=fileChooser("Enter a destination name: ")
        else: #no destination entered - Check for single file flags and if none then 
            if args.sha1:
                if os.path.isdir(source):#given a folder show all of the hashes for the files in it
                    for dir,filename in fileList(source):
                        fname = os.path.join(dir,filename)
                        s1 = sha_1(os.path.join(dir,filename))
                        print(f"{fname:^8} SHA1: {s1}")
                    input("....")
                else: #give the hash of a single file
                    print(sha_1(source))
                    input("....")
            if args.sha256:
                if os.path.isdir(source):#given a folder show all of the hashes for the files in it
                    for dir,filename in fileList(source):
                        fname = os.path.join(dir,filename)
                        s1 = sha_256(os.path.join(dir,filename))
                        print(f"{fname:^8} SHA256: {s1}")
                    input("....")
                else: #give the hash of a single file
                    print(sha_256(self.source))
                    input("....")
            if args.md5:
                if os.path.isdir(self.source):#given a folder show all of the hashes for the files in it
                    for dir,filename in fileList(self.source):
                        fname = os.path.join(dir,filename)
                        s1 = md5(os.path.join(dir,filename))
                        print(f"{fname:^8} MD5: {s1}")
                    input("....")
                else: #give the hash of a single file
                    print(md5(self.source))
                    input("....")
        if args.b:
            print("Backup mode initialized:\n")
            backup(self.source,self.dest,copyVer='backup')
            #return True
        if args.a:
            print("Archive mode initialized:\n")
            backup(self.source,self.dest,copyVer='archive')
            #return True
        if args.nocopy:
            backup(self.source,self.dest,copyVer='nocopy',name='none')
        if args.t :
            timeStamp(self.dest)
        if len(args.names) == 0: #no arguments passed to the program
            menu()
        
        return True
        #copyToMissing(missingFilesList(source, self.dest), self.dest)
        #add some form of flag checking to call appropriate flags
if __name__ == "__main__":
    b = BAT()
    b.main()
