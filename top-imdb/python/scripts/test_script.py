from imdb.imdb_analysis import IMDBAnalysis
import sys
import os
from imdb.downloader import download_database, decompress_file
from pathlib import Path

def main():
    url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    tar_file = download_database(url)
    decompress_file(tar_file)
    # Agrega el directorio 'imdb' al sys.path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'imdb'))
    # Define directorios y archivos de URLs usando Path
    base_dir = Path(__file__).resolve().parent.parent / 'data' / 'aclImdb' / 'train'
    directorio_pos = base_dir / 'pos'
    directorio_neg = base_dir / 'neg'
    urls_pos = base_dir / 'urls_pos.txt'  # Ruta relativa
    urls_neg = base_dir / 'urls_neg.txt'  # Ruta relativa
    # Ejecutar el análisis
    analysis = IMDBAnalysis(url, base_dir, directorio_pos, directorio_neg, urls_pos, urls_neg)
    analysis.ejecutar_analisis()

if __name__ == "__main__":
    main()
