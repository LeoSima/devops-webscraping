import pytest


@pytest.fixture
def mock_html_sucesso():
    """Fixture que retorna um conteúdo HTML simulando uma resposta de sucesso"""
    return """
    <html>
        <body>
            <li class="vaga">
                <h2 class="cargo">
                    <a href="/vaga/v123">Engenheiro(a) DevOps</a>
                </h2>
                <span class="nivelVaga">Júnior</span>
                <span class="emprVaga">Empresa A</span>
                <span class="vaga-local">São Paulo</span>
            </li>
            <li class="vaga">
                <h2 class="cargo">
                    <a href="/vaga/v456">Analista SRE</a>
                </h2>
                <span class="nivelVaga">Sênior</span>
                <span class="emprVaga">Empresa B</span>
                <span class="vaga-local">Remoto</span>
            </li>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_sem_vagas():
    """Fixture que retorna um conteúdo HTML simulando uma busca sem resultados."""
    return "<html><body>Nenhuma vaga encontrada.</body></html>"
