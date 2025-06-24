import asyncio

from utils.gpt_assistant import send_message_to_assistant
from utils.send_to_admins import send_to_admins
from load_services import logger
from loader import proj_settings


class RequestManager:
    def __init__(self, concurrency_limit: int = 5):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.tasks_queue = asyncio.Queue()
        self.MAX_ATTEMPTS = 5

    async def worker(self):
        logger.info("The worker has started")

        while True:
            (video_title, challenge_text,
            comment_text, group_id,
            challenge_id, comment_id, assistant_id, admin_group_id) = await self.tasks_queue.get()
            logger.info("Task was reсeived successfully")

            try:
                async with self.semaphore:
                    extracted_data = None
                    
                    for _ in range(self.MAX_ATTEMPTS):
                        try:
                            extracted_data = await send_message_to_assistant(video_title=video_title, 
                                                                        challenge_text=challenge_text,
                                                                        comment_text=comment_text,
                                                                        assistant_id=assistant_id)
                            if extracted_data:
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
                                            comment_text=comment_text,
                                            admin_group_id=admin_group_id)
            except Exception as exc:
                logger.warning(exc)
            finally:
                await asyncio.sleep(3)
                self.tasks_queue.task_done()
