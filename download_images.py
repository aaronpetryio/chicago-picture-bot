# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 21:09:25 2020

@author: apetry
"""


import json
import shutil
import sys

import requests

import settings

def get_json():
    """ 
    Get JSON with photographer name, photographer URL, and location of photo
    Return dictionary of filenames from Pexels 
    """
    data_list=[]
    for page in range(1,2):
        url = settings.PHOTO_BASE_URL + settings.SEARCH_URL
        try:
            response = requests.get(url,timeout=15,headers=settings.API_KEY)
            data=response.json()['photos']
            parse_data(data_list, data)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
    
    return data_list

def parse_data(picture_list,data):
    """
    Extends a list of pictures
    """
    picture_list.extend(data)
    
def save_json(data):
    """
    Converts list to JSON, writes to file
    """
    data = json.dumps(data)
    
    with settings.METADATA_FILE.open('w') as outfile:
        outfile.write(data)
        
def get_image_links(data):
    """
    Passes in a list of image links
    """
    picture_links=[]
    
    for picture in data:
        picture_links.append(picture['src']['original'])
        
    return picture_links
    
def download_images(links):
    """
    Passes in a list of links pointing to image files to download
    """
    
    for link in links:
        try:
            response = requests.get(link, timeout=15, stream=True)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        image_name  = link.rsplit('/', 1)[1]

        file_location = settings.PICTURE_PATH.joinpath(image_name)

        with open(str(file_location), 'wb') as outfile:
                shutil.copyfileobj(response.raw, outfile)
    
download_images(get_image_links(get_json()))    

