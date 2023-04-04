# FileChecker
## Description

The BAT.py file is meant to be a set of tools that can be used either as a standalone app, via the built in options menu and argument parsing, or as a library to be used in creating another app. 

There is also included a fileChecker.py that is a tester for the BAT.py class.

## Options

|           Argument     |          Description |
| :------------------- | :-------------------- |
| -h, --help            | show this help message and exit |
| -t, --t               | timestamps all of the files in the destination to show they are up to date after the backup |
| -ext EXT [EXT ...], --ext EXT [EXT ...] | filters an extention type(s) to be copied from the source to the destination |
| -log LOG [LOG ...], --log LOG [LOG ...] | create a log file for the copies or a list of files missing in case of the nocopy command |
| -cp, --cp             | copy the file using the command lines cp command |
| -r, --r               | replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!! |
| -b, --b               | backup by creating a folder with a copy of the source in the new source folder |
| -robo, --robo         | copy the file using the command lines robo command |
| -n, --nocopy          | just make a list of missing files |
| -a, --a               | creates a zip file of the source folder |
| -1, --sha1            | uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files |
| -5, --md5             | uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files |
| -256, --sha256        | uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files |

---

## The Options Menu

The menu(options) function is used to print a list of options. The function takes in a list of tuples where each tuple contains the option number, a descriptino, and a function to be called by the option. -> [( #, 'option', function ),...] This allows for further customization by passing custom menu options to be displayed. If there is no function included then there then the options function will return the number of the chosen option.

The program will display an option menu in the case that there is no input arguments. 

><br>The option menu is something like this
\# | Option
<br>1 | MD5 hash of a file
<br>2 | SHA1 hash of a file
<br>3 | SHA256 hash of a file
<br>4 | backup to a folder and create new copies of the files in the destination folder
<br>5 | replace all files in a folder with those from a source
<br>6 | timestamp all of the files in a directory

 
If the option to do a copy operation is selected it then asks if a hash check should be performed for integrity and whether or not to create a logfile

The goal of this program is to easily perform backups that are based on hashcodes that ensure integrity. This can be automated in order to create consistent backups.

# TODO: 
- add argCheck to BAT
