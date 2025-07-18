from database.db_initial import Base

async def prepare_comments(comments: list[Base]) -> dict[list]:

    prepared_comments = {}

    for i_comm in comments:
        if prepared_comments.get(i_comm.challenge_id):
            prepared_comments[i_comm.challenge_id].append(i_comm)
        else:
            prepared_comments[i_comm.challenge_id] = [i_comm]
    
    return prepared_comments
