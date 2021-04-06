#TODO: Search result list page
@app.route('/search', methods=['GET'])
def list_matching():
    temp = connection.read_data("sample_data/question.csv")
    sort = request.args.get("sort") if request.args.get("sort") else "submission_time"
    order = request.args.get("order") if request.args.get("order") else "desc"
    #changed sorting_questions to sorting_searched_questions
    questions_list = data_manager.sorting_searched_questions(temp, sort, order)
    for item in questions_list:
        item["converted_time"] = util.transform_timestamp(item["submission_time"])
    #name of template file should be search_result.html
    return render_template('search_result.html', questions=questions_list)



#TODO: Edit answer page

@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_question(answer_id):
    file = connection.read_data("sample_data/answer.csv")
    for index in range(len(file)):
        if file[index]['id'] == answer_id:
            result = file[index]
    if request.method == 'GET':
        #template name: edit_answer.html
        return render_template('edit_answer.html', result=result)
    else:
        unix_time = int(time.time())
        message = request.form.get('input_message')
        image = request.form.get('input_image_url')
        result.update({'submission_time': unix_time, 'message': message, 'image': image}) #are the names of required variables correct?
        connection.write_data(connection.ANSWER_FILE_PATH, connection.ANSWERS_HEADER, file)
        return redirect(url_for('list_questions')) #not sure... maybe return somewhere else?

#TODO: Edit comment page
#TODO: Delete Comment page

@app.route('/comment/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id): #is called with comment_id
    file = connection.read_data("sample_data/comment.csv") #comment.csv
    for index in range(len(file)):
        if file[index]['id'] == comment_id:
            file.pop(index)
            connection.write_data(connection.COMMENT_FILE_PATH, file) #i'm not sure whether these are the necessary variables, please correct if wrong
            return redirect(url_for('list_questions'))

#TODO: 'add tag' page

'''
@app.route('/list', methods=['GET', 'POST'])
def list_questions():
    temp = connection.read_data("sample_data/question.csv")
    sort = request.args.get("sort") if request.args.get("sort") else "submission_time"
    order = request.args.get("order") if request.args.get("order") else "desc"
    questions_list = data_manager.sorting_questions(temp, sort, order)
    for item in questions_list:
        item["converted_time"] = util.transform_timestamp(item["submission_time"])
    return render_template('list_questions.html', questions=questions_list)
'''

'''
@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    """Routes to the specific ID of the selected question with answers"""
    questions_list = connection.read_data("sample_data/question.csv")
    answers_list = []
    for answer in connection.read_data("sample_data/answer.csv"):
        if answer['question_id'] == question_id:
            answers_list.append(answer)

    for row in questions_list:
        if row['id'] == question_id:
            data_manager.update_view_count(question_id)
            return render_template('show_answers.html', question=row, answers=answers_list)

    abort(404)
'''


'''
@app.route('/answer/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    file = connection.read_data("sample_data/answer.csv")

    id = util.create_id(file)
    vote_number = 0
    unix_time = time.time()

    if request.method == 'GET':
        return render_template('add_answer.html')
    else:
        message = request.form.get('input_message')
        picture = request.form.get('input_image_url')
        file.append(
            {'id': id,
             'submission_time': int(unix_time),
             'vote_number': vote_number,
             'question_id': question_id,
             'message': message,
             'image': picture}
        )
        connection.write_data(connection.ANSWER_FILE_PATH, connection.ANSWERS_HEADER, file)
        return redirect(url_for('list_questions'))
'''



'''
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

'''


'''
@app.route('/question/<question_id>/delete', methods=['POST'])
def delete_question(question_id):
    file = connection.read_data("sample_data/question.csv")
    for index in range(len(file)):
        if file[index]['id'] == question_id:
            file.pop(index)
            connection.write_data(connection.QUESTION_FILE_PATH, connection.QUESTIONS_HEADER, file)
            return redirect(url_for('list_questions'))

'''


'''
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

'''


'''
@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    file = connection.read_data(connection.ANSWER_FILE_PATH)
    for index in range(len(file)):
        if file[index]['id'] == answer_id:
            file.pop(index)
            connection.write_data(connection.ANSWER_FILE_PATH, connection.ANSWERS_HEADER, file)
            return redirect(url_for('list_questions'))

'''

'''
@app.route('/question/<question_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_question(question_id, action):
    data_manager.update_question_votes(question_id, action)
    return redirect(request.referrer)

'''

'''
@app.route('/answer/<answer_id>/<action>')
# <action>: 'vote_up' or 'vote_down'
def vote_answer(answer_id, action):
    data_manager.update_answer_votes(answer_id, action)
    return redirect(request.referrer)

'''
