import openpyxl

from database.models import Comments


async def upload_comments_to_excel(comments: dict[list]):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    headers = ["challenge_id", "challenge_name", "full_name", "club_name",
               "role", "result", "video_link", "comment_text",
               "is_answered", "comment_answer", "execution_time"]
    worksheet.append(headers)
    for i_index, i_chall_id in enumerate(comments.keys()):
        if i_index != 0:
            worksheet = workbook.create_sheet(title=str(i_chall_id))
            worksheet.append(headers)
        worksheet.title = str(i_chall_id)
        for i_comm in comments.get(i_chall_id):
            worksheet.append((
                            i_comm.challenge_id,
                            i_comm.challenge_name,
                            i_comm.full_name,
                            i_comm.club_name,
                            i_comm.role,
                            i_comm.result,
                            i_comm.video_link,
                            i_comm.comment_text,
                            i_comm.is_answered,
                            i_comm.comment_answer,
                            i_comm.time_of_execution
                            ))
    workbook.save('comments.xlsx')
