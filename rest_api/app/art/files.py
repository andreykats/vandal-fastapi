import os
import base64
import shutil
import typing

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from ..config import config


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
    # # Save image to disk if development environment
    # if config.S3_HOST:
    #     try:
    #         await save_image_data_to_disk(file_name, image_data)
    #     except:
    #         pass

    # Create an S3 client
    s3 = boto3.client('s3', endpoint_url=config.S3_HOST, aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    # Convert string to bytes
    bytes = str.encode(image_data)

    # Decode base64string back to image
    base64_bytes = base64.b64decode(bytes)

    # Upload the file
    try:
        response = s3.put_object(Body=base64_bytes, Bucket=config.S3_BUCKET_IMAGES, Key=file_name, ContentType='image/jpeg')
        return response
    except ClientError as error:
        raise error

    
async def save_image_file_to_s3(file_name: str, image_file: typing.BinaryIO) -> str:
    # Save image to disk if development environment
    if config.S3_HOST:
        try:
            await save_image_file_to_disk(file_name, image_file)
        except:
            pass

    s3 = boto3.client('s3', endpoint_url=config.S3_HOST, aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    try:
        # response = s3.upload_file(image_file, config.S3_BUCKET_IMAGES, file_name)
        response = s3.upload_file(file_name=image_file, Bucket=config.S3_BUCKET_IMAGES, Key=file_name, ExtraArgs={'ContentType': 'image/jpeg'})
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
