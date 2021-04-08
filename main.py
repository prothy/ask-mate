from flask import Flask, request, redirect, render_template, url_for, abort
from werkzeug.utils import secure_filename
import data_manager
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = "static/user-upload"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Evaluate UPLOAD_FOLDER relative to the current Flask App's execution directory
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT, UPLOAD_FOLDER)


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
    question = data_manager.get_table_data("question", question_id)[0]
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
        return redirect(url_for("display_question", question_id=question_id))


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('ask_question.html')
    else:
        title = request.form.get('input_title')
        message = request.form.get('input_message')

        images = request.files.getlist('input_image')
        for image in images:
            if image.filename != "":
                f = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))
                data_manager.add_question(
                    {
                        'title': title,
                        'message': message,
                        'image': f
                    }
                )
            else:
                data_manager.add_question(
                    {
                        'title': title,
                        'message': message
                    }
                )
        return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/delete', methods=['POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(request.referrer)


@app.route('/<edit_type>/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(edit_type, question_id):
    result = data_manager.get_table_data(edit_type, question_id)[0]

    if request.method == 'GET':
        return render_template('edit_question.html', result=result)
    else:
        title = request.form.get('input_title')
        message = request.form.get('input_message')

        data_manager.update_table(edit_type, question_id, {
            title: title,
            message: message
        })

        return redirect(request.referrer)


@app.route('/question/<question_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_question(question_id, action):
    if action == "vote_up" or action == "vote_down":
        data_manager.update_votes("question", question_id, action)
        return redirect(request.referrer)


@app.route('/answer/<answer_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_answer(answer_id, action):
    if action == "vote_up" or action == "vote_down":
        data_manager.update_votes("answer", answer_id, action)
        return redirect(request.referrer)


if __name__ == '__main__':
    app.run(
        debug=True
    )
