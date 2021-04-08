from psycopg2.extras import RealDictCursor

import database_common
import datetime


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
def get_table_data(cursor: RealDictCursor, table_name, table_element_id):
    """Lists all the questions by the ID"""
    query = f"""
        SELECT *
        FROM {table_name}
        WHERE id = {table_element_id}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_votes(cursor: RealDictCursor, vote_type: str, item_id, vote_action: str):
    """Updates vote count in database

    Parameters:
     vote_type - Table name to update ("question" or "answer")
     vote_action - "vote_up" or "vote_down"
    """
    calc_votes = "vote_number + 1" if vote_action == "vote_up" else "vote_number - 1"

    query = f"""
        UPDATE {vote_type}
        SET vote_number = {calc_votes} 
        WHERE id = {item_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def update_view_count(cursor: RealDictCursor, question_id):
    """Updates the corresponding view count"""
    query = f"""
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = {question_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, values):
    submission_time = datetime.datetime.now().isoformat(' ', 'seconds')
    query = f"""
        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
        VALUES ('{submission_time}', 0, {values['question_id']}, '{values['message']}', '{values['image']}')
    """
    cursor.execute(query)


@database_common.connection_handler
def add_question(cursor: RealDictCursor, values):
    submission_time = datetime.datetime.now().isoformat(' ', 'seconds')
    if "image" in values.keys():
        query = f"""
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
            VALUES ('{submission_time}', 0, 0, '{values['title']}', '{values['message']}', '{values["image"]}')
        """
    else:
        query = f"""
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
            VALUES ('{submission_time}', 0, 0, '{values['title']}', '{values['message']}', NULL)
        """
    cursor.execute(query)


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id):
    query = f"""
        DELETE FROM question
        WHERE id = {question_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    query = f"""
            DELETE FROM answer
            WHERE id = {answer_id}
        """
    cursor.execute(query)


@database_common.connection_handler
def update_table(cursor: RealDictCursor, table_name, table_element_id, values):
    if table_name == "question":
        query = f"""
                UPDATE {table_name}
                SET title = '{values["title"]}', message = '{values["message"]}'
                WHERE id = {table_element_id}            
            """
    else:
        query = f"""
                UPDATE {table_name}
                SET message = '{values["message"]}'
                WHERE id = {table_element_id}            
            """
    cursor.execute(query)


def search_table(search_query: str) -> tuple:
    """Searches questions and answers for string, returns a list of results in each"""
    question_results = search_questions(search_query)
    answer_results = search_answers(search_query)

    return question_results, answer_results


@database_common.connection_handler
def search_questions(cursor: RealDictCursor, search_query: str):
    query = f"""
        SELECT *
        FROM question
        WHERE (title LIKE '%{search_query}%')
        OR (message LIKE '%{search_query}%')
        """

    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answers(cursor: RealDictCursor, search_query: str):
    query = f"""
            SELECT *
            FROM answer
            WHERE message LIKE '%{search_query}%'
            """

    cursor.execute(query)
    return cursor.fetchall()
