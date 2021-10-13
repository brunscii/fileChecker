from os import walk
from shutil import copyfile
from subprocess import call

#returns missing files in format of (dir,file)
def missingFilesList(path1 = "\\\\fserver\\mounts\\New Volume\\Vids", path2 = "E:\\Video\\Vids"):
        
    print("Enter path 1: ")
    #path1 = "\\\\fserver\\mounts\\New Volume\\Vids"
    print(path1)

    print("Enter path 2: ")
    #path2 = "E:\\Video\\Vids"
    print(path2)

    f1 = []
    for(dirpath, dirnames, filenames) in walk(path1):
        for name in filenames:
            f1.append((dirpath,name))
    f2 = []
    for(dirpath, dirnames, filenames) in walk(path2):
        for name in filenames:
            f2.append((dirpath,name))

    missingFiles = []

    for (dirPath1, fileName1) in f1:
        found = False
        for (dirPath2, fileName2) in f2:
            if fileName1 == fileName2:
                found = True
        if found == False:
            missingFiles.append((dirPath1,fileName1))

    return missingFiles
"""     files = "\""
    files = files + "\", \"".join(missingFiles)
    files = files + "\""
    print(files) """

def copyToMissing(files, dest):
    for (dir, fileName) in files:
        call(["robocopy", dir, dest, fileName, "/sec"])

copyToMissing(missingFilesList(), "E:\\Video\\Vids\\missingFiles" )
#copyFiles(missingFilesList(),"\\\\fserver\\mounts\\New Volume\\Vids\\", "E:\\Video\\Vids\\missingFiles\\")
    #\\fserver\mounts\New Volume\Vids
    #E:\Video\Vids