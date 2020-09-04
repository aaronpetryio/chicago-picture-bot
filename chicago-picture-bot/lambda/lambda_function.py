# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 09:45:12 2020

@author: apetry
"""

import json
import boto3
from botocore.exceptions import ClientError
import tempfile
import os
from six.moves.html_parser import HTMLParser
import random
from collections import defaultdict
from twython import Twython, TwythonError

session = boto3.Session()
s3_resource = boto3.resource('s3', region_name='us-east-1')
s3 = boto3.client('s3')
ssm = boto3.client('ssm')
h = HTMLParser()

def lambda_handler(event, context):
    bucket_name = 'chicago-picture-bot'
    key = 'picture_metadata.json'

    try:
        # load json metadata from S3 bucket into JSON
        data = s3.get_object(Bucket=bucket_name, Key=key)
        json_data = json.loads(data['Body'].read().decode('utf-8'))
    except Exception as e:
        print(e)
        raise e

    print("Got keys")

    indexed_json = defaultdict()

    for value in json_data:
        photographer = value['photographer']
        photographer_url = value['photographer_url']
        values = [photographer, photographer_url]

        # return only image name at end of URL
        find_index = value['src']['original'].rfind('/')
        img_suffix = value['src']['original'][find_index + 1:]
        img_link = img_suffix

        try:
            indexed_json[img_link].append(values)
        except KeyError:
            indexed_json[img_link] = (values)

    # Shuffle images
    single_image_metadata = random.choice(list(indexed_json.items()))

    url = single_image_metadata[0]
    photographer = single_image_metadata[1][0]
    photographer_url = single_image_metadata[1][1]

    print(url, photographer, photographer_url)

    # Connect to Twitter via Twython

    TWITTER_ACCESS_TOKEN = 'Q9c0eadmx9Tly8CzsZ7abAdgp'
    TWITTER_ACCESS_SECRET = '6KcGdiiTPdUrllixZMxcxnvZIT7Y52RgBmGgLLLSSW8Tr9IjEX'
    OAUTH_TOKEN = '1299018493199671297-tcjGzt6jr6xJqcAQRPuuGfn1YlW696'
    OAUTH_TOKEN_SECRET = 'npOnkMUNJvs8oDZQ9032vIpvNEIwqSA4badiyiVC9SkGm'

    try:
        twitter = Twython(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        print(twitter)
    except TwythonError as e:
        print(e)

    #Try tweeting
    try:

        tmp_dir = tempfile.gettempdir()
        # subprocess.call('rm -rf /tmp/*', shell=True)
        path = os.path.join(tmp_dir, url)
        print(path)

        # Try to match URL in filepath to URL in metadata; if it doesn't work, try another one
        for i in range(0, 3):
                try:
                    x = s3_resource.Bucket(bucket_name).download_file(url, path)
                    print("file moved to /tmp")
                    print(os.listdir(tmp_dir))

                    with open(path, 'rb') as img:
                        print("Path", path)
                        twit_resp = twitter.upload_media(media=img)
                        twitter.update_status(status="Photographer: %s \nFind more from this photographer here: %s" % (photographer, photographer_url),
                                              media_ids=twit_resp['media_id'])
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ResourceNotFoundException':
                        continue
                break


    except TwythonError as e:
        print(e)