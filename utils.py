from jose import jwt,JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException,Depends
from datetime import datetime, timedelta
from models.support_model import SupportCase

SECRET_KEY = "chandana2003"
ALGORITHM = "HS256"
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):


    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
def jwt_bearer_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = decode_jwt_token(token)
    return payload  

def generate_case_id():
    last_case = SupportCase.objects.order_by("-case_id").first()
    if last_case and last_case.case_id.startswith("INC"):
        last_number = int(last_case.case_id.replace("INC", ""))
        new_number = last_number + 1
    else:
        new_number = 250000 
    return f"INC{new_number}"
