from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class method2post(BaseModel):
    message : str
    id : int
    income : float
    is_retarded : bool = False
    not_dumb : Optional[bool] = None

@app.get("/")
def demo():
    return {"message" : "This is a practice read."}

@app.post("/demopost")
def postahh(post_meth1: dict = Body(...)):
    print(post_meth1)
    return {f"Wow! you made a {post_meth1["order"]} post request, Congrats on your {post_meth1["analysis"]}"}

@app.post("/alsodemopost")
def postahhh(meth: method2post):
    print(meth)
    return {"Info":f"Inc-{meth.income}, broke?"}