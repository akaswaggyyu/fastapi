from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    #write it here instead of writing it every time in the decorator 
    prefix="/posts",
    tags=['Posts']
    
)
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model= List[schemas.PostOUT])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    #if we wanted to only display posts for currrent user
    #posts=db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    #posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#can add the status code to the decorator 
#post turns into a pydantic model
#pydantic model has .dict() function to turn data into a dictionary
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    new_post=models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    #refresh is like returning *
    db.refresh(new_post)
#     cursor.execute("""INSERT INTO posts (title, content, is_published) 
#     VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
# #make sure to commit to save the data on database
#     conn.commit()
    return new_post
#for updates, PUT request requires change to all the info
#a patch request can update a certain item

#to get a specific post, use "/posts/{id}"
#{id} is a path parameter 
#id is passed as a str so need to convert to int
#can use : in parameter to make sure it is an int
@router.get("/{id}", response_model= schemas.PostOUT)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                 detail=f"post with {id} was not found")
    #use bottom code if you want only logged in user to see each post
    # if post.user_id != current_user.id :
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
    #     detail="Not Authorized to Perform Action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist")
    if post_query.first().user_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
        detail="Not Authorized to Perform Action")
    post_query.delete(synchronize_session=False)
    db.commit()
    #when you delete you should not be sending any data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s 
    # WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post=cursor.fetchone()
    post_query= db.query(models.Post).filter(models.Post.id == id)
    postf = post_query.first()
    if postf == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not exist")
    if postf.user_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
        detail="Not Authorized to Perform Action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()