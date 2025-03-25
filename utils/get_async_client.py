from openai import AsyncOpenAI

from config import proj_settings


client = AsyncOpenAI(api_key=proj_settings.assistant_token, 
                     max_retries=2,
                     timeout=5)
