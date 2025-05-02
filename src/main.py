import uvicorn
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import (
    users,
    auth,
    posts,
    reactions
)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(reactions.router)

models.Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)