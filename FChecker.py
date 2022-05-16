import os
from os import walk,path
import hashlib

def extFilter(src,inc):
    #filteredFiles = []
    files = fileList(src)
    return filter(lambda f: path.splitext(f[1])[1] == inc,files)
    #for p,f in files:
    #    if path.splitext(f)[1] == inc:
    #        print(f)
    #        filteredFiles.append(f)
    #return filteredFiles
    

def getFileHashDict(foldername):
    '''returs a hash dictionary of hashcode : filename'''
    listOfFiles = {}
    #chdir(foldername)
    for dirpath,filename in fileList(foldername):
        fpath = path.join(dirpath,filename)
        listOfFiles[sha_1(fpath)] = fpath
    return listOfFiles

def sha_1(filename):
    '''returns the hashcode in SHA1 for a file'''
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        while True:
            data = f.read(65536)
            if not data :
                break
            sha1.update(data)
    return sha1.hexdigest()

def fileList(folderName):
    '''return a tuple of path,filename in a folder'''
    files = []
    for(dirpath, dirname, filenames) in walk(folderName) :
        for f in filenames:
            files.append((dirpath,f))
    return files

def main():
    print(list(extFilter('C:\\Users\\meatw\\Desktop\\school\\PONG','.cpp')))
    #print(path.splitext('C:\\Users\\meatw\\Desktop\\school\\PONG\\ball.h'))

if __name__ == '__main__':
    main()