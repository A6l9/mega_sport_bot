import asyncio

from utils.gpt_assistant import send_message_to_assistant
from utils.send_to_admins import send_to_admins
from load_services import logger


class RequestManager:
    def __init__(self, concurrency_limit: int = 5):
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.tasks_queue = asyncio.Queue()

    async def worker(self):
        while True:
            video_title, challenge_text, comment_text, group_id, challenge_id, comment_id = await self.tasks_queue.get()

            try:
                async with self.semaphore:
                    extracted_data = await send_message_to_assistant(video_title=video_title, 
                                                                        challenge_text=challenge_text,
                                                                        comment_text=comment_text)
                    if extracted_data:
                        if extracted_data.get("data"): 
                            await send_to_admins(message=extracted_data, 
                                                group_id=group_id, 
                                                challenge_id=challenge_id,
                                                comment_id=comment_id,
                                                comment_text=comment_text)
            except Exception as exc:
                logger.debug(exc)
            finally: 
                self.tasks_queue.task_done()
