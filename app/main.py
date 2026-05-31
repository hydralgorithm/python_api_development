from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1},
            {"title":"Favourite foods", "content":"Pizza Yum Yum", "id":2}]

@app.get("/")
def root():
    return {"message" : "Welcome to my api"}

@app.get("/posts")
def get_posts():
    # return{"data": "These are your posts"}
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post":f"Title: {payLoad['title']}  Content: {payLoad['content']}"}
# title str, content str

# def create_posts(new_post: Post):
#     print(new_post)
#     print(new_post.content)
#     return {"data":"new post"}

def create_posts(post:Post):
    # print(post)
    # print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(1,100000001)
    my_posts.append(post_dict)
    return {"data": post_dict}

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
    print(type(id))
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}

# Commented