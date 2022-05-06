This is a python application that will take inputs in the form of python fileChecker/py source destination [-option].

options:
  -h, --help            show this help message and exit
  -t, --t               timestamps all of the files in the destination to show they are up to date after the backup
  -ext EXT [EXT ...], --ext EXT [EXT ...]
                        filters an extention type(s) to be copied from the source to the destination
  -log LOG [LOG ...], --log LOG [LOG ...]
                        create a log file for the copies or a list of files missing in case of the nocopy command
  -cp, --cp             copy the file using the command lines cp command
  -r, --r               replace the files that are in the destination folder with the version from the source. !!!Warning the files will be overwritten!!!
  -b, --b               backup by creating a folder with a copy of the source in the new source folder
  -robo, --robo         copy the file using the command lines robo command
  -n, --nocopy          just make a list of missing files
  -a, --a               creates a zip file of the source folder
  -1, --sha1            uses SHA1 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files
  -5, --md5             uses a MD5 hash to ensure that the files in the destination match those of the source and copies over any missing files
  -256, --sha256        uses SHA256 hashes to ensure the files in the destination are the same as the source to ensure there are no missing files


The program will display an option menu in the case that there is no input arguments. 
The option menu is something like this
# | Option
1 | MD5 hash of a file
2 | SHA1 hash of a file
3 | SHA256 hash of a file
4 | backup to a folder and create new copies of the files in the destination folder
5 | replace all files in a folder with those from a source
6 | timestamp all of the files in a directory

If an option to do a copy operation is selected it then asks if a hash check should be performed for integrity and whether or not to create a logfile

The goal of this program is to easily perform backups that are based on hashcodes that ensure integrity. This can be automated in order to create consistent backups.

The current goals for this project is to make something that can be used to ensure my large backups happen accuratly and only copy over missing files based on a hash a hash check instead of name alone.
