from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from .config import config

import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import time

from jose import jwk, jwt
from jose.utils import base64url_decode
from jose.exceptions import JWTError
import urllib.request


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_secret_hash(username: str) -> str:
    msg = username + config.APP_CLIENT_ID
    dig = hmac.new(str(config.APP_CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def initiate_cognito_auth(username: str, password: str) -> dict:
    secret_hash = get_secret_hash(username)
    client = boto3.client('cognito-idp')
    try:
        response = client.admin_initiate_auth(
            UserPoolId=config.USERPOOL_ID,
            ClientId=config.APP_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                # 'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            # ClientMetadata={
            #     'username': form_data.username,
            #     'password': form_data.password,
            # }
        )
    except client.exceptions.NotAuthorizedException:
        print("NotAuthorizedException")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except client.exceptions.UserNotConfirmedException:
        print("UserNotConfirmedException")
        raise HTTPException(status_code=400, detail="User Not Confirmed")
    except Exception as error:
        print("Exception: " + error.__str__())
        raise HTTPException(status_code=400, detail=error.__str__())

    # return response
    return {"access_token": response["AuthenticationResult"]["AccessToken"], "token_type": "bearer"}


def create_cognito_user(username: str, password: str) -> str:
    client = boto3.client("cognito-idp")
    try:
        response = client.sign_up(
            ClientId=config.APP_CLIENT_ID,
            # SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": username}
            ]
        )
    except Exception as error:
        raise error

    try:
        cognito_id = response.get('UserSub')
    except Exception as error:
        raise error

    return cognito_id


def confirm_sign_up(username: str) -> str:
    client = boto3.client("cognito-idp")
    try:
        response = client.admin_confirm_sign_up(
            UserPoolId=config.USERPOOL_ID,
            Username=username
        )
    except Exception as error:
        raise error

    try:
        cognito_id = response.get('UserSub')
    except Exception as error:
        raise error
    
    return cognito_id


def download_public_keys():
    # Instead of re-downloading the public keys every time
    # we download them only on cold start
    # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(config.AWS_REGION, config.USERPOOL_ID)
    try:
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
    except Exception as error:
        print('Error downloading public keys: ' + error.__str__())
        return None
        # raise HTTPException(status_code=401, detail="Error downloading public keys")

    keys = json.loads(response.decode('utf-8'))['keys']
    return keys

public_keys = download_public_keys()

async def verify_jwt(token: str, scopes: list, keys = public_keys):
    # Attempt to decode the token header
    try:
        headers = jwt.get_unverified_headers(token)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get the kid from the headers prior to verification.
    # The kid is a hint that indicates which key was used to secure the JSON web signature (JWS) of the token.     
    kid = headers['kid']

    if not keys:
        print('Public keys not found')
        raise HTTPException(status_code=401, detail="Public keys not found")

    # Search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        raise HTTPException(status_code=401, detail="Public key not found in jwks.json")

    # Construct the public key
    public_key = jwk.construct(keys[key_index])

    # Get the last two sections of the token, message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)

    # Decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    # Verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        raise HTTPException(status_code=401, detail="Signature verification failed")

    # Since we passed the verification, we can now safely use the unverified claims
    claims = jwt.get_unverified_claims(token)

    # Additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        raise HTTPException(status_code=401, detail="Token is expired")

    # And the client_id
    if claims['client_id'] != config.APP_CLIENT_ID:
        print('Token was not issued for this client')
        raise HTTPException(status_code=401, detail="Token was not issued for this client")

    # Verify scope
    for group in scopes:
        # If 'cognito:groups' key does not exist in claims, then user is in 'users' group
        if group in claims.get('cognito:groups', ['users']):
            return claims

    raise HTTPException(status_code=401, detail="Token was not authorized for this scope")


async def admin(token: str = Depends(oauth2_scheme)):
    try:
        return await verify_jwt(token=token, scopes=["admins"])
    except Exception as error:
        raise error


async def user(token: str = Depends(oauth2_scheme)):
    try:
        return await verify_jwt(token=token, scopes=["users", "admins"])
    except Exception as error:
        raise error

if __name__ == "__main__":
    print("create_cognito_user")