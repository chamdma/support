from fastapi import FastAPI, Depends
from routes import support_routes
from utils import jwt_bearer_auth


from database import *




app=FastAPI()


app.include_router(support_routes.router,dependencies=[Depends(jwt_bearer_auth)])


