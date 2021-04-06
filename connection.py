"""
 data_manager.py --> is responsible for formatting data.
"""
from connection import read_data, write_data, QUESTION_FILE_PATH, ANSWER_FILE_PATH, QUESTIONS_HEADER, ANSWERS_HEADER


def sorting_questions(questions_list, order_by, order_direction):
    if questions_list[0][order_by].isdigit():
        sorted_questions = sorted(questions_list, key=lambda k: int(k[order_by]))
    else:
        sorted_questions = sorted(questions_list, key=lambda k: k[order_by].lower())
    return sorted_questions if order_direction == "asc" else sorted_questions[::-1]


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