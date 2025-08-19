import pytest
import requests
from fastapi import HTTPException
from app.services.scraper import buscar_vagas


def test_buscar_vagas_sucesso(mocker, mock_html_sucesso):
    """
    Testa o caso de sucesso onde vagas são encontradas e convertidas corretamente.
    - Mocks: `requests.get`
    """
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.content = mock_html_sucesso.encode('utf-8')
    mocker.patch('app.services.scraper.requests.get', return_value=mock_response)

    # Act
    vagas = buscar_vagas(filtro="devops", limite=5)

    # Assert
    assert len(vagas) == 2
    assert vagas[0]["titulo"] == "Engenheiro(a) DevOps"
    assert vagas[0]["senioridade"] == "Júnior"
    assert vagas[0]["empresa"] == "Empresa A"
    assert vagas[0]["local"] == "São Paulo"
    assert vagas[0]["link"] == "https://www.vagas.com.br/vaga/v123"

    assert vagas[1]["titulo"] == "Analista SRE"
    assert vagas[1]["senioridade"] == "Sênior"
    assert vagas[1]["empresa"] == "Empresa B"
    assert vagas[1]["local"] == "Remoto"
    assert vagas[1]["link"] == "https://www.vagas.com.br/vaga/v456"


def test_buscar_vagas_sem_resultados(mocker, mock_html_sem_vagas):
    """
    Testa o caso onde a página é carregada, mas nenhuma vaga é encontrada.
    - Mocks: `requests.get`
    """
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.content = mock_html_sem_vagas.encode('utf-8')
    mocker.patch('app.services.scraper.requests.get', return_value=mock_response)

    # Act
    vagas = buscar_vagas(filtro="teste-erro", limite=5)

    # Assert
    assert len(vagas) == 0


def test_buscar_vagas_erro_de_requisicao(mocker):
    """
    Testa o tratamento de erro quando 'requests.get' falha
    - Mocks: `requests.get` para lançar uma exceção.
    """
    # Arrange
    mocker.patch('app.services.scraper.requests.get', side_effect=requests.exceptions.RequestException("Erro de rede"))

    # Act & Assert
    with pytest.raises(HTTPException) as ex_info:
        buscar_vagas(filtro="devops", limite=5)

    assert ex_info.value.status_code == 503


def test_buscar_vagas_erro_inesperado(mocker):
    """
    Testa o tratamento de erro quando há uma exceção inesperada
    - Mocks: `requests.get` para lançar uma exceção
    """
    # Arrange
    mocker.patch('app.services.scraper.requests.get', side_effect=Exception("Erro inesperado"))

    # Act & Assert
    with pytest.raises(HTTPException) as ex_info:
        buscar_vagas(filtro="devops", limite=5)

    assert ex_info.value.status_code == 500
