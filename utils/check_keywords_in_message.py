import re


async def check_message(message_text: str) -> str:
    if message_text:
        pattern = r"#\S+"
        result = re.findall(pattern, message_text, re.IGNORECASE)
        if result:
            if "#terfitchallenge" in result:
                return "#terfitchallenge"
            elif "#athletxchallenge" in result:
                return "#athletxchallenge"
        return ""
