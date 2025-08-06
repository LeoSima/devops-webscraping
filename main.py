from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.get("/HealthCheck")
async def healthCheck():
    return {"message": "devops-webscraping no ar"}
