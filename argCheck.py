from argparse import ArgumentParser
'''
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
parser = ArgumentParser()
parser.add_argument('-cp',"--cp",action = "store_true",help = "copy the file using the command lines cp command")
parser.add_argument('-r','--r',action = "store_true",help = "replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!")
parser.add_argument('-b',"--b",action = "store_true",help = "backup by creating a folder with a copy of the source in the new source folder")
parser.add_argument('-1',"--1",action = "store_true",help = "uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
parser.add_argument('-5',"--5",action = "store_true",help = "uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files")
parser.add_argument('-256',"--256",action = "store_true",help = "uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files")
parser.add_argument('-t',"--t",action = "store_true",help = "timestamps all of the files in the destination to show they are up to date after the backup")
parser.add_argument('-ext',"--ext",type = str,action = 'append',nargs = '+',help = "filters an extention type(s) to be copied from the source to the destination")
parser.add_argument('-log',"--log",type=str,action = "append",help = "create a log file for the copies or a list of files missing in case of the nocopy command")
parser.add_argument('-robo',"--robo",action = "store_true",help = "copy the file using the command lines robo command")
parser.add_argument('-nocopy',"--nocopy",action = "store_true",help = "just make a list of missing files")

args = parser.parse_args()

if args.r == True:
    print("r is true")
    input()
if args.cp == True:
    print("cp")
    input()
if args.ext:
    extentions = []
    if len(args.ext) > 0:
        ext = lambda s : f".{s}" 
        
        print(args.ext)
        for i in args.ext:
            print(i)
            for x in i:
                extentions.append(ext(x))
        
        for s in extentions:
            print(s)
        input("Look Good")