from datetime import datetime

from pytz import timezone

from database.get_db_interface import db_interface


async def check_challenge_end_date(chall_list: list) -> None:
    date_now = datetime.now(tz=timezone("Europe/Moscow")).date()
    ended_challenges = []
    for i_chall in chall_list:
        if date_now > i_chall.date_of_end:
            ended_challenges.append(i_chall.challenge_id)
    if ended_challenges:
        await db_interface.change_challenges_status(challenge_ids=ended_challenges, status=True)
