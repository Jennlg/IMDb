import urllib.request
import tarfile
from pathlib import Path

def download_database(url):
    """Descarga la base de datos desde la URL especificada."""
    directory = Path("data")  # Cambié a la carpeta 'data' en lugar de '/content'
    directory.mkdir(parents=True, exist_ok=True)
    tar_path = directory / "aclImdb_v1.tar.gz"

    if not tar_path.exists():  # Si el archivo no existe, descargarlo
        urllib.request.urlretrieve(url, tar_path)
        print("Descarga completada.")
    else:  # Si el archivo ya existe, imprimir un mensaje
        print("El archivo ya existe. Se omite la descarga.")
    return tar_path

def decompress_file(tar_path):
    """Descomprime el archivo .tar.gz especificado."""
    directory = tar_path.parent
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=directory)
    print(f"Archivo descomprimido en {directory}")
