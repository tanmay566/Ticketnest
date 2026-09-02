import os 
from datetime  import datetime, timedelta , timezone


from passlib.context import CryptContext
from jose import jwt 

SCERET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-")
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 60 *24  

pwd_context  = CryptContext(schemas =["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str , hasehd_password:str) -> bool :
    return pwd_context.verify(plain_password , hasehd_password)
def create_access_token(user_id:int)-> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes = ACESS_TOKEN_EXPIRE_MINUTES

    )
    payload = {
        "sub":str(user_id),
        "exp": expire

    }
    token = jwt.encode(payload, SCERET_KEY, algorithm=ALGORITHM)
    return token