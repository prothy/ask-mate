from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, order_by, order_direction):
    """Sorts questions by the given criteria, defaults to submission time"""
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order_direction}
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_for_question(cursor: RealDictCursor, question_id):
    """Get all the answers for the selected question"""
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {question_id}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor: RealDictCursor, question_id):
    """Lists all the questions """
    query = f"""
        SELECT *
        FROM question
        WHERE id = {question_id}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_votes(cursor: RealDictCursor, vote_type, item_id, vote_action):
    calc_votes = "vote_number + 1" if vote_action == "vote_up" else "vote_number - 1"

    query = f"""
        UPDATE {vote_type}
        SET vote_number = {calc_votes} 
        WHERE id = {item_id}
    """

    cursor.execute(query)


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
