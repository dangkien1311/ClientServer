import asyncio
import logging
from typing import List
from fastapi import APIRouter, status, Request, Body, HTTPException, Response, BackgroundTasks, FastAPI
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
from fastapi.responses import JSONResponse
import datetime
from models.user import UserSchema, UpdateUserSchema, EventSchema

config = dotenv_values(".env")

router = APIRouter()
app = FastAPI()
time = datetime.datetime.now()
lst_event = [] 

# def write_notification(_id: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"api for {_id}: {message}"
#         email_file.write(content)
# def addEvent(request: Request):
#     for req in lst_event:
#         request.app.database[config["MONGO_COL_EVENT"]].insert_one(req)

@router.get("/users", response_description="All users", response_model=List[UserSchema])
async def all_users(request: Request):
    users = list(request.app.database[config["MONGO_COL_USER"]].find({}))
    # logging.info(f"{request.method} {response.status_code}")
    return users

@router.get("/events", response_description="All events", response_model=List[EventSchema])
async def all_users(request: Request):
    users = list(request.app.database[config["MONGO_COL_EVENT"]].find({}))
    return users



@router.get("/user/{id}", response_description="user by id", response_model= UserSchema)
async def get_user(id: str, request: Request):
    users = request.app.database[config["MONGO_COL_USER"]].find_one({"_id": id})
    return users

@router.get("/event/{id}", response_description="event by id", response_model= EventSchema)
async def get_user(id: str, request: Request):
    event = request.app.database[config["MONGO_COL_EVENT"]].find_one({"_id": id})
    # background_tasks.add_task(write_notification,{id},message = "log " + str(time))
    return event


@router.post("/user/add", response_description="Create new user", status_code=status.HTTP_201_CREATED,response_model=UserSchema)
async def create_user(request: Request, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database[config["MONGO_COL_USER"]].insert_one(user)
    created_user = request.app.database[config["MONGO_COL_USER"]].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user

@router.post("/event/add", response_description="add new event", status_code=status.HTTP_201_CREATED,response_model=EventSchema)
async def add_event(request: Request ,event: EventSchema = Body(...)):
    event = jsonable_encoder(event)
    lst_event.append(event)
    if len(lst_event) == 3:
        request.app.database[config["MONGO_COL_EVENT"]].insert_many(lst_event)
        lst_event.clear()
    # new_event = request.app.database[config["MONGO_COL_EVENT"]].insert_one(event)
    # add_event = request.app.database[config["MONGO_COL_EVENT"]].find_one(
    #     {"_id": new_event.inserted_id}
    # )
    return event

@router.post("/collection/user", response_description="Create new user collection", status_code=status.HTTP_201_CREATED)
async def create_collection(name: str,request: Request):
    request.app.database.create_collection(name)
    config["MONGO_COL_USER"] = name
    return f"Collection {name} is created"

@router.post("/collection/event", response_description="Create new event collection", status_code=status.HTTP_201_CREATED)
async def create_collection(name: str,request: Request):
    request.app.database.create_collection(name)
    config["MONGO_COL_EVENT"] = name
    return f"Collection {name} is created"

@router.put("/user/{id}", response_description="Update a user", response_model=UpdateUserSchema)
async def update_user(id: str, request: Request, user: UpdateUserSchema = Body(...)):
    jsuser = jsonable_encoder(user)

    if not request.app.database[config["MONGO_COL_USER"]].find_one({"_id": id}):
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        request.app.database[config["MONGO_COL_USER"]].update_one(
                {"_id": id}, {"$set": jsuser}
            )
        result = request.app.database[config["MONGO_COL_USER"]].find_one({"_id": id})
        return result
    except Exception as e:
        return {"message": str(e)}, 500


@router.delete("/user/{id}", response_description="Delete a user")
async def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database[config["MONGO_COL_USER"]].delete_one({"_id": id})
    fail_result =  response.status_code = status.HTTP_204_NO_CONTENT
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_202_ACCEPTED
        return response

    return fail_result

@router.delete("/event/{id}", response_description="Delete a event")
async def delete_event(id: str, request: Request, response: Response):
    delete_result = request.app.database[config["MONGO_COL_EVENT"]].delete_one({"_id": id})
    fail_result =  response.status_code = status.HTTP_204_NO_CONTENT
    print(type(delete_result))
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_202_ACCEPTED
        return response
    
    return fail_result