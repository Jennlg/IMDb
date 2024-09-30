import os
import pandas as pd
from collections import defaultdict
from pathlib import Path
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup

class IMDBAnalysis:
    def __init__(self, url, directorio, directorio_pos, directorio_neg, urls_pos, urls_neg):
        self.url = url
        self.directorio = directorio
        self.directorio_pos = directorio_pos
        self.directorio_neg = directorio_neg
        self.urls_pos = urls_pos
        self.urls_neg = urls_neg

    def leer_puntuaciones(self, directorio):
        puntuaciones = defaultdict(list)
        for subdir, _, files in os.walk(directorio):
            for file_name in files:
                try:
                    identificador, puntuacion_str = file_name.split('_')
                    puntuacion = int(puntuacion_str.split('.')[0])
                    puntuaciones[identificador].append(puntuacion)
                except (ValueError, IndexError):
                    continue
        return puntuaciones

    def calcular_promedios(self, puntuaciones):
        promedios_conjunto = set()
        for identificador, scores in puntuaciones.items():
            promedio = sum(scores) / len(scores)
            promedios_conjunto.add((identificador, promedio))  # Guardamos (película, promedio) en un conjunto
        return promedios_conjunto

    def obtener_top_n(self, promedios, n=10, mejor=True):
        sorted_movies = sorted(promedios, key=lambda x: x[1], reverse=mejor)

        peliculas_unicas = []
        vistos = set()

        for pelicula, promedio in sorted_movies:
            if pelicula not in vistos:
                peliculas_unicas.append((pelicula, promedio))
                vistos.add(pelicula)
            if len(peliculas_unicas) == n:
                break

        return peliculas_unicas

    def procesar_url(self, url):
        return url.split('/usercomments')[0]

    def obtener_nombre_pelicula(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            return "Acceso denegado (403 Forbidden)"

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.replace(' - IMDb', '').strip()
        else:
            return "Título no encontrado"

    def crear_dataframe(self, peliculas, urls_path):
        urls = Path(urls_path).read_text().splitlines()
        data = []
        nombres_vistos = set()

        for identificador, promedio in peliculas:
            url = self.procesar_url(urls[int(identificador) - 1])
            nombre_pelicula = self.obtener_nombre_pelicula(url)

            if nombre_pelicula not in nombres_vistos:
                nombres_vistos.add(nombre_pelicula)
                data.append({'url': url, 'Película': nombre_pelicula, 'Promedio': promedio})

        return pd.DataFrame(data)

    def imprimir_peliculas(self, titulo, peliculas):
        '''Imprime en consola el título y la lista de películas con su promedio y URL en formato de tabla.'''
        table = PrettyTable()
        table.field_names = ["Película", "Promedio", "URL"]
        for pelicula in peliculas:
            table.add_row([pelicula['Película'], f"{pelicula['Promedio']:.2f}", pelicula['url']])
        print(titulo)
        print(table)

    def ejecutar_analisis(self):
        # Leer puntuaciones
        puntuaciones_pos = self.leer_puntuaciones(self.directorio_pos)
        puntuaciones_neg = self.leer_puntuaciones(self.directorio_neg)

        # Calcular promedios
        promedios_p = self.calcular_promedios(puntuaciones_pos)
        promedios_n = self.calcular_promedios(puntuaciones_neg)

        # Obtener las 10 mejores y peores películas
        mejores_peliculas = self.obtener_top_n(promedios_p, n=10)
        peores_peliculas = self.obtener_top_n(promedios_n, n=10, mejor=False)

        # Crear DataFrames
        df_mejores = self.crear_dataframe(mejores_peliculas, self.urls_pos)
        df_peores = self.crear_dataframe(peores_peliculas, self.urls_neg)

        while len(df_mejores) < 10:
            n_a_row = pd.DataFrame({'url': [''], 'Película': ['N/A'], 'Promedio': [0]})
            df_mejores = pd.concat([df_mejores, n_a_row], ignore_index=True)

        while len(df_peores) < 10:
            n_a_row = pd.DataFrame({'url': [''], 'Película': ['N/A'], 'Promedio': [0]})
            df_peores = pd.concat([df_peores, n_a_row], ignore_index=True)

        self.imprimir_peliculas("Las 10 películas mejor calificadas:\n", df_mejores.to_dict(orient='records'))
        self.imprimir_peliculas("Las 10 películas peor calificadas:\n", df_peores.to_dict(orient='records'))
