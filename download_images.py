# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 21:09:25 2020

@author: apetry
"""


import json
import shutil
import sys
import boto3
import requests

import settings

# intialize connection to S3 resources
s3 = boto3.resource('s3')
s3_client = boto3.client('s3', 'us-west-2')

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
                
def upload_images_to_s3(directory):
    """
    Upload images to S3 bucket if they end with png, jpg, or jpeg
    """

    for f in directory.iterdir():
        if str(f).endswith(('.png', '.jpg', '.jpeg')):
            full_file_path = str(f.parent) + "/" + str(f.name)
            file_name = str(f.name)
            s3_client.upload_file(full_file_path, settings.BASE_BUCKET, file_name)
            print(f,"put")


def upload_json_to_s3(directory):
    """
    Upload metadata json to directory
    """

    for f in directory.iterdir():
        if str(f).endswith('.json'):
            full_file_path = str(f.parent) + "/" + str(f.name)
            file_name  = str(f.name)
            s3_client.upload_file(full_file_path, settings.BASE_BUCKET, file_name)
    
upload_json_to_s3(settings.PICTURE_PATH)
