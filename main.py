from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "devops-webscraping no ar"}


@app.get("/random")
async def root():
    return {"teste": True, "num_aleatorio": random.randint(0, 100)}
