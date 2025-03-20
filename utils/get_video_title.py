import re
import asyncio

import aiohttp

from constants import RUTUBE_URL
from loader import logger


async def get_video_title(video_link: str) -> str:
    pattern = r"https:\/\/rutube\.ru\/video(?:\/private)?\/([a-f0-9]{32})\/"
    video_id = re.search(pattern=pattern, string=video_link)
    if video_id:
        for _ in range(5):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(RUTUBE_URL.format(video_id=video_id.group(1))) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data["title"]
                        await asyncio.sleep(2)
            except TimeoutError:
                logger.debug("The response from the server has been waiting too long, I'm trying again.")
                await asyncio.sleep(2)
