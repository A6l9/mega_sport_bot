import re
import json
import asyncio

from aiogram.exceptions import TelegramBadRequest
from openai import RateLimitError, APIConnectionError, OpenAIError

from loader import bot
from load_services import logger
from utils.get_async_client import client
from config import proj_settings
from misc.prompts_instructions import ASSISTANT_PROMPT
from utils.get_assistant_storage import assistant_id_storage


async def send_message_to_assistant(video_title: str, challenge_text: str, comment_text: str):
    try:
        prompt = ASSISTANT_PROMPT.format(comment=comment_text,
                                         challenge_text=challenge_text,
                                         video_title=video_title)

        thread = await client.beta.threads.create()
        thread_message = await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )    

        run_assistant = await client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id_storage.assistant_id
            )
        
        while run_assistant.status in ["queued", "in_progress"]:

            keep_retrieving_run = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_assistant.id
            )

            logger.debug(f"Run status: {keep_retrieving_run.status}")

            if keep_retrieving_run.status == "completed":
                
                messages = await client.beta.threads.messages.list(thread_id=thread.id)
                answer = messages.data[0].content[0].text.value
                answer = re.sub(r"```json\n(.*?)\n```", r"\1", answer, flags=re.DOTALL)
                response_data = json.loads(answer)
                await asyncio.sleep(2)
                return response_data
            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                logger.debug(f"Run status: {keep_retrieving_run.status}")
                return None
            await asyncio.sleep(4)
                
    except RateLimitError:
        try:
            await bot.send_message(chat_id=proj_settings.admins_group_id, 
                                   text="Ошибка, средства на балансе OpenAI закончились.\nПожалуйста, пополните баланс.")
        except TelegramBadRequest:
            logger.debug(f"Не удалось найти пользователя с таким ID {proj_settings.admins_group_id}")
        return None
    except APIConnectionError as exc:
        logger.debug(f"Failed to connect to OpenAI API: {exc}")
        return None
    except OpenAIError as exc:
        logger.debug(f"OpenAI API error: {exc}")
        return None
    except Exception as exc:
        logger.debug(exc)