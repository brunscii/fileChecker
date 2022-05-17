from os import chdir, walk
import os
from os.path import exists
from pathlib import Path
import shutil
import sys
import time
import hashlib
import datetime

class BAT:

    def __init__(self, src = None, dst = None, hashType = None, copyType = None, name = None):
        self.source = src
        self.dest = dst
        self.hashType = copyType
        self.copyType = hashType
        self.name = name

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

    def copyToMissingRobo(self,files, dest):
        '''This is a function to copy the missing files to the destination'''
        for (dir, fileName) in files:
            #time.sleep(2.5)
            call(["robocopy", dir, dest, fileName])
            
    def getFolders(self,s,d):
        '''grab the folders and check that they exist'''
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
        '''gets the name of a file and checks if it exists. If it does then it is returned'''
        while True :
            f = input(msg)
            if exists(f) :
                if(input("Are you sure y/n: ").lower() == "y"):
                    return f
        
    def sha_1(self,filename) :
        '''returns the hashcode in SHA1 for a file'''
        sha1 = hashlib.sha1()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                sha1.update(data)
        return sha1.hexdigest()

    def md5(self,filename) :
        '''returns the hashcode in MD5 for a file'''
        md5 = hashlib.md5()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                md5.update(data)
        return md5.hexdigest()

    def sha_256(self,filename) :
        '''returns the hashcode in SHA256 for a file'''
        sha256 = hashlib.sha256()
        with open(filename,'rb') as f:
            while True:
                data = f.read(65536)
                if not data :
                    break
                sha256.update(data)
        return sha256.hexdigest()

    def getFileHashDict(self,foldername):
        '''returs a hash dictionary of hashcode : filename'''
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
        '''returns a tuple of (path,file) from the src path that incudes the extension contained in inc'''
        files = fileList(src)
        #since the files list is a tuple (path,file) and splitext is (file,ext) then ([1])[1]
        return filter(lambda f: path.splitext(f[1])[1] == inc,files)

    def backup(self,s = "", destination = "", name='',copyVer='default',hashCheck=None,options=[]):
        '''performs a backup depending on the copying style, whether or not a hash check is performed'''
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
            print("No Hash Checking Enabled:::::::")
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
        '''non strict check for missing files by hash'''
        sourceFiles = os.listdir(source)
        destFiles = os.listdir(dest)

    def fileList(self,folderName):
        '''return a tuple of path,filename in a folder'''
        files = []
        for(dirpath, dirname, filenames) in walk(folderName) :
            for f in filenames:
                files.append((dirpath,f))
        return files

    def getCopyType(self):
        '''checks for the type of copy to perform in the menu options'''
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
        '''passes the options that are passed into the function to be printed. If no options are given then the defaults are used'''

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
        '''time stamps all of the files and folders in a directory'''
        if exists(destination):        
            for path,file in fileList(destination):
                Path(path).touch()
                Path(os.path.join(path,file)).touch()
        else:
            timeStamp(fileChooser('Enter a destination: '))
        return True

    def main(self):
        self.menu1()
        return True
        
if __name__ == "__main__":
    b = BAT('C:\\Users\\meatw\\Desktop\\school\\PONG','C:\\Users\\meatw\\Desktop\\missingFiles')
    b.main()
