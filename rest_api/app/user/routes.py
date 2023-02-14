from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import auth
from . import crud, schemas
from ..utility import generate_unique_id


router = APIRouter(
    prefix="/users",
    tags=["users"],
    generate_unique_id_function=generate_unique_id
)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    return auth.initiate_cognito_auth(username=form_data.username, password=form_data.password)


@router.post("/create")
def create_user(user: schemas.UserCreate) -> schemas.User:
    if crud.get_user_by_email(email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        cognito_id = auth.create_cognito_user(username=user.email, password=user.password)
    except Exception as error:
        raise HTTPException(status_code=504, detail=str(error), headers={"X-Error": str(error)})

    try:
        return crud.create_db_user(user=user, cognito_id=cognito_id)
    except Exception as error:
        raise HTTPException(status_code=504, detail=str(error), headers={"X-Error": str(error)})


@router.get("/get", dependencies=[Depends(auth.admin)])
def get_all_users() -> list[schemas.User]:
    try:
        return crud.get_all_users()
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/get/{email_address}", dependencies=[Depends(auth.admin)])
def get_user(email_address: str) -> schemas.User:
    try:
        db_user = crud.get_user_by_email(email=email_address)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return db_user


@router.get("/user-auth", dependencies=[Depends(auth.user)])
async def check_user_auth() -> dict[str, str]:
    return {"authorized": "true"}


@router.get("/admin-auth") 
async def check_admin_auth(claims: dict = Depends(auth.admin)) -> dict:
    return claims
