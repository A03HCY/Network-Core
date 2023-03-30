import os
 
# get all files inside a specific folder
dir_path = './'
for path in os.scandir(dir_path):
    print(path.name, path.is_file(), list(path.stat()))