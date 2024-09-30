import requests
from bs4 import BeautifulSoup

class ReviewParser:
    def __init__(self, url):
        self.url = url

    def parse(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.text.replace(' - IMDb', '').strip()
            else:
                return "Título no encontrado"
        except requests.exceptions.RequestException as e:
            return f"Error al obtener reseña: {e}"

