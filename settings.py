# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:50:46 2020

@author: apetry
"""
from pathlib import Path

#Pexels
API_KEY = {'Authorization':'563492ad6f9170000100000123a66e89f37a4bfe836394f9e8efad36'}
PHOTO_BASE_URL = "https://api.pexels.com/v1/"
SEARCH_URL = "search?query=chicago&per_page=4"

#Local filepaths
TOP_LEVEL_PATH = Path('/Users/apetry/Data Science/chicago-picture-bot')
PICTURE_FOLDER = 'pictures'
PICTURE_PATH = TOP_LEVEL_PATH.joinpath(PICTURE_FOLDER)

#Metadata filenames
METADATA_FILENAME = 'picture_metadata.json'
METADATA_FILE = PICTURE_PATH.joinpath(METADATA_FILENAME)
