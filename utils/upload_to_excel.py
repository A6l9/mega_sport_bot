import openpyxl

from database.models import Comments


async def upload_comments_to_excel(comments: list[Comments]):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    headers = ["challenge_name", "full_name", "club_name",
               "role", "result", "video_link", "comment_text",
               "is_answered", "comment_answer"]
    worksheet.append(headers)
    for i_comm in comments:
        worksheet.append((
                          i_comm.challenge_name,
                          i_comm.full_name,
                          i_comm.club_name,
                          i_comm.role,
                          i_comm.result,
                          i_comm.video_link,
                          i_comm.comment_text,
                          i_comm.is_answered,
                          i_comm.comment_answer
                          ))
    workbook.save('comments.xlsx')
