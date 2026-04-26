import sys
import requests
from groq import Groq
from openai import OpenAI
import anthropic
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from app.configs.timeouts import OPENAI_TIMEOUTS
from openai_cost_calculator import estimate_cost

class Load_Env(BaseSettings):
    client_id: str
    client_secret: str
    refresh_token: str
    customer_id: str
    developer_token: str

    groq_api_key: str
    openai_key: str
    perplexity_key: str

    claude_sonnet_api: str
    claude_model: str
    claude_model_temperature: float
    claude_max_tokens: int

    supabase_url: str
    supabase_key: str

    gemini_api_key: str

    sheet_id: str

    mongo_string: str

    pexel_token: str

    polotno: str

    google_service_private_key: str
    google_service_client_email: str
    google_service_client_id: str
    google_service_private_id_key: str
    google_service_project_id: str
    google_service_client_x509_cert_url: str

    encryption_key : str

    search_engine_id : str

    serper_api : str

    class Config:
        env_file = ".env"
        case_sensitive = False


try:
    env_var = Load_Env()
except Exception as e:
    print("Error loading environment variables:", e)
    sys.exit(1)  # Properly stop the server


groq_client = Groq(
    api_key=env_var.groq_api_key,
)
openai_client = OpenAI(api_key=env_var.openai_key)
anthropic_client = anthropic.Anthropic(api_key=env_var.claude_sonnet_api)


def openai_heartbeat():
    try:
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Greet the user"},
                {"role": "user", "content": "How are you?"},
            ],
            model="gpt-5-nano-2025-08-07",
            timeout=OPENAI_TIMEOUTS,
            max_completion_tokens=5,
            # max_tokens=1
        )

        print("OPENAI> ", chat_completion)
        estimate_cost(chat_completion)['total_cost']


    except Exception as e:
        print("❌ OpenAI not responding")


def claude_heartbeat():
    try:
        chat_completion = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            temperature=0,
            max_tokens=5,
            system="ping",
            messages=[
                {"role": "user", "content": "ping"},
            ],
        )
        print("Claude > ", chat_completion)
    except Exception as e:
        print("❌ Claude Not responding")


def groq_heartbeat():

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "ping",
                },
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )
        print(chat_completion.usage.completion_tokens)
    except Exception as e:
        print("❌ Claude Not responding")

from typing import Optional


class Usage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


class Cost(BaseModel):
    input_tokens_cost: float
    output_tokens_cost: float
    request_cost: float
    total_cost: float


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    search_context_size: str
    cost: Cost


class ChatCompletion(BaseModel):
    model: str
    usage: Usage


class ResearchedKeywordsGuardrail(BaseModel):
    focus_keywords: list[str]
    short_tail_keywords: list[str]
    long_tail_keywords: list[str]
    lsi_keywords: list[str]


def perplexity_heartbeat():

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "ping"},
                {"role": "user","content": "ping"},
            ],
            "max_tokens": 1,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "schema": ResearchedKeywordsGuardrail.model_json_schema()
                },
            },
        }
    
    headers = {
        "Authorization": f"Bearer {env_var.perplexity_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    # response.raise_for_status()

    print(ChatCompletion.model_validate(response.json()).usage.cost.total_cost)


# claude_heartbeat()
# openai_heartbeat()
# groq_heartbeat()
# perplexity_heartbeat()
