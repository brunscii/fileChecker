import os
import argparse
import datetime

for file in os.listdir(r'C:\Users\meatw\Desktop\school\PONG'):
    print(file)

f = open('{}-log'.format(datetime.date.today().strftime('%m-%d-%Y')),'w')
print(f.name)
f.close()

#shutil.make_archive(r'C:\Users\meatw\Desktop\missingFiles\pong' ,"zip",r'C:\Users\meatw\Desktop\school\PONG',)