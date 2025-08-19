from pydantic import BaseModel, Field


class WebScrapingConfig(BaseModel):
    filtro: str = Field(..., example="python", description="O termo a ser buscado para a vaga")
    limite: int = Field(default=10, gt=0, le=50, description="Número de resultados a serem retornados (mínimo 1 e "
                                                             "máximo 50)")
    ordenacao: str = Field(default="relevancia", description="Critério de ordenação (ainda não implementado)")
