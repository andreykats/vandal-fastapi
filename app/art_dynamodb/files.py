import os
import base64
import shutil
import typing


async def save_image_data(file_name: str, image_data: str) -> str:
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


async def save_image_file(file_name: str, image_file: typing.BinaryIO) -> str:
    try:
        # Save image to disk
        with open("./images/" + file_name, "wb") as buffer:
            shutil.copyfileobj(image_file, buffer)
            return file_name
    except Exception as error:
        raise error


async def delete_file(file_name: str) -> str:
    try:
        os.remove("./images/" + file_name)
    except Exception as error:
        raise error
