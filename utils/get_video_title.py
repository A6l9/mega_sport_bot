import asyncio
from random import randrange

import aiohttp

from load_services import logger
from utils.extract_video_id import extract_video_id


async def get_video_title(video_link: str) -> str:
    video_link = await extract_video_id(video_link)

    if video_link:
        for _ in range(8):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(video_link) as response:
                        if response.status == 200:
                            data = await response.json()
                            await asyncio.sleep(randrange(3, 5))
                            logger.debug(f"Getting a title ended succesfully title: {data.get("title")}")
                            return data.get("title")
                        else:
                            seconds_sleep = randrange(5, 8)
                            logger.debug(f"The response has a status {response.status}. Next try after {seconds_sleep}s.")
                            await asyncio.sleep(seconds_sleep)
            except TimeoutError:
                logger.debug("The response from the server has been waiting too long, I'm trying again.")
                await asyncio.sleep(randrange(3, 5))
            except Exception as exc:
                logger.debug(exc)
                await asyncio.sleep(randrange(3, 5))
    return None
