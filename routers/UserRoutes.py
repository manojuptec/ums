

from fastapi import APIRouter,Header, Query,status
from typing import List,Optional
from controllers.UserControllers import get_users,create_user,login_user,user_logout
from schemas.user_schema import User,CreateUser
from schemas.user_schema import UserResponse,UserCreateResponse,PostUser,LoginUser,UserLogout
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
@router.post("/api/login", response_model=UserResponse, summary="Login user",status_code=status.HTTP_201_CREATED)
def user_login(user: LoginUser):
    data= login_user(user)
    return JSONResponse(
        status_code=200,
        content=data
    )
@router.post("/user/logout", response_model=UserLogout, summary="Logout User")
def logout(
    user_id: int = Query(..., description="User ID"),
    token: str = Header(..., description="User Token")
):
 data = user_logout(user_id,token)
 return JSONResponse(
        status_code=200,
        content=data
    )
