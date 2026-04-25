from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from app.db import Post, get_async_session, create_db_and_tables, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import uuid
import shutil
import os
import tempfile
from app.users import current_active_user, fastapi_users, auth_backend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    
    
# this will create db whenever the application start
app = FastAPI(lifespan=lifespan)

#here the fastapi_user.. automatically creates routes(like POST and etc)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]) #tags help to group the routes in the documentation, it is optional
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])



@app.post("/upload")
async def upload_file(
    file: UploadFile= File(...), #here three dots meann an object
    caption: str = Form(""),
    #to give access to only signed in personwe will use this depInjection adn give access
    user: User= Depends(current_active_user),
    session: AsyncSession= Depends(get_async_session), #it is Depedency injection, it will inject the session in the function, so that we can use it to interact with the database
):
    
    temp_file_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        upload_result = imagekit.upload_file(
            file = open(temp_file_path, "rb"),
            file_name = file.filename,
            options = UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        if upload_result.response_metadata.http_status_code==200:
            post = Post(
                user_id = user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)# like staging it
            await session.commit() #same as git
            await session.refresh(post) #it will refresh and render the db changes if there are any..
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path) #this will delete the temporary file after uploading it to imagekit
        file.file.close()
        

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session), #to get access to db
    user: User= Depends(current_active_user)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()] #here all the feed list will be available(row-> ___->___ so we took list)
    
    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    
    user_dict = {u.id:u.email for u in users}
    
    posts_data = []
    for post in posts :
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(user.id),
                "caption": post.caption,
                "url": post.url,
                "file_name": post.file_name,
                "file_type": post.file_type,
                "created_at":post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
        
    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str, 
    session: AsyncSession = Depends(get_async_session),
    user: User= Depends(current_active_user)
):
    try:
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id== post_uuid))
        #scalar() is used to get the first column of the first row of the result, and first() is used to get the first row of the result, so it will return the post object if it exists, otherwise it will return None
        #scalars() is used to get all the rows of the result as a list of objects, and first() is used to get the first object from the list, so it will return the post object if it exists, otherwise it will return None
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You dont have permission to delete this post")
        
        await session.delete(post)
        await session.commit()
        
        return {"success": True, "message": "Post was successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))