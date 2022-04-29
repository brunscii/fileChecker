import os
from os.path import exists
from pathlib import Path

while True:
    p = input("Enter a path: ")
    pathTo = p if exists(p) else None 
    if pathTo:
        while True:
            f = input("Enter a filename: ")
            filename = f if os.path.isfile(os.path.join(pathTo,f)) else None
            print(os.path.join(pathTo,f))
            if filename:
                Path(os.path.join(pathTo,filename)).touch()
                
                exit()