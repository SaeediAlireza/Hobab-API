from fastapi import FastAPI
import routers

from model import database, model
import routers.authentication
import routers.user
import routers.user_type
from util import util

app = FastAPI()
model.Base.metadata.create_all(database.engine)
db = util.get_db()

app.include_router(routers.authentication.get_router(db))
app.include_router(routers.user.get_router(db))
app.include_router(routers.user_type.get_router(db))
