from os import walk

print("Enter path 1: ")
path1 = "\\\\fserver\\mounts\\New Volume\\Vids"
print(path1)

print("Enter path 2: ")
path2 = "E:\\Video\\Vids"
print(path2)


f1 = []
for(dirpath, dirnames, filenames) in walk(path1):
    f1.extend(filenames)
f2 = []
for(dirpath, dirnames, filenames) in walk(path2):
    f2.extend(filenames)

missingFiles = []

for n1 in f1:
    found = False
    for n2 in f2:
        if n1 == n2:
            found = True
    if found == False:
        file = (path1 + n1)
        missingFiles.append(file)

files = "\""
files = files + "\", \"".join(missingFiles)
files = files + "\""
print(files)


#\\fserver\mounts\New Volume\Vids
#E:\Video\Vids