import re
import json
import asyncio
import time

from aiogram.exceptions import TelegramBadRequest
from openai import RateLimitError, APIConnectionError, OpenAIError

from loader import bot
from load_services import logger
from utils.get_async_client import client
from config import proj_settings
from misc import prompts_instructions


async def send_message_to_assistant(video_title: str, challenge_text: str, comment_text: str, assistant_id: str):
    try:
        prompt = prompts_instructions.ASSISTANT_PROMPT.format(comment=comment_text,
                                         challenge_text=challenge_text,
                                         video_title=video_title)

        thread = await client.beta.threads.create()
        logger.debug(f"Adding message to thread {thread.id}")
        thread_message = await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )    

        run_assistant = await client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id,
                temperature=0.1
            )
        
        start_time = time.time()
        timeout = 120
        
        while run_assistant.status in ["queued", "in_progress"]:
            if time.time() - start_time > timeout:
                logger.warning(f"Run time out for thread {thread.id}")
                
                return None

            keep_retrieving_run = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_assistant.id
            )

            logger.debug(f"Run status: {keep_retrieving_run.status}")

            run_assistant = keep_retrieving_run

            if keep_retrieving_run.status == "requires_action":
                message = run_assistant.required_action.submit_tool_outputs.tool_calls[0].function.arguments
                response_data = json.loads(message)
                return response_data
            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                logger.warning(f"Couldn't to get response, status: {keep_retrieving_run.status}")
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


async def create_assistants() -> None:
    list_of_assistants = prompts_instructions.ASSISTANTS

    for ast in list_of_assistants:
        assistant = await client.beta.assistants.create(model="gpt-4-turbo",
                                            **ast, temperature=0.1)
        logger.info(f"<< {assistant.name} - {assistant.id} >>")
