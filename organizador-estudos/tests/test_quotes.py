"""Teste de integracao para o modulo de frases motivacionais."""

from unittest.mock import MagicMock, patch

from src.quotes import fetch_quote


class TestFetchQuote:
    """Testes de integracao com a API de frases."""

    def test_fetch_quote_success(self):
        """Deve retornar frase e autor quando a API responde corretamente."""
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = [
            {"q": "A persistencia e o caminho do exito.", "a": "Charles Chaplin"}
        ]
        fake_response.raise_for_status = MagicMock()

        with patch("src.quotes.requests.get", return_value=fake_response):
            result = fetch_quote()

        assert result is not None
        assert result["text"] == "A persistencia e o caminho do exito."
        assert result["author"] == "Charles Chaplin"

    def test_fetch_quote_api_offline(self):
        """Deve retornar None quando a API esta fora do ar."""
        import requests

        with patch(
            "src.quotes.requests.get",
            side_effect=requests.ConnectionError("sem conexao"),
        ):
            result = fetch_quote()

        assert result is None

    def test_fetch_quote_invalid_json(self):
        """Deve retornar None quando a API retorna dados inesperados."""
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = []
        fake_response.raise_for_status = MagicMock()

        with patch("src.quotes.requests.get", return_value=fake_response):
            result = fetch_quote()

        assert result is None

    def test_fetch_quote_timeout(self):
        """Deve retornar None quando a API demora demais."""
        import requests

        with patch(
            "src.quotes.requests.get",
            side_effect=requests.Timeout("timeout"),
        ):
            result = fetch_quote()

        assert result is None
