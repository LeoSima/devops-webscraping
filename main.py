from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WebScrapingConfig(BaseModel):
    filtro: str
    limite: int
    ordenacao: str

@app.get("/HealthCheck")
async def health_check():
    return {"message": "devops-webscraping no ar"}

@app.post("/WebScraping")
async def init_webscraping(web_scraping_config: WebScrapingConfig):
    return {"message": "Método ainda não implementado"}
