from fastapi import FastAPI


app = FastAPI(
    title="Virtual Try-On API",
    version="1.0"
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Virtual Try-On API is running"
    }
