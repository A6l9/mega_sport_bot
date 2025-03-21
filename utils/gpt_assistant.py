import asyncio
from typing import Optional

from aiogram.exceptions import ChatNotFound
from openai import RateLimitError, APIConnectionError, OpenAIError

from loader import logger, client, bot
from misc.prompts_instructions import ASSISTANT_INSTRUCTION, ASSISTANT_PROMPT


async def send_message_to_assistant(video_title: str, challenge_text: str, comment_text: str):
    try:
        prompt = ASSISTANT_PROMPT.format(comment=comment_text,
                                         challenge_text=challenge_text,
                                         video_title=video_title)
        

        my_assistant = await client.beta.assistants.create(model="gpt-4o",
                                                        instructions=ASSISTANT_INSTRUCTION,
                                                        name="Assistant")

        thread = await client.beta.threads.create()
        thread_message = await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )    

        run_assistant = await client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=my_assistant.id
            )
        
        while run_assistant.status in ["queued", "in_progress"]:

            keep_retrieving_run = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_assistant.id
            )

            logger.debug(f"Run status: {keep_retrieving_run.status}")

            if keep_retrieving_run.status == "completed":
                
                messages = await client.beta.threads.messages.list(thread_id=thread.id)
                return messages.data[0].content.text.value
            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                logger.debug(f"Run status: {keep_retrieving_run.status}")
                return None
            await asyncio.sleep(4)
                
    # except RateLimitError:
        # for i_id in USERS_IDS:
        #     try:
        #         await bot.send_message(chat_id=i_id, text="Ошибка, средства на балансе OpenAI закончились.\nПожалуйста, пополните баланс.")
        #     except ChatNotFound:
        #         logger.debug(f"Не удалось найти пользователя с таким ID {i_id}")
        # return None
    except APIConnectionError as exc:
        logger.debug(f"Failed to connect to OpenAI API: {exc}")
        return None
    except OpenAIError as exc:
        logger.debug(f"OpenAI API error: {exc}")
        return None