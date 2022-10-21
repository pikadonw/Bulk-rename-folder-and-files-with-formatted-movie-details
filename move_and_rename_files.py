#!/usr/bin/env python
#This script fetches all the data from the csv file "Your script folder name/Output/orig_filenames.csv" created by the 'mvfind_file.py' script.
#And creates a folder in the required format, and it renames and moves that file to that new folder. 
#Technically it moves the renamed files to a corresponding folder (by creating that folder).


import shutil
import csv
import re
import os
import time

destination = "Your Movies folder name"


def move(src, dest):
    shutil.move(src, dest)


with open('Your script folder name/Output/orig_filenames.csv', 'r', encoding="utf8") as movies:
    reader = csv.reader(movies)
    for row in reader:
        moviePath = row[1]
        movieName = row[0]
        #print(moviePath)
        
        movieExtension = moviePath[-4:]
        movieName = re.sub('/', '-', movieName.rstrip())
        movieName = re.sub(',', '', movieName.rstrip())
        #movieName = re.sub('?', '', movieName.rstrip())
        movieName = re.sub('"', '', movieName.rstrip())
        movieName = re.sub('<', '', movieName.rstrip())
        movieName = re.sub('>', '', movieName.rstrip())
        movieName = re.sub("'", '', movieName.rstrip())
        movieName = re.sub('\'', '', movieName.rstrip())
        movieName = re.sub(':', ' -', movieName.rstrip())
        #print(movieName)
        Dest = destination +"/"+movieName
        #print(Dest)
        os.makedirs(Dest)
        fullDest = Dest +"/"+movieName+movieExtension
        #print(fullDest)
        move(moviePath, fullDest)
        csvFile = open('output.csv', 'a',newline='',encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        temp = "Move Successfull for files: "+movieName+movieExtension
        csvData = [[temp]]
        csvWriter.writerows(csvData)
        csvFile.close()
        time.sleep(1)
