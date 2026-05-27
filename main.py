from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None 

@app.get("/")
def root():
    return {"message" : "Welcome to my api"}

@app.get("/posts")
def get_posts():
    return{"data": "These are your posts"}

@app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post":f"Title: {payLoad['title']}  Content: {payLoad['content']}"}
# title str, content str

def create_posts(new_post: Post):
    print(new_post)
    print(new_post.content)
    return {"data":"new post"}