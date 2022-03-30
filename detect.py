import os
import json
import boto3
import smtplib
from email.message import EmailMessage
from os import environ
from datetime import date
import json
import base64
from io import BytesIO

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

#S3 bucket name 
destination_bucketname = os.environ['test_yolo_bucket']
def lambda_handler(event, context):

    print("Event :", event)
    source_bucket_name = event['Records'][0]['s3']['bucket']['name']
    print("Source bucket name is: ", source_bucket_name, "only")

    file_key_name = event['Records'][0]['s3']['object']['key']
    print('File key name is: ', file_key_name, "only")
    
    bucket = s3_resource.Bucket(source_bucket_name)
    path, filename = os.path.split(file_key_name)
    print('path found for S3 is:', path)
    print('Key we are downloading is: ',filename)
    
    print('before downloading file from S3, filename: at /tmp/', filename)
    try:
        bucket.download_file(file_key_name, "/tmp/" + filename)
    except Exception as e:
        print('failed to download file from S3, exception occurred: ',e)

    print('inside this directory: ',os.getcwd())
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print('contents in current directory:', files)

    print('before calling detect python file')
    try:
        os.system("python3 detect.py --project /tmp/ --exist-ok  --save-txt --source /tmp/"+ filename  )
    except Exception as e:
        print('exception occurred in detect python file: ', e)

    print('before uploading output file to destination S3 bucket')
    
    try:
        s3.upload_file('/tmp/exp/'+filename, destination_bucketname,"output_images/"+filename)
    except:
        print('inside exp 2 ')
        s3.upload_file('/tmp/exp2/'+filename, destination_bucketname,"output_images/"+ filename)
    
    print('end of yolo processing and uploading output image to s3 bucket')