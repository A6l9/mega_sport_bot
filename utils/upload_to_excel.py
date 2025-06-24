import openpyxl

from challenges_config import CHALLENGES_CONFIG


async def upload_comments_to_excel(comments: dict[list], challenge_type: str):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    headers = ["challenge_id", "challenge_name", "full_name",
               "result", "video_link", "comment_text",
               "is_answered", "comment_answer"]
    headers.extend(CHALLENGES_CONFIG[challenge_type]["headers_list"])
    worksheet.append(headers)

    for i_index, i_chall_id in enumerate(comments.keys()):
        if i_index != 0:
            worksheet = workbook.create_sheet(title=str(i_chall_id))
            worksheet.append(headers)
        worksheet.title = str(i_chall_id)
        for i_comm in comments.get(i_chall_id):
            comments_row = (i_comm.challenge_id,
                            i_comm.challenge_name,
                            i_comm.full_name,
                            i_comm.result,
                            i_comm.video_link,
                            i_comm.comment_text,
                            i_comm.is_answered,
                            i_comm.comment_answer,)
            additional_fields = (i_comm.club_name, i_comm.role, i_comm.time_of_execution,) \
                                if challenge_type == "terfit" else (i_comm.phone_number,)
            worksheet.append(comments_row + additional_fields)
    workbook.save(f'comments-{challenge_type}.xlsx')
