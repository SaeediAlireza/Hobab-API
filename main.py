from fastapi import FastAPI
import routers

from model import database, model
import routers.authentication
import routers.quantity
import routers.user
import routers.user_type


app = FastAPI()
model.Base.metadata.create_all(database.engine)

app.include_router(routers.authentication.router)
app.include_router(routers.user.router)
app.include_router(routers.user_type.router)
app.include_router(routers.quantity.router)
