from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.helpers.log_helper import debug_log
from sqlalchemy.orm import Session

from app.schemas.token_schema import Token
from app.database import get_db

router = APIRouter()


@router.post("/token",
             response_model=Token,
             operation_id='token',
             tags=['auth'])
@debug_log
async def token_from_username_and_password(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)) -> Token:

    if form_data.username == "admin" and form_data.password == "password":
        return Token(access_token="accsess_token")
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
