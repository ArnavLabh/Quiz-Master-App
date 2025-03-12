from .database import db
from datetime import datetime, timedelta

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)
    qualification = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    type = db.Column(db.String(), default='general', nullable=False)
    scores = db.relationship('Score', backref='user')

class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    chapters = db.relationship('Chapter', backref='subject')

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter')

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    questions = db.relationship('Question', backref='quiz')
    scores = db.relationship('Score', backref='quiz')

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_title = db.Column(db.String(), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(), nullable=False)
    option2 = db.Column(db.String(), nullable=False)
    option3 = db.Column(db.String(), nullable=False)
    option4 = db.Column(db.String(), nullable=False)
    correct_option = db.Column(db.String(), nullable=False)

class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date(), nullable=False)
    percentage = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    remarks = db.Column(db.String(), nullable=False)