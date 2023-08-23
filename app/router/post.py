from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, utils, oauth2
from typing import Optional, List
from ..schemas import PostCreate, PostBase, Post, UserCreate, UserResponse, PostOut
from ..database import engine, get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


# A get route to get all posts!
# @router.get("/", response_model=List[Post])
@router.get("/", response_model=List[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


# POST route
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# GET one single post
@router.get("/{id}", response_model=PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(f""" SELECT * FROM posts WHERE id = %s """, (str(id)))

    # single_post = cursor.fetchone()

    single_post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    print(f"SINGLE POST: {single_post}")

    if not single_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found",
        )

    return single_post


# Delete a single post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()

    # Fetch the post with the id you want to delete
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    print(f"POST TO DELETE {post}")

    # If the post does not exist send a notification of the same
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The item with id {id} seems to have already been deleted!",
        )

    # Ensure the owner deletes their own posts
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to perform the requested action!",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@router.put("/{id}", response_model=Post)
def update_post(
    id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    # Ensure the owner updated only their own posts
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to perform the requested action!",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    # Return the updated post by searching a post with that id after update is complete
    return post_query.first()
