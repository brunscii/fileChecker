from genericpath import isdir
from os import listdir 
import hashlib
from typing import List
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

def test():
    dfiles = getFileHashDict("C:\\Users\\meatw\\Desktop\\missingFiles")
    sfiles = getFileHashDict("C:\\Users\\meatw\\Desktop\\school\\PONG")

    #this ignores the folder structure and checks for files in the destination that can be in different folders
    for f in sfiles:
        if not f in dfiles:
            print(sfiles[f])


    #do an actual folder by folder check of missing files preserving the file tree
    

if __name__ == "__main__":
    test()