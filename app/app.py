from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key"  # Replace
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulated user database (para demo)
class UserInDB(BaseModel):
    username: str
    hashed_password: str

fake_users_db = {
    "user1": UserInDB(username="user1", hashed_password="hashed_password_1"),
    "user2": UserInDB(username="user2", hashed_password="hashed_password_2"),
}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token gen and valid
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        return db[username]

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoints
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(oauth2_scheme)):
    return {"username": current_user}

@app.post("/register")
async def register_user(username: str, password: str):
    # Check if the username already exists
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password
    hashed_password = get_password_hash(password)
    
    # Create a new user
    new_user = UserInDB(username=username, hashed_password=hashed_password)
    
    # Store the new user in the database (en memoria, por simplicidad)
    fake_users_db[username] = new_user
    
    return {"message": "User registered successfully"}

@app.get("/")
async def read_root():
    return {"message": "Hello, voting API!"}
