import re


async def characters_escaping(text: str) -> str:
    pattern = r"([_*\[\]()~`>#+\-=|{}.!])"
    return re.sub(pattern=pattern, repl=r"\\\1", string=text)
