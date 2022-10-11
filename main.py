from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': 'list blogs'}


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
