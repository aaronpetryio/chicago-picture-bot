# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:50:46 2020

@author: apetry
"""
from pathlib import Path

#Pexels
#API_KEY = removed
PHOTO_BASE_URL = "https://api.pexels.com/v1/"
SEARCH_URL = "search?query=chicago&per_page=281"

#Local filepaths
TOP_LEVEL_PATH = Path('/Users/apetry/Data Science/chicago-picture-bot')
PICTURE_FOLDER = 'pictures'
PICTURE_PATH = TOP_LEVEL_PATH.joinpath(PICTURE_FOLDER)

#Metadata filenames
METADATA_FILENAME = 'picture_metadata.json'
METADATA_FILE = PICTURE_PATH.joinpath(METADATA_FILENAME)

#AWS location
BASE_BUCKET = 'chicago-picture-bot'
