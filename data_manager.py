import datetime

import bcrypt
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, order_by: str, order_direction: str, tag_list: list):
    """Sorts questions by the given criteria, defaults to submission time
    Args:
        order_by: Any column in question and tag table
        order_direction: 'asc' or 'desc'
        tag_list: List of tags that will be filtered
    """
    query = f"""
        SELECT *
        FROM (
            SELECT q.id, submission_time, view_number, vote_number, title, message, image, array_agg(name) tags
            FROM question q
            INNER JOIN question_tag qt ON q.id = qt.question_id
            INNER JOIN tag t ON t.id = qt.tag_id
            GROUP BY q.id
            ORDER BY {order_by} {order_direction}
        ) tab
        WHERE NOT tags && %s
    """
    cursor.execute(query, (tag_list, ))
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor: RealDictCursor):
    query = """
        SELECT name
        FROM tag
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
def update_votes(cursor: RealDictCursor, vote_type: str, item_id: int, vote_action: str):
    """Updates vote count in database

    @param vote_type: Table name to update ("question" or "answer")
    @param vote_action: "vote_up" or "vote_down"
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
        VALUES ('{values['user_id']}', '{submission_time}', 0, {values['question_id']}, '{values['message']}', '{values['image']}')
    """
    cursor.execute(query)


@database_common.connection_handler
def add_question(cursor: RealDictCursor, values):
    submission_time = datetime.datetime.now().isoformat(' ', 'seconds')
    if "image" in values.keys():
        query = f"""
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
            VALUES ('{values['user_id']}', '{submission_time}', 0, 0, '{values['title']}', '{values['message']}', '{values["image"]}', NONE)
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
        DELETE FROM answer
        WHERE question_id = {question_id};
        
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
    """Searches questions and answers for string, returns a list of results in each
    @return: Tuple in format (question_results, answer_results)"""
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


@database_common.connection_handler
def register_user(cursor: RealDictCursor, values):
    hashed_password = bcrypt.hashpw(values['password'].encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')

    query = f"""
            INSERT INTO users(username, email, password, reputation)
            VALUES ('{values['username']}', '{values['email']}', '{hashed_password}', 0)
            """

    cursor.execute(query)


@database_common.connection_handler
def login(cursor: RealDictCursor, values):
    query = f"""
                SELECT password
                FROM users
                WHERE username LIKE '{values['username']}'
                """

    result = cursor.execute(query)
    return verify_password(values['password'], result.fetchall()[0])


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def update_reputation(cursor: RealDictCursor, vote_type, user_id, vote_action):
    if vote_action == "vote_up":
        points = 5 if vote_type == "question" else 10
    elif vote_action == "vote_down":
        points = -2
    else:
        points = 15

    query = f"""
        UPDATE users
        SET reputation = reputation + {points}
        WHERE id = {user_id}
    """
    cursor.execute(query)


@database_common.connection_handler
def list_users(cursor: RealDictCursor):
    query = f"""
    SELECT id, username, reputation
    FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def collect_qa(cursor: RealDictCursor, user_id, table):
    query = f"""
    SELECT id
    FROM {table}
    WHERE user_id = {user_id}
    GROUP BY user_id
    """
    cursor.execute(query)
    return cursor.fetchall()