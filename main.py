import requests

from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional


app = FastAPI(
    title="DevOps WebScraping API",
    description="API simples desenvolvida para estudar e demonstrar conceitos de DevOps e web scraping",
    version="0.1.0"
)

class WebScrapingConfig(BaseModel):
    filtro: str
    limite: int
    ordenacao: str

@app.get("/HealthCheck", tags=["Status"])
async def health_check():
    """Endpoint para verificar se a API está no ar"""
    return {"message": "devops-webscraping no ar"}

@app.post("/WebScraping", tags=["Scraping"])
async def init_webscraping(web_scraping_config: WebScrapingConfig):
    """Faz o processo de web scraping utilizando os filtros fornecidos"""
    vagas = buscar_vagas(
        filtro=web_scraping_config.filtro,
        limite=web_scraping_config.limite
    )

    if not vagas:
        return {"message": "Nenhuma vaga encontrada no filtro fornecido", "data": []}

    return {
        "message": f"{len(vagas)} vaga(s) encontrada(s)",
        "data": vagas
    }

def buscar_vagas(filtro: str, limite: int) -> List[Dict[str, Optional[str]]]:
    """
    Busca vagas no site vagas.com.br de acordo com o filtro e o limite especificados
    Args:
        filtro(str): Termo chave para a busca
        limite(int): O número máximo de vagas para o retorno
    Returns:
        List[Dict[str, Optional[str]]]: Lista de dicionários, com cada dicionário sendo uma vaga
    """
    url = f"https://www.vagas.com.br/vagas-de-{filtro.replace(' ', '-')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        vagas_html = soup.findAll("li", class_="vaga")

        lista_de_vagas = []
        for vaga in vagas_html[:limite]:
            titulo_tag = vaga.find("h2", class_="cargo")
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

            senioridade_tag = vaga.find("span", class_="nivelVaga")
            senioridade = senioridade_tag.get_text(strip=True) if senioridade_tag else None

            empresa_tag = vaga.find("span", class_="emprVaga")
            empresa = empresa_tag.get_text(strip=True) if empresa_tag else None

            # Os dois seletores podem conter vaga, pensar numa maneira de conciliá-los no scraping
            # local_tag = vaga.find("div", class_="vaga-local")
            # local = local_tag.get_text(strip=True) if local_tag else None

            local_tag = vaga.find("span", class_="vaga-local")
            local = local_tag.get_text(strip=True) if local_tag else None

            link_tag = titulo_tag.find("a") if titulo_tag else None
            link = f"https://www.vagas.com.br{link_tag["href"]}" if link_tag else None

            lista_de_vagas.append({
                "titulo": titulo,
                "senioridade": senioridade,
                "empresa": empresa,
                "local": local,
                "link": link
            })

        return lista_de_vagas;
    except requests.exceptions.RequestException as ex:
        print(f"Erro ao fazer a requisição HTTP: {ex}")
        return []
    except Exception as ex:
        print(f"Erro inesperado durante o scraping: {ex}")
        return []
