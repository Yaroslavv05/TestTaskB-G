from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.v1.crud import create_post, get_post, get_posts, update_post, delete_post
from app.db.schemas import PostCreate, PostUpdate, Post as PostSchema
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts/", response_model=PostSchema)
def create_post_route(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db=db, title=post.title, content=post.content)

@router.get("/posts/{post_id}", response_model=PostSchema)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/posts/", response_model=List[PostSchema])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts

@router.put("/posts/{post_id}", response_model=PostSchema)
def update_post_route(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = update_post(db, post_id=post_id, title=post.title, content=post.content)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.delete("/posts/{post_id}", response_model=PostSchema)
def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    db_post = delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
