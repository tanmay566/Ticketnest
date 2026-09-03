from fastapi import APIRouter, Depends , HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models ,schemas , security 
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags = ["Auth"])

@router.post(
    "/register",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(payload : schemas.UserCreate, db:Session = Depends(get_db)):
    existing_user = db.query(models.User),filter(
        models.User.email ==payload.email

    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = security.hash_password(payload.password)
    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed_password,
        role =payload.role 
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data : OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"},
        
)
    is_password_valid  = security.verify_password(
        form_data.password,
        user.hashed_password
    )
    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(user.id)
    return{
        "acess-token":access_token,
        "token_type": "bearer"
    }
@router.get("/me", response_model=schemas.UserOut)
def read_me (current_user : models.User =Depends(get_current_user)):
    return current_user