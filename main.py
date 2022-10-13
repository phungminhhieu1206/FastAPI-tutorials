from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# problem when you get list blogs about 1 million items
@app.get('/blog')
def index(limit=10, published: bool = False):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


# static router need write above dynamic router
@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blogs'}


# dynamic router
@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    # fetch comments of blog with id = id
    return {'data': {
        'blog_id': id,
        'comments': 'list comments'
    }}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog/create')
def create_blog(blog: Blog):
    return 'done'
