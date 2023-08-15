### Users API con autorización OAuth2 JWT ###

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWSError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# Genero número random con "openssl rand -hex 32" en la terminal
SECRET = "dae1747fe4ff5972f698bc0210dd2e69b9a16b8a15f7339fd0fdd1e557e9916c"

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "beaves83": {
        "username": "beaves83",
        "full_name": "Bibi Ruiz",
        "email": "bruiz@gmail.com",
        "disabled": False,
        "password": "$2a$12$2tKmRauBpLFizSVU7Jl.Vuu/ndoI/NVjqA83kREncRVeGhVq7VeXu"
    },
     "susuro": {
        "username": "susuro",
        "full_name": "Cristina Usero",
        "email": "cusero@gmail.com",
        "disabled": True,
        "password": "$2a$12$OiodAK/zq4gARPJ9EyBztuHOO/zGf9eBO0.tQ5//RWS48C6DwUbaa"
    }
}  

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autentificación inválidas", 
        headers={ "WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWSError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La contraseña no es correcta")
    
    access_token = { "sub" : user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
                    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type" : "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
