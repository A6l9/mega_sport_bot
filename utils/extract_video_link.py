import re
from typing import Union


async def extract_video_link(message: str) -> Union[str, None]:
    if message:
        pattern = r"\bhttps:\/\/rutube\.ru\/video\/\S*"
        video_link = re.search(pattern=pattern, string=message)
        if video_link:
            return video_link.group()
        return None
