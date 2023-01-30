import os
import base64
import shutil
import typing

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

ACCESS_KEY = 'AKIAVNGMWN72PYV3Z25H'
SECRET_KEY = '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'
BUCKET_NAME = 'vandal-images-bucket-stage'

async def save_image_data_to_disk(file_name: str, image_data: str) -> str:
    try:
        # Convert string to bytes
        bytes = str.encode(image_data)

        # Decode base64string back to image
        base64_bytes = base64.b64decode(bytes)

        # Save image to disk
        with open("./images/" + file_name, "wb") as buffer:
            buffer.write(base64_bytes)
            return file_name
    except Exception as error:
        raise error


async def save_image_data_to_s3(file_name: str, image_data: str) -> str:
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    # Convert string to bytes
    bytes = str.encode(image_data)

    # Decode base64string back to image
    base64_bytes = base64.b64decode(bytes)

    # Upload the file
    try:
        response = s3.put_object(Body=base64_bytes, Bucket=BUCKET_NAME, Key=file_name, ContentType='image/jpeg')
        return response
    except ClientError as error:
        raise error

    
async def save_image_file_to_s3(file_name: str, image_file: typing.BinaryIO) -> str:
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        response = s3.upload_file(image_file, BUCKET_NAME, file_name)
        return response
    except ClientError as error:
        raise error



async def save_image_file_to_disk(file_name: str, image_file: typing.BinaryIO) -> str:
    try:
        # Save image to disk
        with open("./images/" + file_name, "wb") as buffer:
            shutil.copyfileobj(image_file, buffer)
            return file_name
    except Exception as error:
        raise error


async def delete_file_from_disk(file_name: str) -> str:
    try:
        os.remove("./images/" + file_name)
        return file_name
    except Exception as error:
        raise error
