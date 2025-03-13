from flask import Flask, render_template, request, redirect
from flask import current_app as app
from .models import *
from datetime import datetime, date

# INDEX ROUTE

@app.route('/')
def home():
    return render_template('home.html')


# LOGIN, REGISTER AND DASHBOARD ROUTES

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pwd:
                if this_user.type == 'admin':
                    return redirect(f'/admin_dash')
                else:
                    return redirect(f'/user_dash/{this_user.user_id}?username={username}')
            else:
                return "Invalid password"
        else:
            return """User does not exist:
            <a href='/register'>Register</a>"""
    return render_template('login.html')

@app.route('/admin_dash')
def admin_dash():
    username = request.args.get('username')
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('admin_dash.html', username=username, subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions)

@app.route('/user_dash/<int:user_id>')
def user_dash(user_id):
    user= User.query.get(user_id)
    username = request.args.get('username')
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('user_dash.html',user=user, username=user.username, subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions, user_id=user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        fullname = request.form.get('fullname')
        qualification = request.form.get('qualification')
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            return """User already exists:
            <a href='/login'>Login</a>"""
        else:
            new_user = User(username=username, password=pwd, full_name=fullname, qualification=qualification, date_of_birth=dob)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/login')
    return render_template('register.html')


# ADMIN FUNCTIONS (New Subject, Chapter, Quiz, Question) ROUTES

@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    if request.method == 'POST':
        name = request.form.get('subj_name')
        description = request.form.get('subj_description')
        this_subject = Subject.query.filter_by(name=name).first()
        if this_subject:
            return "Subject already exists"
        else:
            new_subject = Subject(name=name, description=description)
            db.session.add(new_subject)
            db.session.commit()
        return redirect('/admin_dash')
    return render_template('admin_new_subject.html')

@app.route('/subject/<int:subject_id>/new_chapter', methods=['GET', 'POST'])
def new_chapter(subject_id):
    if request.method == 'POST':
        name = request.form.get('chapter')
        description = request.form.get('chap_desc')
        this_chapter = Chapter.query.filter_by(name=name).first()
        if this_chapter:
            return "Chapter already exists"
        else:
            new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
        return redirect('/admin_dash')
    return render_template('admin_new_chapter.html')

@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    if request.method == 'POST':
        chapter_name = request.form.get('chapter_name')
        title = request.form.get('quiz_title')
        chapter = Chapter.query.filter_by(name=chapter_name).first()
        if not chapter:
            return "Error: Chapter not found"
        chapter_id = chapter.chapter_id

        duration_str = request.form.get('quiz_duration')
        time_obj = datetime.strptime(duration_str, '%H:%M')
        duration_seconds = time_obj.hour * 3600 + time_obj.minute * 60

        date_str = request.form.get('quiz_date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        this_quiz = Quiz.query.filter_by(title=title).first()
        if this_quiz:
            return "Quiz already exists"
        else:
            new_quiz = Quiz(title=title, duration=duration_seconds, chapter_id=chapter_id, date=date)
            db.session.add(new_quiz)
            db.session.commit()
        return redirect('/quizzes')
    chapters = Chapter.query.all()
    return render_template('admin_new_quiz.html', chapters=chapters)

@app.route('/quiz/<int:quiz_id>/new_question', methods=['GET', 'POST'])
def new_question(quiz_id):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Save and Next':
            question_title = request.form.get('ques_title')
            question_statement = request.form.get('ques_stmt')
            option1 = request.form.get('ques_opt1')
            option2 = request.form.get('ques_opt2')
            option3 = request.form.get('ques_opt3')
            option4 = request.form.get('ques_opt4')
            correct_option = request.form.get('ques_optCorrect')
            this_question = Question.query.filter_by(question_title=question_title).first()
            if this_question:
                return "Question already exists"
            else:
                new_question = Question(question_title=question_title, question_statement=question_statement, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, quiz_id=quiz_id)
                db.session.add(new_question)
                db.session.commit()
            return redirect(f'/quiz/{quiz_id}/new_question')
        elif action == 'Close':
            return redirect('/quizzes')
    return render_template('admin_new_question.html', quiz_id=quiz_id)

@app.route('/quizzes')
def quizzes():
    username = request.args.get('username')
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('admin_quiz_management.html', username=username, subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions)




# DELETE ROUTES

@app.route('/subject/<int:subject_id>/delete', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if subject:
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        for chapter in chapters:
            db.session.delete(chapter)
        db.session.delete(subject)
        db.session.commit()
    return redirect('/admin_dash')

@app.route('/chapter/<int:chapter_id>/delete', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if chapter:
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        for quiz in quizzes:
            questions = Question.query.filter_by(quiz_id=quiz.quiz_id).all()
            for question in questions:
                db.session.delete(question)
            db.session.delete(quiz)
        db.session.delete(chapter)
        db.session.commit()
    return redirect('/admin_dash')

@app.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        if questions:
            for question in questions:
                db.session.delete(question)
        db.session.delete(quiz)
        db.session.commit()
    return redirect('/quizzes')

@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
    return redirect('/quizzes')


# EDIT ROUTES

@app.route('/subject/<int:subject_id>/edit', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        subject.name = request.form.get('subj_name')
        subject.description = request.form.get('subj_description')
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('admin_edit_subject.html', subject=subject)

@app.route('/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if request.method == 'POST':
        chapter.name = request.form.get('chapter')
        chapter.description = request.form.get('chap_desc')
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('admin_edit_chapter.html', chapter=chapter)

@app.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return redirect('/quizzes')
    if request.method == 'POST':
        chapter_name = request.form.get('chapter_name')
        chapter = Chapter.query.filter_by(name=chapter_name).first()
        if not chapter:
            return redirect('/quizzes')
        quiz.chapter_id = chapter.chapter_id
        quiz.title = request.form.get('quiz_title')

        duration_str = request.form.get('quiz_duration')
        time_obj = datetime.strptime(duration_str, '%H:%M')
        quiz.duration = time_obj.hour * 3600 + time_obj.minute * 60

        date_str = request.form.get('quiz_date')
        quiz.date = datetime.strptime(date_str, '%Y-%m-%d').date()

        db.session.commit()
        return redirect('/quizzes')
    chapters = Chapter.query.all()
    return render_template('admin_edit_quiz.html', quiz=quiz, chapters=chapters)



@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return redirect('/quizzes')
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Save':
            question.question_title = request.form.get('ques_title')
            question.question_statement = request.form.get('ques_stmt')
            question.option1 = request.form.get('ques_opt1')
            question.option2 = request.form.get('ques_opt2')
            question.option3 = request.form.get('ques_opt3')
            question.option4 = request.form.get('ques_opt4')
            question.correct_option = request.form.get('ques_optCorrect')
            db.session.commit()
            return redirect('/quizzes')
    quiz_id = question.quiz_id
    return render_template('admin_edit_question.html', question=question, quiz_id=quiz_id)


# SUMMARY ROUTE

@app.route('/admin/summary')
def summary():
    username = request.args.get('username')
    users= len(User.query.all())-1
    subjects = len(Subject.query.all())
    chapters = len(Chapter.query.all())
    quizzes = len(Quiz.query.all())
    questions = len(Question.query.all())
    return render_template('admin_summary.html', username=username, subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions, users=users)


# SEARCH ROUTE

@app.route("/results")
def search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    results = []
    if key == "user":
        results = User.query.filter_by(username=search_word).all()
    elif key == "subject":
        results = Subject.query.filter(Subject.name.ilike(search_word)).all()
    elif key == "chapter":
        results = Chapter.query.filter(Chapter.name.ilike(search_word)).all()
    elif key == "quiz":
        results = Quiz.query.filter(Quiz.title.ilike(search_word)).all()
    
    return render_template("results.html", results=results, key=key)


# USER QUIZ ROUTES

@app.route('/quiz/<int:quiz_id>/view/<int:user_id>')
def view_quiz(quiz_id, user_id):
    quiz = Quiz.query.get(quiz_id)
    user = User.query.get(user_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    chapter = Chapter.query.get(quiz.chapter_id)
    subject = Subject.query.get(quiz.chapter.subject_id)

    hours, remainder = divmod(quiz.duration, 3600)
    minutes, _ = divmod(remainder, 60)
    formatted_duration = f"{int(hours):02d}:{int(minutes):02d}"
    
    return render_template('user_view_quiz.html', quiz=quiz, questions=questions, chapter=chapter, subject=subject, formatted_duration=formatted_duration, user=user)


@app.route('/quiz/<int:quiz_id>/question/<int:question_id>/<int:user_id>', methods=['GET', 'POST'])
def answer_question(quiz_id, question_id, user_id):
    action = None

    user = User.query.get(user_id)
    quiz = Quiz.query.get(quiz_id)
    question = Question.query.get(question_id)

    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_id).all()
    total_questions = len(questions)

    current_index = next((i for i, q in enumerate(questions) if q.question_id == question_id), 0)

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        action = request.form.get('action')

        score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        if not score:
            score = Score(
                user_id=user_id, quiz_id=quiz_id, score=0, date=date.today(), percentage=0.0)
            db.session.add(score)

        if selected_answer == question.correct_option:
            score.score += 1
            score.percentage = (score.score / total_questions) * 100
    
        db.session.commit()

    if action == 'save_next':
        next_index = current_index + 1
        if next_index < total_questions:
            next_question = questions[next_index]
            return redirect(f'/quiz/{quiz_id}/question/{next_question.question_id}/{user_id}')
        else:
            return redirect(f'/quiz/{quiz_id}/result/{user_id}')
        
    elif action == 'submit_quiz':
        return redirect(f'/quiz/{quiz_id}/result/{user_id}')
    return render_template('user_answer_quiz.html', question=question, user=user, quiz=quiz, questions=questions, quiz_id=quiz_id, user_id=user_id, current_number=current_index+1, total_questions=total_questions)

@app.route('/quiz/<int:quiz_id>/start/<int:user_id>')
def start_quiz(quiz_id, user_id):
    old_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    if old_score:
        old_score.score = 0
        db.session.commit()
    
    first_question = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_id).first()
    if first_question:
        return redirect(f'/quiz/{quiz_id}/question/{first_question.question_id}/{user_id}')
    else:
        return "This quiz has no questions yet."
    
@app.route('/quiz/<int:quiz_id>/result/<int:user_id>')
def quiz_results(quiz_id, user_id):
    user = User.query.get(user_id)
    quiz = Quiz.query.get(quiz_id)
    score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    
    percentage = 0
    if total_questions > 0 and score:
        percentage = (score.score / total_questions) * 100
    
    return render_template('quiz_results.html', user=user, quiz=quiz, score=score.score if score else 0, total_questions=total_questions, percentage=percentage)


# USER SCORES AND SUMMARY ROUTES

@app.route('/user/<int:user_id>/scores')
def user_scores(user_id):
    user = User.query.get(user_id)
    scores = Score.query.filter_by(user_id=user_id).all()
    question_counts = {}
    for score in scores:
        if score.quiz_id not in question_counts:
            question_counts[score.quiz_id] = Question.query.filter_by(quiz_id=score.quiz_id).count()
    return render_template('user_scores.html', user=user, scores=scores, username=user.username, question_counts=question_counts)

@app.route('/user/<int:user_id>/summary')
def user_summary(user_id):
    import matplotlib.pyplot as plt
    import os
    if not os.path.exists('static'):
        os.mkdir('static')

    user = User.query.get(user_id)
    scores = Score.query.filter_by(user_id=user_id).all()
    
    total_scores = len(scores)
    total_score = 0
    for score in scores:
        total_score += score.score

    subjects = Subject.query.all()
    subject_names = []
    subject_counts = []

    for subject in subjects:
        subject_names.append(subject.name)
        count = 0
        for score in scores:
            chapter = Chapter.query.get(score.quiz.chapter_id)
            if chapter.subject_id == subject.subject_id:
                count += 1
        subject_counts.append(count)

    plt.figure(figsize=(10, 5))
    plt.bar(subject_names, subject_counts, color='blue')
    plt.xlabel('Subjects')
    plt.ylabel('Number of Quizzes')
    plt.title('Subject-wise Quiz Count')
    plt.xticks(rotation=45)

    subject_file = f'static/subject_graph_{user_id}.png'
    plt.savefig(subject_file)
    plt.clf()

    monthly_counts = {}
    for score in scores:
        month_year = score.date.strftime('%B %Y')
        if month_year in monthly_counts:
            monthly_counts[month_year] += 1
        else:
            monthly_counts[month_year] = 1

    months = list(monthly_counts.keys())
    counts = list(monthly_counts.values())
    
    plt.figure(figsize=(10, 5))
    plt.bar(months, counts, color='green')
    plt.xlabel('Month')
    plt.ylabel('Quizzes Attempted')
    plt.title('Monthly Quiz Attempts')
    plt.xticks(rotation=45)
    
    monthly_file = f'static/monthly_graph_{user_id}.png'
    plt.savefig(monthly_file)
    plt.clf()

    return render_template('user_summary.html', user=user, username=user.username, total_scores=total_scores, total_score=total_score, subject_graph=f'subject_graph_{user_id}.png', monthly_graph=f'monthly_graph_{user_id}.png')