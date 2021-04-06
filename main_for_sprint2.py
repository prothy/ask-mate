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
def edit_answer(answer_id):
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

@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_question(answer_id):
    file = connection.read_data("sample_data/comment.csv")
    for index in range(len(file)):
        if file[index]['id'] == comment_id:
            result = file[index]
    if request.method == 'GET':
        #template name: edit_comment.html
        return render_template('edit_comment.html', result=result)
    else:
        unix_time = int(time.time())
        message = request.form.get('input_message')
        image = request.form.get('input_image_url')
        result.update({'submission_time': unix_time, 'message': message, 'image': image}) #are the names of required variables correct?
        connection.write_data(connection.COMMENT_FILE_PATH, connection.COMMENTS_HEADER, file)
        return redirect(url_for('list_questions')) #not sure... maybe return somewhere else?

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

@app.route('/tag/<question_id>/add', methods=['GET', 'POST'])
def add_tag(question_id): #add tag to question
    file = connection.read_data("sample_data/question.csv") #add tag to question

    for index in range(len(file)):
        if file[index]['id'] == question_id:
            result = file[index]
    if request.method == 'GET':
        return render_template('add_tag.html', result=result)
    else:
        unix_time = int(time.time())
        title = request.form.get('input_title')
        message = request.form.get('input_message')
        image = request.form.get('input_image_url')
        tags = request.form.get('input_tag')
        #new_question and add_question should be modified (variable for tags)
        result.update({'submission_time': unix_time, 'title': title, 'message': message, 'image': image, 'tags': tags})
        connection.write_data(connection.QUESTION_FILE_PATH, connection.QUESTIONS_HEADER, file)
        return redirect(url_for('list_questions'))