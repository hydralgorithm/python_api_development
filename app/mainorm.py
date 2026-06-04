from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", 
                                password="wasd", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database successfully connected!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("ERROR: ",error)
        time.sleep(3)

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate, db:Session=Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int, db:Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    return {"data":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post does not exist!")
    post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}")
def update_post(id:int,post:schemas.PostUpdate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}

