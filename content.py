import os
def content(app_folder):

 APP_FOLDER = app_folder

 totalFiles = 0
 totalDir = 0

 for base, dirs, files in os.walk(APP_FOLDER):
    print('Searching in : ',base)
    for directories in dirs:
        totalDir += 1
    for Files in files:
        totalFiles += 1


 print('Total number of files',totalFiles)
 print('Total Number of directories',totalDir)
 print('Total:',(totalDir + totalFiles))
 return totalFiles
