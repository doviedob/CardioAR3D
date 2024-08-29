import yaml
import requests
import os
from tqdm import tqdm

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def main():
    with open('large_files.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    for file_info in config['large_files']:
        path = file_info['path']
        url = file_info['url']
        
        # Asegúrate de que el directorio existe
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        print(f"Descargando {path}...")
        download_file(url, path)
        print(f"{path} descargado exitosamente.")

if __name__ == "__main__":
    main()
