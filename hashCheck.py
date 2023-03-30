from genericpath import exists, isdir
from os import listdir 
import hashlib
from typing import Dict, List
from os import chdir
from os import path
from os import walk

def sha_1(filename) :
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha1.update(data)
    return sha1.hexdigest()

def fileChooser(msg='Enter a filename: '):
    '''gets the name of a file and checks if it exists. If it does then it is returned'''
    while True :
        f = input(msg)
        if exists(f) :
            if(input("Are you sure y/n: ").lower() == "y"):
                return f
    throw : NameError

def fileList(folderName):
    files = []
    for(dirpath, dirname, filenames) in walk(folderName) :
        for f in filenames:
            files.append((dirpath,f))
    return files


def getFileHashDict(foldername):
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

def test():
    '''This is the tester for this app'''
    source = fileChooser()

    print ( 'SHA1: ', sha_1( source ) )
    # dfiles = getFileHashDict(source) # requires a folder name not file name
    # sfiles = getFileHashDict(fileChooser())

    #this ignores the folder structure and checks for files in the destination that can be in different folders
    '''for f in sfiles:
        if not f in dfiles:
            print(sfiles[f])'''
    # for f in checkMissingIntact(sfiles,dfiles,source):
    #     print(f)


    #do an actual folder by folder check of missing files preserving the file tree
    

if __name__ == "__main__":
    test()