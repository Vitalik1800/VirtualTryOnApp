from fastapi import FastAPI

from server.database.base import Base
from server.database.connection import engine
from server.api.accessories import router as accessories_router
from server.api.try_on import router as try_on_router


app = FastAPI(
    title="Virtual Try-On API",
    version="1.0"
)

Base.metadata.create_all(
    bind=engine
)

app.include_router(
    accessories_router
)

app.include_router(
    try_on_router
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Virtual Try-On API is running"
    }
