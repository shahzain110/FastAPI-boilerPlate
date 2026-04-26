import os
import requests
from pathlib import Path

def download_supabase_file(url: str, output_dir: str) -> Path:
    """
    Download a file from a public Supabase (or any HTTP) URL
    and save it into the given folder.

    Returns the downloaded file path.
    """

    os.makedirs(output_dir, exist_ok=True)

    filename = url.split("/")[-1]
    file_path = output_dir / filename

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return file_path