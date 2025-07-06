#!/usr/bin/env python3

import boto3
from pathlib import Path
import yaml
import shutil
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
access_key_id = os.getenv("access_key_id")
secret_key = os.getenv("secret_key")


with open("backup_config.yaml") as stream:
    files = yaml.safe_load(stream)

backup_paths = files['backups']
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

S3_BUCKET = "bucket-yc-rxdeye"


all_backups = []

for path in backup_paths:
    if os.path.exists(path):
        base_name = os.path.basename(os.path.normpath(path))
        archive_path = "/home/redeye/Desktop/backup_python/"
        archive_name = f"backup_{base_name}_{timestamp}"
        full_path = os.path.join(archive_path,archive_name)
        shutil.make_archive(archive_name, 'gztar', path)
        all_backups.append(full_path + ".tar.gz") 

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id = access_key_id,
    aws_secret_access_key = secret_key
    )

for file_path in all_backups:
    s3.upload_file(file_path,S3_BUCKET,os.path.basename(file_path))

for file_path in all_backups:
    os.remove(file_path)




