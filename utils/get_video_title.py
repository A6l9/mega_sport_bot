import asyncio
from random import randrange

import aiohttp

from load_services import logger
from utils.extract_video_id import extract_video_id


async def get_video_title(video_link: str) -> str:
    video_link = await extract_video_id(video_link)

    if video_link:
        for _ in range(5):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(video_link) as response:
                        if response.status == 200:
                            data = await response.json()
                            await asyncio.sleep(randrange(3, 5))
                            return data["title"]
            except TimeoutError:
                logger.debug("The response from the server has been waiting too long, I'm trying again.")
                await asyncio.sleep(randrange(3, 5))
