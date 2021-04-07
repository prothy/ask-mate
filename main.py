from flask import Flask, request, redirect, render_template, url_for, abort
from werkzeug.utils import secure_filename
import data_manager
import time
import os

UPLOAD_FOLDER = "/static/user-upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/list')
def list_questions():
    """INITIAL: Lists the questions by order"""
    sort = request.args.get("sort") if request.args.get("sort") else "submission_time"
    order = request.args.get("order") if request.args.get("order") else "desc"
    questions_list = data_manager.sort_questions(sort, order)
    return render_template('list_questions.html', questions=questions_list)


@app.route('/question/<question_id>')
def display_question(question_id):
    """Routes to the specific ID of the selected question displaying corresponding answers"""
    question = data_manager.get_question(question_id)[0]
    answers_list = data_manager.get_answers_for_question(question_id)
    data_manager.update_view_count(question_id)
    return render_template('show_answers.html', question=question, answers=answers_list)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html')
    else:
        message = request.form.get('input_message')
        picture = request.form.get('input_image_url')
        data_manager.add_answer(
            {
                'question_id': question_id,
                'message': message,
                'image': picture
             }
        )
        return redirect(url_for('list_questions'))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    file = connection.read_data("sample_data/question.csv")
    if request.method == 'GET':
        return render_template('ask_question.html')
    else:
        id = util.create_id(file)
        unix_time = int(time.time())
        view_number = 0
        vote_number = 0
        title = request.form.get('input_title')
        message = request.form.get('input_message')

        images = request.files.getlist('input_image')
        image_list = []
        for image in images:
            f = image.filename
            image.save(os.path.join("static/user-upload", f))
            image_list.append(f)

        file.append(
            {'id': id,
             'submission_time': unix_time,
             'view_number': view_number,
             'vote_number': vote_number,
             'title': title,
             'message': message,
             'image': image_list
             }
        )
        connection.write_data(connection.QUESTION_FILE_PATH, connection.QUESTIONS_HEADER, file)
        return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/delete', methods=['POST'])
def delete_question(question_id):
    file = connection.read_data("sample_data/question.csv")
    for index in range(len(file)):
        if file[index]['id'] == question_id:
            file.pop(index)
            connection.write_data(connection.QUESTION_FILE_PATH, connection.QUESTIONS_HEADER, file)
            return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    file = connection.read_data("sample_data/question.csv")
    for index in range(len(file)):
        if file[index]['id'] == question_id:
            result = file[index]
    if request.method == 'GET':
        return render_template('edit_question.html', result=result)
    else:
        unix_time = int(time.time())
        title = request.form.get('input_title')
        message = request.form.get('input_message')
        image = request.form.get('input_image_url')
        result.update({'submission_time': unix_time, 'title': title, 'message': message, 'image': image})
        connection.write_data(connection.QUESTION_FILE_PATH, connection.QUESTIONS_HEADER, file)
        return redirect(url_for('list_questions'))


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    file = connection.read_data(connection.ANSWER_FILE_PATH)
    for index in range(len(file)):
        if file[index]['id'] == answer_id:
            file.pop(index)
            connection.write_data(connection.ANSWER_FILE_PATH, connection.ANSWERS_HEADER, file)
            return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_question(question_id, action):
    data_manager.update_votes("question", question_id, action)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_answer(answer_id, action):
    data_manager.update_votes("answer", answer_id, action)
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(
        debug=True
    )
