from bs4 import BeautifulSoup
import requests

def get_soup(url):
    """Hace una solicitud GET a la URL y devuelve el objeto BeautifulSoup."""
    response = requests.get(url)

    return BeautifulSoup(response.content, 'html.parser')