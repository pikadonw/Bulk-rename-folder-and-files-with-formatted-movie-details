#!/usr/bin/env python
#This script fetches all the data from the csv file "Your script folder name/Output/orig_foldernames.csv" created by the 'mvfind_folder.py' script.
#And renames all the existing foldernames to the required foldernames - [Year] Movie name (Director). 
#Technically it moves the contents of the folder to the new formatted foldername path


import shutil
import csv
import re
import os
import time

destination = "Your Movies folder name"


def rename(src, dest):
    os.rename(src, dest)


with open('Your script folder name/Output/orig_foldernames.csv', 'r', encoding="utf8") as folder:
    reader = csv.reader(folder)
    for row in reader:
        folderPath = row[1]
        folderName = row[0] 
        folderName = re.sub('/', '-', folderName.rstrip())
        folderName = re.sub(',', '', folderName.rstrip())
        #folderName = re.sub('?', '', folderName.rstrip())
        folderName = re.sub('"', '', folderName.rstrip())
        folderName = re.sub('<', '', folderName.rstrip())
        folderName = re.sub('>', '', folderName.rstrip())
        folderName = re.sub("'", '', folderName.rstrip())
        folderName = re.sub('\'', '', folderName.rstrip())
        folderName = re.sub(':', ' -', folderName.rstrip())
        newFoldername = destination+"/"+folderName
        #print(newFoldername)
        rename(folderPath, newFoldername)
        csvFile = open('output_folder.csv', 'a',newline='',encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        temp = "Rename Successfull for folders: "+folderName
        csvData = [[temp]]
        csvWriter.writerows(csvData)
        csvFile.close()
        time.sleep(1)
