from supabase import create_client, Client
from app.configs.models import env_var

SUPABASE_URL = env_var.supabase_url
SUPABASE_KEY = env_var.supabase_key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)