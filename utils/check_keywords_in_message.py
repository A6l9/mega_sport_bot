import re


async def check_message(message_text: str) -> bool:
    keywords = ["#челендж" "челенджа", "челендж", "челенджей", "челенджи"]
    pattern = "|".join(rf"\b{i}\b" for i in keywords).replace(" ", r"\s+")
    result = re.findall(pattern, message_text, re.IGNORECASE)
    if result:
        return True
    return False
