

from fastapi import APIRouter, Query,status
from typing import List,Optional
from controllers.UserControllers import get_users,create_user
from schemas.user_schema import User,CreateUser
from schemas.user_schema import UserResponse,UserCreateResponse,PostUser
from fastapi.responses import JSONResponse
router = APIRouter(prefix="", tags=["Users"])

@router.get("/user/{user_id}", response_model=UserResponse, summary="Get user details")
def users(
user_id:int
):
    data = get_users(user_id)
    # if not data["id"]:
    #     return JSONResponse(
    #         status_code=404,
    #         content={"message": "No users found", "data": []}
    #     )
    # data["added_date"] = data["added_date"].isoformat()
    return JSONResponse(
        status_code=200,
        content=data
    )
@router.post("/api/register", response_model=PostUser, summary="Register user",status_code=status.HTTP_201_CREATED)
def add_user(user: CreateUser):
    return create_user(user)