import uuid
from typing import Optional #the type can be anything
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    JWTStrategy,
    BearerTransport
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db
import dotenv
dotenv.load_dotenv()
import os

SECRET = os.getenv("SECRET_KEY")

#UUIDIDMixin -> Adds support for UUID instead of default int IDs
#this class is responsible for managing user-related operations such as creating users, resetting passwords, and verifying accounts. It inherits from BaseUserManager and UUIDIDMixin to provide these functionalities while using UUIDs for user identification.
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
    
    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
    
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_stratergy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)#seconds

#authBack is responsible for handling the authentication process, it uses the BearerTransport to receive the token from the client and the JWTStrategy to verify the token and get the user information from it. The name "jwt" is just an identifier for this authentication backend, it can be anything you want.
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_stratergy
)

#FastAPIUsers = core engine that wires your user system into FastAPI so you can use auth features easily.
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
#this will create the dependency that we can use in our routes to get the current active user, it will check if the user is authenticated and active, if not it will return an error, if yes it will return the user information.
current_active_user = fastapi_users.current_user(active=True)