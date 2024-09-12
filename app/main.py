from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title 1", "content": "content 1", "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i
        
#path oprator function
@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000) 
    my_posts.append(post_dict)
    return {
        "data": my_posts
    }
    
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int,):
    
    post = find_post(id)
    if not post : 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {
        "post_detail": post
    }
    
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int,):
   postIndx = find_index_post(id)
   if postIndx == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
   my_posts.pop(postIndx)
   return  Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    print(post)
    #find the index
    index = find_index_post(id)
    # if the index is not found
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    #convert to dic
    post_dic = post.model_dump()
    #update the list
    my_posts[index] = post_dic
    
    return {
        "data": post_dic
    }