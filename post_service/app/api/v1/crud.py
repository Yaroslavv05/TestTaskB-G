from sqlalchemy.orm import Session
from app.db.models import Post

def create_post(db: Session, title: str, content: str):
    db_post = Post(title=title, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def update_post(db: Session, post_id: int, title: str, content: str):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.title = title
        db_post.content = content
        db.commit()
        db.refresh(db_post)
        return db_post
    return None

def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post
    return None
