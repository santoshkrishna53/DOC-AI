from google.cloud import storage
from google.cloud import vision
from google.cloud import storage
import os
import io
storage_client = storage.Client()
bucket = storage_client.bucket('testproject-75541.appspot.com')
blob = bucket.blob('oceimage.PNG')
blob.download_to_filename('tempImageFile.PNG')

def detect_text():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = 'tempImageFile.PNG'
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception('{}\n Error: '.format(response.error.message))
    for text in response.text_annotations:
        string = string + text.description
    temp_file = open('tempfile.txt', 'w')
    temp_file.write(string)
    temp_file.close()
    bucket = storage_client.bucket('testproject-75541.appspot.com')
    blob = bucket.blob('results.txt')
    blob.upload_from_filename('tempfile.txt')

detect_text()