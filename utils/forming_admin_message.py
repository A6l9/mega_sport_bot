from loader import proj_settings
from data_models import AdminMessage


async def forming_message(message: dict, group_id: int, challenge_id: int) -> tuple[str, AdminMessage]:
    challenge_link = f"https://t.me/c/{group_id}/{challenge_id}"

    admin_message = AdminMessage(challenge_name = message.get("challenge_name") or "Не указано",
                                full_name = message.get("full_name") or "Не указано",
                                role = message.get("role") or "Не указано",
                                club_name = message.get("club") or "Не указано",
                                result = message.get("result") or "Не указано",
                                phone_number = message.get("phone_number") or "Не указано",
                                video_link = message.get("link"),
                                time_of_execution = message.get("time_of_execution") or "Не указано")

    if int(f"100{group_id}") == proj_settings.terfit_discussion_group_id:
        text = f"Новый комментарий к [челленджу]({challenge_link})\n\n" \
                f"**Название челенджа:** {admin_message['challenge_name']}\n" \
                f"**ФИО:** {admin_message['full_name']}\n" \
                f"**Член клуба\Тренер:** {admin_message['role']}\n" \
                f"**Название клуба:** {admin_message['club_name']}\n" \
                f"**Результат:** {admin_message['result']}\n" \
                f"**Время выполнения:** {admin_message['time_of_execution']}\n\n" \
                f"[Ссылка на видео]({admin_message['video_link']})"
    else:
        text = f"Новый комментарий к [челленджу]({challenge_link})\n\n" \
                f"**Название челенджа:** {admin_message['challenge_name']}\n" \
                f"**ФИО:** {admin_message['full_name']}\n" \
                f"**Результат:** {admin_message['result']}\n" \
                f"**Номер телефона:** {admin_message['phone_number']}\n" \
                f"[Ссылка на видео]({admin_message['video_link']})"

    return text, admin_message
