import logging
from fastapi import FastAPI, Request, Response
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

# Configure logging
logger = logging.getLogger(__name__)
logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s - %(message)s",
    filename='logs.txt'
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGO_URL"])
    app.database = app.mongodb_client[config["MONGO_DB"]]
    print("connect successful")

@app.middleware("http")
async def loggingInfo(request: Request, call_next, response : Response):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"{request.client} -  method: {request.method} - path: {request.scope['path']}- status_code: {response.status_code} - process_time: {process_time}")
    return response

@app.exception_handler(Exception)
async def handle_500_errors(request, exc):
    logger.error(f"500 Internal Server Error: {exc}")
    return {"detail": "Internal Server Error"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("server shutdown")


# including the router
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)