from genericpath import isfile
from BAT import BAT
import os
def main():
    backup = BAT('C:\\Users\\meatw\\Desktop\\school\\PONG', 'C:\\Users\\meatw\\Desktop\\missingFiles')
    print(f'Using source file of {backup.source}')
    for f in os.listdir(backup.source):
        
        if isfile(os.path.join(backup.source,f)):
            print(f"MD5 {backup.md5(os.path.join(backup.source,f))} : {f}")

    backup.md5(backup.source)
    return True

if __name__ == '__main__':
    main()