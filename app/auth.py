from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, database

# Configuración
SECRET_KEY = "AntigravityKey_2026_Taller" # En producción usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hora de sesión

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def validate_password_strength(password: str):
    # Política Flexible corregida: Min 6 caracteres (Beta)
    if len(password) < 6:
        raise ValueError("La clave debe tener al menos 6 caracteres")
    return True

def handle_failed_login(db: Session, user: models.User):
    user.failed_attempts += 1
    if user.failed_attempts >= 3:
        user.status = 'Suspendido'
    db.commit()

def reset_failed_login(db: Session, user: models.User):
    user.failed_attempts = 0
    db.commit()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependencia para obtener el usuario actual desde la Cookie
async def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    # Quitar el prefijo 'Bearer ' si existe
    if token.startswith("Bearer "):
        token = token[7:]
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Middleware-like checker para Roles
def check_role(roles_allowed: list):
    async def role_checker(current_user: models.User = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(status_code=302, detail="No autenticado", headers={"Location": "/NucleoTallerV1/login"})
        
        user_roles = [r.name for r in current_user.roles]
        if not any(role in roles_allowed for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta acción"
            )
        return current_user
    return role_checker
