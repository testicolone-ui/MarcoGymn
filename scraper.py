import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gymresult.it/"

def get_gare_femminili():
    url = BASE_URL + "gare.php"  # pagina principale con tutte le gare
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    gare = []

    for link in soup.select("a[href*='gara_']"):
        nome_gara = link.text.strip()
        href = link["href"]
        if "Femminile" in nome_gara or "GAF" in nome_gara:
            gare.append({
                "nome": nome_gara,
                "link": BASE_URL + href
            })

    return gare

def cerca_gara(keyword):
    """Restituisce le gare che contengono una parola chiave (es. 'Campionato', 'Regionale')"""
    tutte = get_gare_femminili()
    return [g for g in tutte if keyword.lower() in g["nome"].lower()]
