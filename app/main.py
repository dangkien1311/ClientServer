from fastapi import FastAPI, Request
from routes import routes
from dotenv import dotenv_values
from pymongo import MongoClient
import uvicorn
import time
import threading
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

config = dotenv_values(".env")

app = FastAPI()

# class BackgroundTasks(threading.Thread):
#     def run(self,*args,**kwargs):
#         while True:
#             print('Hello')
#             time.sleep(5)
            

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGO_URL"])
    app.database = app.mongodb_client[config["MONGO_DB"]]
    # t = BackgroundTasks()
    # t.start()
    print("connect successful")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("server shutdown")

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
  return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))

# including the router
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)