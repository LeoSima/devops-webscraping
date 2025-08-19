from fastapi import FastAPI
from app.api import scraping

app = FastAPI(
    title="DevOps WebScraping API",
    description="API simples desenvolvida para estudar e demonstrar conceitos de DevOps com web scraping",
    version="0.1.0"
)

app.include_router(scraping.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"welcome": "Acesse /docs para ver a documentação da API."}
