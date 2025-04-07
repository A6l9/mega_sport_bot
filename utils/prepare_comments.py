from database.models import Comments


async def prepare_comments(comments: list[Comments]) -> dict[list]:

    prepared_comments = {}

    for i_comm in comments:
        if prepared_comments.get(i_comm.challenge_id):
            prepared_comments[i_comm.challenge_id].append(i_comm)
        else:
            prepared_comments[i_comm.challenge_id] = [i_comm]
    
    return prepared_comments
