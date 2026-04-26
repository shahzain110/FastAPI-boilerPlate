import requests
from app.database.supabase.init import supabase

def upload_html(local_file_pth: str, supabase_path : str) -> str:

    with open(local_file_pth, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Add BOM to force UTF-8 recognition
    file_bytes = '\ufeff'.encode('utf-8') + content.encode("utf-8")
    
    response = supabase.storage.from_("test").upload(
        path=supabase_path,
        file=file_bytes,
        file_options={
            "cache-control": "3600",
            "upsert": "true",
            "content-type": "text/html; charset=utf-8",
        },
    )
    
    public_url = supabase.storage.from_("test").get_public_url(path=supabase_path)
    return public_url


def upload_png_from_url(image_url: str, supabase_path: str) -> str:
    # Download image
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()  # fail fast if download breaks

    file_bytes = response.content  # raw PNG bytes

    supabase.storage.from_("test").upload(
        path=supabase_path,
        file=file_bytes,
        file_options={
            "cache-control": "3600",
            "upsert": "true",
            "content-type": "image/png",
        },
    )

    return supabase.storage.from_("test").get_public_url(supabase_path)