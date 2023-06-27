from typing import List
from fastapi import APIRouter, status, Request, Body, HTTPException, Response, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
import datetime
from models.user import UserSchema, UpdateUserSchema

config = dotenv_values(".env")

router = APIRouter()
time = datetime.datetime.now()

def write_notification(_id: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"api for {_id}: {message}"
        email_file.write(content)

@router.get("/users", response_description="All users", response_model=List[UserSchema])
def all_users(request: Request):
    users = list(request.app.database[config["MONGO_COL"]].find({}))
    return users



@router.get("/user/{id}", response_description="user by id", response_model=UserSchema)
def get_user(id: str, request: Request, background_tasks: BackgroundTasks):
    users = request.app.database[config["MONGO_COL"]].find_one({"_id": id})
    background_tasks.add_task(write_notification,{id},message = "log " + str(time))
    return users


@router.post("/user/add", response_description="Create new user", status_code=status.HTTP_201_CREATED,response_model=UserSchema)
def create_user(request: Request, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database[config["MONGO_COL"]].insert_one(user)
    created_user = request.app.database[config["MONGO_COL"]].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user



@router.post("/collection/add", response_description="Create new collection", status_code=status.HTTP_201_CREATED)
def create_collection(name: str,request: Request):
    new_collection = request.app.database.create_collection(name)
    config["MONGO_COL"] = name
    return new_collection

@router.put("/user/{id}", response_description="Update a user", response_model=UpdateUserSchema)
def update_user(id: str, request: Request, user: UpdateUserSchema = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database[config["MONGO_COL"]].update_one(
            {"_id": id}, {"$set": user}
        )
        if update_result.modified_count == 0:
            return "User not found"
    if (
            exist_user := request.app.database[config["MONGO_COL"]].find_one({"_id": id})
    ) is not None:
        return exist_user

    return "User not found"



@router.delete("/user/{id}", response_description="Delete a user")
def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database[config["MONGO_COL"]].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return "User not found"
