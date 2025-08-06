from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "devops-webscraping no ar"}
