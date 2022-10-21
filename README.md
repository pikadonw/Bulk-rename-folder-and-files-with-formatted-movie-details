# Bulk Folder and file renaming for Movies using TMDB API
To bulk rename any/all unorderly Movie folders and files to a formatted name - "[Year] Movie name (Director)" with proper Movie details fetched from TMDB.

## Prerequistes:
* Latest version of Python installed.
* TMDB API Key -> https://www.themoviedb.org/settings/api
* (Optional) Any editors like VS Code to edit the scripts to your preference.

## Scripts:
### For renaming the existing movie filenames to a formatted name and moving them into corresponding folders of the same name,
         * mvfind_file.py --> To find Movie details in the format of [Year] Movie name (Director) from the filenames via TMDB API.
         * move_and_rename_files.py --> To rename the original unformatted/unorderly filenames to the fetched values and move them into a folder of the same new name. 

### For renaming the existing movie folder names to a formatted name,
         * mvfind_folder.py--> To find Movie details in the format of [Year] Movie name (Director) from the Folder names via TMDB API.
         * rename_folders.py --> To rename the original unformatted/unorderly folder names to the fetched values.

## Process:
1. Edit the script for finding and replacing your API and folder details.<br/>
       * "inser your api TMDB key" --> TMDB API Key (in mvfind_file.py and mvfind_folder.py).<br/>
       * "Your script folder name" --> Folder where you have placed/downloaded the scripts (in all the scripts).<br/>
       * "Your Movies folder name" --> Folder where your movie files and folders exist(in all the scripts).<br/>
2. Run the find files (mvfind_file.py and mvfind_folder.py) and it will return a csv file with data like "new formatted name, original folder/filename".<br/>
        * **For e.g. "[2021] Last Night in Soho (Edgar Wright),W:\Format Movies folder\Test\Last.Night.in.Soho.2021.2160p.WEB-DL.x265".**<br/>
3. Validate the ouput orig_filenames.csv, and orig_foldernames.csv for any discrepencies before executing the rename files.<br/>         
4. Run the rename files (rename_folders.py, and move_and_rename_files.py) and it will take the previous csv data and make new folder/filenames with the new                formatted name.
5. That's it! Your folder/files should be renamed by now.
         
 *Run the python files based on your preference/need (either renaming only files, folders or both) in the order/group mentioned above.


#### Disclaimer: In some cases TMDB does not return the expected movie details and it can be frustrating. It can be overcome by tweaking the code or alter the existing filename for the query to fetch the required movie details.
              
I highly doubt anyone would want to bulk rename movie files and folders this way (since this took me almost 3 days to refine, and I honestly think i could have manually renamed all my movie files within 2 days), but this way is fun! If anyone faces any issues with the scripts or if you have some queries please hit me up at my discord.

Discord: Pikadon#5713

Thank you!
