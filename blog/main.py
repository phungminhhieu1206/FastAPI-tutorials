from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Dict


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@app.post('/blogs/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# GET_ALL
# Do ở đây .all() nên response_model là dạng List objects
@app.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
async def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# GET BY ID
# Ở đây .first() nên response_model là dạng 1 object
@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def get_by_id(id, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
    else:
        return blogs


# DELETE
@app.delete('/blogs/delete/{id}', status_code=status.HTTP_200_OK)
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f'Not records with id {id} in database')

    blog.delete(synchronize_session=False)
    db.commit()  # commit that transaction
    return {'status': 'delete done'}  # return response


# UPDATE
@app.put('/blogs/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not found')

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {'status': 'update done'}


# USER
@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
