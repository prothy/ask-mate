from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, order_by, order_direction):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order_direction}
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_for_question(cursor: RealDictCursor, question_id):
    query = """
        SELECT a.*
        FROM question
        JOIN answer a on question.id = a.question_id
        WHERE question.id = (%s)
        """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE question.id = (%s)
        """
    cursor.execute(query, [question_id])
    return cursor.fetchall()


def update_question_votes(item_id, vote_action):
    """Updates vote questions: vote_action = True or False"""
    file = read_data(QUESTION_FILE_PATH)
    # Initiate vote_count variable to be returned
    vote_count = None
    for line in file:
        if line["id"] == item_id:
            # Upvote:
            if vote_action == "True":
                vote_count = int(line.get("vote_number", 0)) + 1
                line["vote_number"] = vote_count
            # Downvote:
            elif vote_action == "False":
                vote_count = int(line.get("vote_number", 0)) - 1
                line["vote_number"] = vote_count
    write_data(QUESTION_FILE_PATH, QUESTIONS_HEADER, file)
    return vote_count


def update_answer_votes(item_id, vote_action):
    """Updates vote answers: vote_action = True or False"""
    file = read_data(ANSWER_FILE_PATH)
    # Initiate vote_count variable to be returned
    vote_count = None
    for line in file:
        if line["id"] == item_id:
            # Upvote:
            if vote_action == "True":
                vote_count = int(line.get("vote_number", 0)) + 1
                line["vote_number"] = vote_count
            # Downvote:
            elif vote_action == "False":
                vote_count = int(line.get("vote_number", 0)) - 1
                line["vote_number"] = vote_count
    write_data(ANSWER_FILE_PATH, ANSWERS_HEADER, file)
    return vote_count


def update_view_count(item_id):
    """Updates vote answers: vote_action = True or False"""
    file = read_data(QUESTION_FILE_PATH)
    # Initiate vote_count variable to be returned
    view_count = None
    for line in file:
        if line["id"] == item_id:
            line["view_number"] = int(line.get("view_number", 0)) + 1
    write_data(QUESTION_FILE_PATH, QUESTIONS_HEADER, file)
    return view_count
