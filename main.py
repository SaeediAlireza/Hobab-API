from fastapi import FastAPI
import routers

from model import database, model
import routers.ages
import routers.authentication
import routers.category
import routers.caviar
import routers.caviar_breed
import routers.fish
import routers.fish_breed
import routers.item
import routers.length_class
import routers.location
import routers.pool
import routers.pool_type
import routers.quantity
import routers.shift
import routers.sub_category
import routers.task
import routers.transaction
import routers.user
import routers.user_type
import routers.weight_class
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
model.Base.metadata.create_all(database.engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routers.ages.router)
app.include_router(routers.authentication.router)
app.include_router(routers.caviar_breed.router)
app.include_router(routers.caviar.router)
app.include_router(routers.category.router)
app.include_router(routers.fish_breed.router)
app.include_router(routers.fish.router)
app.include_router(routers.item.router)
app.include_router(routers.length_class.router)
app.include_router(routers.location.router)
app.include_router(routers.pool_type.router)
app.include_router(routers.pool.router)
app.include_router(routers.quantity.router)
app.include_router(routers.shift.router)
app.include_router(routers.sub_category.router)
app.include_router(routers.task.router)
app.include_router(routers.transaction.router)
app.include_router(routers.user_type.router)
app.include_router(routers.user.router)
app.include_router(routers.weight_class.router)
