from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app import models 
from app.database import get_db
from app.security import SECRET_KEY , ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate credentials",
        headers={"WWW-Authenticate":"Bearer"},

    )
    try:
        payload =jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]

        )
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        user_id  =int(user_id)
    except JWTError:
        raise credentials_exception

    except ValueError:
        raise credentials_exception

    user = db.get(models.User, user_id)
    if user is None:
        raise credentials_exception
    return user

def get_current_organizer(
        current_user : models.User = Depends(get_current_user)
):
    if current_user.role not in ["organizer" , "admin"]:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Only organizers can perform this action"
        )

    return current_user
