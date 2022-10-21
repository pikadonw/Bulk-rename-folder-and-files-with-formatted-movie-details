#!/usr/bin/env python
#
# This script parses the filenames and passes them to TMDB API to fetch the movie details - Movie Name, Director, and Release year
# Then it the writes fetched data in the required format - [Year] Movie name (Director) into a csv file along with the original filename (this is useful to match the filenames when bulk renaming all the files)
#
import os
import re
import json
import urllib.parse
import urllib.request
import datetime
import csv
import time
import tmdbsimple as tmdb
from xmlrpc.client import _datetime

goodExt = (".avi", ".m2ts", ".mkv", ".mp4")


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
            #date = _datetime(moviedate)
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


files = [filename for filename in os.listdir(
    'Your Movies folder name') if os.path.isfile(os.path.join('Your Movies folder name', filename))]
for filename in files:
    if filename.endswith(goodExt):
        moviePath = (os.path.join('W:\Movies', filename))
        #print(moviePath)
        #filename = re.sub(r'^([a-zA-Z]+?-)', ' ', filename)
        filename = re.sub('\W', ' ', filename)
        filename = re.sub('2160p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('1080p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('720p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        try:
            year = re.search(r'\d{4}.*?', filename).group(0)
        except AttributeError:
            year = '0000'
        # print (filename)
        # print(year)
        # all the below replace w space
        filename = re.sub('.avi', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('.mp4', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('.mkv', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('AC3', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub(
            'DVDRIP', ' ', filename.rstrip(), flags=re.IGNORECASE)
        filename = re.sub('2160p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('1080p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub('720p', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub(r'(?!2046)(19|20)[\d]{2,2}\S.*$', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub(r'(?!2046)(19|20)[\d]{2,2}\s.*$', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub(r'(?!2046)(19|20)[\d]{2,2}.*$', ' ', filename.rstrip(),
                          flags=re.IGNORECASE)
        filename = re.sub(r'/^ +/gm, ''', ' ', filename.lstrip(),
                          flags=re.IGNORECASE)
        file = str(filename)

        # print(file)
        if "sample" not in filename.lower():
            movieDetails = getImdbResponse(file, year)
            if movieDetails is None:
                wrt = "No match found for: '"+file+"' in path - "+moviePath
                csvFile = open('Your script folder name/Output/failed_filenames.csv', 'a',
                               newline='', encoding="utf-8")
                csvWriter = csv.writer(csvFile)
                csvData = [[wrt]]
                csvWriter.writerows(csvData)
                csvFile.close()
            else:
                # print(moviePath)
                movieDetails = re.sub(',', ' and', movieDetails.rstrip()) 
                movieName = movieDetails
                movieName = re.sub(r'/^ +/gm, ''', ' ', movieName.lstrip(),
                                   flags=re.IGNORECASE)
                movieName = re.sub(r'/^ +/gm, ''', ' ', movieName.rstrip(),
                                   flags=re.IGNORECASE)
                                  
                print(movieName)
                csvFile = open('Your script folder name/Output/orig_filenames.csv', 'a',
                               newline='', encoding='utf8')
                csvWriter = csv.writer(csvFile)
                csvData = [[movieName, moviePath]]
                csvWriter.writerows(csvData)
                csvFile.close()
