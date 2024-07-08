import os

import urllib.request
import gzip
import shutil
from pathlib import Path
from sqlalchemy import create_engine

import geopandas

engine = create_engine(
    f"postgresql://aherman:kk0f6xbykj97qdrxa0sa@postgresql-161505.user-aherman:5432/db"
)

PCI_URL = "https://cadastre.data.gouv.fr/data"


def download_and_extract_gzip(url, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Télécharger le fichier gzip
    filename = output_dir / url.split("/")[-1]
    urllib.request.urlretrieve(url, filename)

    # Décompresser le fichier gzip
    with gzip.open(filename, "rb") as f_in:
        with open(filename.with_suffix(""), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Supprimer le fichier gzip téléchargé
    filename.unlink()
    return filename


def create_and_populate_pci_table(code_insee, output_dir):
    output_dir = Path(output_dir)
    geojson = output_dir / f"cadastre-{code_insee}-parcelles.json"
    gdf = geopandas.read_file(geojson)
    gdf.to_postgis(
        f"pci_{code_insee}", schema="public", if_exists="replace", con=engine
    )
    return len(gdf)


if __name__ == '__main__':
    codes_insee = ['59350','59646','59002']
    output_dir = "pci_output"
    
    for code_insee in codes_insee:
        url = f"{PCI_URL}/etalab-cadastre/latest/geojson/communes/59/{code_insee}/cadastre-{code_insee}-parcelles.json.gz"
        download_file = download_and_extract_gzip(url, output_dir)
        nb_line = create_and_populate_pci_table(code_insee, output_dir)
        print(f"Integration {code_insee} : {nb_line} parcelles")