from fastapi import APIRouter

from app.services.scraper import buscar_vagas
from app.schemas.scraping import WebScrapingConfig

router = APIRouter()


@router.get("/HealthCheck", tags=["Status"])
async def health_check():
    """Endpoint para verificar se a API está no ar"""
    return {"message": "devops-webscraping no ar"}


@router.post("/WebScraping", tags=["Scraping"])
async def init_webscraping(web_scraping_config: WebScrapingConfig):
    """
    Inicia o processo de web scraping com base nos filtros fornecidos.
    """
    vagas = buscar_vagas(
        filtro=web_scraping_config.filtro,
        limite=web_scraping_config.limite
    )

    if not vagas:
        return {"message": "Nenhuma vaga encontrada para o filtro fornecido", "data": []}

    return {
        "message": f"{len(vagas)} vaga(s) encontrada(s)",
        "data": vagas
    }
