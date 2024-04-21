# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring,C0301:line-too-long
# pylint: disable=W0612:unused-variable,W0707:raise-missing-from
# import asyncio
# from datetime import datetime
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import HTTPException#,Depends
from jose import jwt,JWTError
import bcrypt
# import uuid
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import scoped_session
from app.db.models.user_model import User
# from fastapi import Cookie


class CurrUser:
    def __init__(self,user_id,email,firstname='',lastname=''):
        self.user_id = user_id
        self.email = email
        self.firstname=firstname
        self.lastname = lastname

class UserService:
    def __init__(self):
        self.secret_key = "your-secret-key"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 1440
        self.cookie_expire_seconds =86400 # 24hours

    def get_current_user(self,token):
        '''
        get_current_user
        '''
        if token is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = self.decode_token(token)
            email: str = payload.get("sub")
            # task_id: str = payload.get("task_id")
            firstname: str = payload.get("firstname")
            lastname: str = payload.get("lastname")
            user_id:int=payload.get("user_id")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        # curr_user=CurrUser(email,task_id,firstname,lastname)
        curr_user=CurrUser(user_id,email,firstname,lastname)
        return curr_user

    async def register(self,firstname: str,lastname: str,email: str,password: str,db:scoped_session):
        '''
        register
        '''
        try:
            # self.user_is_allowed(email,db)
            hashed_password = self.get_password_hash(password)
            db_user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_password
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)# Refresh user object to get the auto-incremented ID
            # db_task=Task(user_id=db_user.id)
            # db.add(db_task)
            db.commit()
            # db.refresh(db_task)
            return {"firstname": db_user.firstname,"lastname":db_user.lastname,"email":db_user.email}
        except IntegrityError as e:
            # Check if the exception is due to a unique constraint violation
            if "UNIQUE constraint failed: user.email" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists",
                )
            else:
                # Handle other IntegrityError cases if needed
                raise HTTPException(
                    status_code=500,
                    detail="Internal Server Error",
                )

    def login(self,email: str, password: str, db: Session):
        '''
        login
        '''
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user or not self.verify_password(password, db_user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        # print(f"Task: {db_user.task[0].id}")
        access_token = self.create_jwt_token(data={"user_id":db_user.id,"sub": email,"firstname":db_user.firstname,"lastname":db_user.lastname}, expires_delta=access_token_expires)

        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer","email":email,"firstname":db_user.firstname,"lastname":db_user.lastname})
        # Set the token in a cookie
        # response.set_cookie(domain="127.0.0.1",key="cxc_access_token", value=access_token,max_age=self.COOKIE_EXPIRE_SECONDS)
        # response.set_cookie(domain="stacitswd1.sauwi.uwi.tt",key="cxc_access_token", value=access_token,max_age=self.COOKIE_EXPIRE_SECONDS)
        # response.set_cookie(domain="localhost",key="cxc_access_token", value=access_token,max_age=self.COOKIE_EXPIRE_SECONDS)
        return response

    def decode_token(self,token):
        '''
        decode_token
        '''
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    # JWT settings
    def create_jwt_token(self,data: dict, expires_delta: timedelta = None):
        '''
        create_jwt_token
        '''
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    # Hash a password using bcrypt
    def get_password_hash(self,password:str):#https://github.com/pyca/bcrypt/issues/684#issuecomment-1902590553
        '''
        get_password_hash
        '''
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    # Check if the provided password matches the stored password (hashed)
    def verify_password(self,plain_password, hashed_password):
        '''
        verify_password
        ## [bcrypt](https://github.com/pyca/bcrypt/issues/684#issuecomment-1902590553)
        '''
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)
