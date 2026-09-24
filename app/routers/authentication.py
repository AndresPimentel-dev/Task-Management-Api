from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.models import UsersTable
from app.schemas import TokenResponse, UserCreate

router = APIRouter(prefix="/api/v1.0", tags=["Authentication"])

# ==========================================
#          ENDPOINTS DE AUTENTICACIÓN
# ==========================================


@router.post("/auth/register", status_code=201, response_model=TokenResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    email = db.query(UsersTable).filter(UsersTable.email == user_data.email).first()
    username = (
        db.query(UsersTable).filter(UsersTable.username == user_data.username).first()
    )
    if email or username:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_pwd = get_password_hash(plain_password=user_data.password)
    new_user = UsersTable(
        username=user_data.username, email=user_data.email, hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login", status_code=200, response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    user = (
        db.query(UsersTable).filter(UsersTable.username == form_data.username).first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
