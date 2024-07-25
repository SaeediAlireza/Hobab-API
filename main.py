from fastapi import FastAPI
import routers

from model import database, model
import routers.authentication

app = FastAPI()
model.Base.metadata.create_all(database.engine)


app.include_router(routers.authentication.get_router())
