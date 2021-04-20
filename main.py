import os

from flask import Flask, request, redirect, render_template, url_for, flash
from werkzeug.utils import secure_filename

import data_manager
from form import RegistrationForm, LoginForm

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = "static/user-upload/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['SECRET_KEY'] = '406d389c74e700a2a35307d872bb618e'

# Evaluate UPLOAD_FOLDER relative to the current Flask App's execution directory
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT, UPLOAD_FOLDER)
print(APP_ROOT)
print(app.config['UPLOAD_FOLDER'])


@app.route('/')
@app.route('/list')
def list_questions():
    """INITIAL: Lists the questions by order"""
    sort = request.args.get("sort") if request.args.get("sort") else "submission_time"
    order = request.args.get("order") if request.args.get("order") else "desc"

    questions_list = data_manager.sort_questions(sort, order)
    for question in questions_list:
        question["message"] = question["message"].replace('"', "'")

    tags = data_manager.get_tags()

    return render_template('list_questions.html', questions=questions_list, tags=tags)


@app.route('/question/<question_id>')
def display_question(question_id):
    """Routes to the specific ID of the selected question displaying corresponding answers"""
    question = data_manager.get_table_data("question", question_id)[0]
    question["message"] = question["message"].replace('"', "'")
    answers_list = data_manager.get_answers_for_question(question_id)
    for answer in answers_list:
        answer["message"] = answer["message"].replace('"', "'")
    data_manager.update_view_count(question_id)
    return render_template('show_answers.html', question=question, answers=answers_list)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html')
    else:
        message = request.form.get('input_message')
        picture = request.form.get('input_image_url')

        message = message.replace("'", '"')

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
        message = message.replace("'", '"')

        images = request.files.getlist('input_image')
        for image in images:
            if image.filename != "":
                filename = secure_filename(image.filename)
                file_path = app.config['UPLOAD_FOLDER'] + filename
                save_path = "user-upload/" + filename
                image.save(file_path)

                data_manager.add_question(
                    {
                        'title': title,
                        'message': message,
                        'image': save_path
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


@app.route('/question/<question_id>/delete', methods=['GET'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/delete', methods=['GET'])
def delete_answer(answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(request.referrer)


@app.route('/<edit_type>/<q_and_a_id>/edit', methods=['GET', 'POST'])
def edit_q_and_a(edit_type, q_and_a_id):
    result = data_manager.get_table_data(edit_type, q_and_a_id)[0]
    result["message"] = result['message'].replace('"', "'")

    if request.method == 'GET':
        return render_template('edit_q_and_a.html', edit_type=edit_type, result=result)
    else:
        if edit_type == "question":
            title = request.form.get('input_title')
            message = request.form.get('input_message')
            message = message.replace("'", '"')

            data_manager.update_table(edit_type, q_and_a_id, {
                "title": title,
                "message": message
            })

            return redirect("/")
        elif edit_type == "answer":
            message = request.form.get('input_message')
            message = message.replace("'", '"')

            data_manager.update_table(edit_type, q_and_a_id, {
                "message": message
            })

            question_id = data_manager.get_table_data("answer", q_and_a_id)[0]["question_id"]

            return redirect(url_for("display_question", question_id=question_id))


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


@app.route('/search')
def list_matching():
    # sort = request.args.get("sort") if request.args.get("sort") else "submission_time"
    # order = request.args.get("order") if request.args.get("order") else "desc"

    search_query = request.args.get("search")
    questions, answers = data_manager.search_table(search_query)
    for question in questions:
        question["message"] = question["message"].replace('"', "'")
        question["message"] = "<p>" + question["message"].replace(search_query,
                                                                  f"<span class='search-query'>{search_query}</span>") + "</p>"
    for answer in answers:
        answer["message"] = answer["message"].replace('"', "'")
        answer["message"] = "<p>" + answer["message"].replace(search_query,
                                                              f"<span class='search-query'>{search_query}</span>") + "</p>"

    return render_template('search_results.html', questions=questions, answers=answers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # data_manager.register_user()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('list_questions'))
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('list_questions'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template("login.html", title='Login', form=form)
    # if request.method == 'GET':
    #     return render_template('login.html', message='')
    # else:
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     if data_manager.login(username=username, password=password):
    #         return render_template('/')
    #     else:
    #         return render_template('login.html', message='Invalid password or username. Please try again!')


@app.route("/logout")
def logout():
    pass


if __name__ == '__main__':
    app.run(
        debug=True
    )
