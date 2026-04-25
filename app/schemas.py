from pydantic import BaseModel
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title: str
    content: str
    
class PostResponse(BaseModel):
    title:str
    content:str
    
#this class is for the user response, it inherits from the BaseUser class provided by fastapi_users and we are using uuid as the id type for the user.
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
#this class is for the user creation, it inherits from the BaseUserCreate class provided by fastapi_users and it will take the email and password as input and create a new user in the database.
class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
