from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Testa se o endpoint de HealthCheck retorna 200 (Ok)"""
    # Act
    response = client.get("/HealthCheck")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "devops-webscraping no ar"}


def test_post_webscraping_sucesso(mocker):
    """
    Testa o endpoint /WebScraping em um cenário de sucesso.
    - Mocks: `app.api.scraping.buscar_vagas`
    """
    # Arrange
    payload = {"filtro": "python", "limite": 2}
    vagas_mock = [
        {"titulo": "Vaga Falsa 1", "empresa": "Empresa Mock", "local": "Nuvem", "link": "http://link.mock"}
    ]

    mocker.patch('app.api.scraping.buscar_vagas', return_value=vagas_mock)

    # Act
    response = client.post("/WebScraping", json=payload)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == "1 vaga(s) encontrada(s)"
    assert data["data"] == vagas_mock


def test_post_webscraping_sem_resultados(mocker):
    """
    Testa o endpoint /WebScraping quando o serviço não retorna nenhuma vaga.
    - Mocks: `app.api.scraping.buscar_vagas`
    """
    # Arrange
    payload = {"filtro": "vaga_inexistente", "limite": 5}
    mocker.patch('app.api.scraping.buscar_vagas', return_value=[])

    # Act
    response = client.post("/WebScraping", json=payload)
    data = response.json()

    # Arrange
    assert response.status_code == 200
    assert data["message"] == "Nenhuma vaga encontrada para o filtro fornecido"
    assert data["data"] == []
