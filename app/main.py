from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth, vote 
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#this was used to create all the tables but now we are using alembic to do that
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


#the / in get() means this is what it gets when you go to website.com/ 
#unicorn main:app activates the server
#if you add --reload it will change the server on demand
@app.get("/")
async def root():
    return {"message": "welcome to my api"}


