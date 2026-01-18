from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from app.database import Base, engine
from app.insert_data import insert_sample_data
from app.routers import metrics, sensors


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    insert_sample_data()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(sensors.router)
app.include_router(metrics.router)


@app.get("/")
def read_root():
    return {"Welcome to my weather metrics rest API."}


# Custome handler, at the moment using the fastapi provided one
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"

    return PlainTextResponse(message, status_code=422)
