import asyncio

from utils.gpt_assistant import send_message_to_assistant
from utils.send_to_admins import send_to_admins
from load_services import logger


class RequestManager:
    def __init__(self, concurrency_limit: int = 1):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.tasks_queue = asyncio.Queue()
        self.MAX_ATTEMPTS = 5

    async def worker(self):
        while True:
            video_title, challenge_text, comment_text, group_id, challenge_id, comment_id = await self.tasks_queue.get()

            try:
                async with self.semaphore:
                    extracted_data = None
                    
                    for _ in range(self.MAX_ATTEMPTS):
                        try:
                            extracted_data = await send_message_to_assistant(video_title=video_title, 
                                                                        challenge_text=challenge_text,
                                                                        comment_text=comment_text)
                            if extracted_data and extracted_data.get("data"):
                                    break
                        except Exception as exc:
                            logger.warning(f"Task failed {exc}")
                            await asyncio.sleep(5)

                    else:
                        extracted_data = None

                    if extracted_data:
                        logger.debug(f"Extracted data from assistant {extracted_data}")
                        
                        await send_to_admins(message=extracted_data, 
                                            group_id=group_id, 
                                            challenge_id=challenge_id,
                                            comment_id=comment_id,
                                            comment_text=comment_text)
            except Exception as exc:
                logger.warning(exc)
            finally:
                await asyncio.sleep(3)
                self.tasks_queue.task_done()
