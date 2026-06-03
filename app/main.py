from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
                                password="wasd" , cursor_factory=RealDictCursor)
        cursor = conn.cursor() #Used to execute sql statements
        print("Database connection was successfull !")
        break
    except Exception as error:
        print("Connecting to database failed :/")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1},
            {"title":"Favourite foods", "content":"Pizza Yum Yum", "id":2}]

@app.get("/")
def root():
    return {"message" : "Welcome to my api"}

@app.get("/posts")
def get_posts():
    
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    
    # return{"data": "These are your posts"}
    # return {"data": my_posts}
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post":f"Title: {payLoad['title']}  Content: {payLoad['content']}"}
# title str, content str

# def create_posts(new_post: Post):
#     print(new_post)
#     print(new_post.content)
#     return {"data":"new post"}

# def create_posts(post:Post):
#     # print(post)
#     # print(post.dict())
#     post_dict = post.dict()
#     post_dict["id"] = randrange(1,100000001)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES 
                   (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts/{id}")
def get_post(id : int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    print(post)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} was not foundddd")
    return {"POST DETAIL": post}

    # post = find_post(id)

    # if not post:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message":f"Post with id: {id} was not found"}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"Post with id: {id} was not found")
    # return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone() 
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found...")
    
    return {"deleted content":deleted_post} 
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
                   WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    return {"data":updated_post}

    
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict

    # return {"data": post_dict}
