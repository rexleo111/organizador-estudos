"""Modulo para buscar frases motivacionais de API publica."""

import requests

API_URL = "https://zenquotes.io/api/random"


def fetch_quote():
    """Busca uma frase motivacional aleatoria da API zenquotes.

    Returns:
        Dicionario com 'text' e 'author', ou None se falhar.
    """
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            return {
                "text": data[0].get("q", ""),
                "author": data[0].get("a", "Desconhecido"),
            }
    except (requests.RequestException, ValueError, KeyError):
        pass

    return None


def translate_quote(text, target_lang="pt"):
    
    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"en|{target_lang}",
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # A MyMemory coloca a tradução dentro de responseData -> translatedText
        if "responseData" in data and "translatedText" in data["responseData"]:
            return data["responseData"]["translatedText"]
            
    except (requests.RequestException, ValueError, KeyError):
        pass
        
    return None
