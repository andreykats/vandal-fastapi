from pynamodb.exceptions import DoesNotExist, DeleteError, GetError, ScanError, QueryError, TableError, TableDoesNotExist
from . import models, schemas
from datetime import datetime
from typing import Optional

# -----------------------
# DynamoDB CRUD functions
# -----------------------


def get_all_users() -> list[schemas.User]:
    try:
        user_list = []
        for user in models.UsersTable.scan():
            user_list.append(schemas.User(**user.attribute_values))
        return user_list
    except ScanError as error:
        raise error
    except Exception as error:
        raise error


def get_user_by_email(email: str) -> Optional[schemas.User]:
    try:
        user_list = []
        for model in models.UsersTable.query(email):
            user_list.append(schemas.User(**model.attribute_values))

        if not user_list:
            return None
        else:
            return user_list[0]
    except Exception as error:
        raise error


def create_db_user(user: schemas.UserCreate, cognito_id: str) -> schemas.User:
    current_datetime = datetime.now()
    model = models.UsersTable(
        email=user.email,
        cognito_id=cognito_id,
        is_active=True,
        is_superuser=False,
        created_at=current_datetime
    )

    try:
        model.save()
        return schemas.User(**model.attribute_values)
    except Exception as error:
        raise error