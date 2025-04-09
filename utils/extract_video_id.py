import re

from constants import RUTUBE_PRIVATE_URL, RUTUBE_URL


async def extract_video_id(video_link: str) -> str | None:
    url = None

    pattern_video = r"https:\/\/rutube\.ru\/video\/([a-f0-9]{32})\/"
    pattern_private_video = r"https:\/\/rutube\.ru\/video\/private\/([a-f0-9]{32})\/"

    video_id = re.search(pattern=pattern_video, string=video_link)
    private_video_id = re.search(pattern=pattern_private_video, string=video_link)

    if video_id:
        url = RUTUBE_URL.format(video_id=video_id.group(1))
    elif private_video_id:
        sub_video_id_pattern = r"[?&]p=([\w-]+)"
        sub_video_id = re.search(sub_video_id_pattern, video_link)
        if sub_video_id:
            url = RUTUBE_PRIVATE_URL.format(video_id=private_video_id.group(1), sub_video_id=sub_video_id.group(1))
    return url
