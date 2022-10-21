#!/usr/bin/env python
#
#This script parses the foldernames and passes them to TMDB API to fetch the movie details - Movie Name, Director, and Release year
#Then it the writes fetched data in the required format - [Year] Movie name (Director) into a csv file along with the original folder name (this is useful to match the folder names when bulk renaming all the folders)
#

import os
import re
import json
import urllib.parse
import urllib.request
import datetime
# from dateutil.parser import *
# from datetime import *
import csv
import time
import tmdbsimple as tmdb
from xmlrpc.client import _datetime


def getImdbResponse(title, getyear):
    apiKey = "inser your api TMDB key"
    titleSplit = title.split()
    count = len(titleSplit)
    yearreq = int(getyear)
    # print (count)
    while count > 0:
        words = titleSplit[:count]
        encoded = urllib.parse.quote(str(words))
        # print(str(words))
        mvReq = "https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1&include_adult=true&year=%s" % (
            apiKey, encoded, yearreq)
        mvResp = urllib.request.urlopen(mvReq)
        mvJson = mvResp.read()
        mvDetailstemp = json.loads(mvJson)
        # print(mvDetailstemp)
        if mvDetailstemp['total_results'] == 0:
            count = 0
            return None
            time.sleep(1)
        else:
            def myFunc(e):
                return e['vote_count']
            mvDetails = mvDetailstemp['results']
            mvDetails.sort(reverse=True, key=myFunc)
            # print(mvDetails)
            if yearreq == 0000:
                mvName = mvDetails[0]
            else:
                Validate = [
                    yearVal for yearVal in mvDetails if (datetime.datetime.strptime(yearVal['release_date'], "%Y-%m-%d")).year == yearreq]

                # print(Validate)
                if Validate == []:
                    print("No matching year found for this Movie: "+title)
                    count = 0
                    return None
                    time.sleep(1)
                else:
                    mvName = Validate[0]

            mvID = mvName['id']
            crewReq = "https://api.themoviedb.org/3/movie/%s/credits?api_key=%s&language=en-US" % (
                mvID, apiKey)
            crewResp = urllib.request.urlopen(crewReq)
            crewJson = crewResp.read()
            crewDetails = json.loads(crewJson)

            movietitle = mvName['title']
            moviedate = mvName['release_date']
            crew = crewDetails['crew']
            # print(crew)
            directors = [
                credit["name"] for credit in crew if credit["job"] == "Director"]

            dirdetails = directors
            # print(dirdetails)
            dirName = ', '.join([str(elem) for elem in dirdetails])
            # print(dirName)
            # date = _datetime(moviedate)
            yearDetails = (datetime.datetime.strptime(
                moviedate, "%Y-%m-%d")).year
            # # print(year)
            # years = date.year
            mvyear = str(yearDetails)
            details = "[" + mvyear + "]" + " " + \
                movietitle + " " + "(" + dirName + ")"
            # print(movietitle)
            count = 0
            return details
            time.sleep(1)


dirnames = [dname for dname in os.listdir(
    'Your Movies folder name') if os.path.isdir(os.path.join('Your Movies folder name', dname))]
for dirname in dirnames:
    moviePath = (os.path.join('Your Movies folder name', dirname))
    dirname = re.sub('\W', ' ', dirname)
    # all the below replace w space
    dirname = re.sub('.avi', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('.mp4', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('.mkv', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('AC3', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(
        'DVDRIP', ' ', dirname.rstrip(), flags=re.IGNORECASE)
    dirname = re.sub('2160p', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('1080p', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('720p', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    try:
        year = re.search(r'\d{4}.*?', dirname).group(0)
    except AttributeError:
        year = '0000'

    dirname = re.sub('www ', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('torrenting ', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub('com     ', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(r'(?!2046)(19|20)[\d]{2,2}\S.*$', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(r'(?!2046)(19|20)[\d]{2,2}\s.*$', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(r'(?!2046)(19|20)[\d]{2,2}.*$', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(r'/^ +/gm, ''', ' ', dirname.lstrip(),
                     flags=re.IGNORECASE)
    dirname = re.sub(r'/^ +/gm, ''', ' ', dirname.rstrip(),
                     flags=re.IGNORECASE)

    file = str(dirname)
    # print(file)
    # print(year)
    if "sample" not in dirname.lower():
        movieDetails = getImdbResponse(file, year)
        # print(moviePath)
        if movieDetails is None:
            wrt = "No match found for: '"+file+"' in path - "+moviePath
            csvFile = open('Your script folder name/Output/failed_foldernames.csv', 'a',
                           newline='', encoding="utf-8")
            csvWriter = csv.writer(csvFile)
            csvData = [[wrt]]
            csvWriter.writerows(csvData)
            csvFile.close()
        else:
            movieDetails = re.sub(',', ' and', movieDetails.rstrip()) 
            movieName = movieDetails

            movieName = re.sub(r'/^ +/gm, ''', ' ', movieName.lstrip(),
                               flags=re.IGNORECASE)
            movieName = re.sub(r'/^ +/gm, ''', ' ', movieName.rstrip(),
                               flags=re.IGNORECASE)
            # print(movieName)
            csvFile = open('Your script folder name/Output/orig_foldernames.csv', 'a',
                           newline='', encoding="utf-8")
            csvWriter = csv.writer(csvFile)
            csvData = [[movieName, moviePath]]
            csvWriter.writerows(csvData)
            csvFile.close()
