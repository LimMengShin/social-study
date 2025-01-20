from flask import Flask, render_template, g, request, jsonify, redirect, flash
import sqlite3
from random import randint
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

database = "database.db"
page_num = 0

class AddQuestionForm(FlaskForm):
    subject = SelectField("Subject", choices=["Computing", "Math", "Physics", "Chemistry", "Economics", "English"], validators=[DataRequired()])
    question = TextAreaField("Question", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])
    correct_option = RadioField("Correct option", choices=["Option 1", "Option 2", "Option 3", "Option 4"], validators=[DataRequired()])

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def split_list(lst, n):
    new_lst = []
    for i in range(0, len(lst)-1, n):
        new_lst.append(lst[i:i+n])
    return new_lst

@app.route("/", methods=["GET", "POST"])
def index():
    global page_num
    if request.method == "POST":
        page_num = request.json.get('pageNum', page_num)
        print(page_num)
        return redirect("/")
    posts = query_db("SELECT * FROM posts ORDER BY created_utc DESC;")
    posts = [
        {
            **dict(post),
            'created_utc': datetime.datetime.fromtimestamp(post["created_utc"])
        }
        for post in posts
    ]
    posts_list = split_list(posts, 5)
    posts = posts_list[page_num % len(posts_list)]
    return render_template("index.html", posts=posts)

@app.route("/questions")
def questions():
    questions = query_db("SELECT * FROM questions;")
    questions = [dict(question) for question in questions]
    questions_dict = {}
    for question in questions:
        subject = question["subject"]
        question_dict = {"subject": question["subject"], "question": question["question"], "options": [question["option1"], question["option2"], question["option3"], question["option4"]], "correct": question["correct_option"]}
        if subject not in questions_dict:
            questions_dict[subject] = []
        questions_dict[subject].append(question_dict)
    questions_list = list(questions_dict.items())
    print(questions_list)
    return render_template("questions.html", questions_list=questions_list)

@app.route("/add_questions", methods=["GET", "POST"])
def add_questions():
    form = AddQuestionForm()
    if form.validate_on_submit():
        subject = request.form.get("subject")
        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")
        try:
            correct_option = "1234".index(correct_option[-1])+1
            insert_db("INSERT INTO questions (subject, question, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?);", (subject, question, option1, option2, option3, option4, correct_option))
            flash("Question submitted!")
        except ValueError:
            pass
        return redirect("/add_questions")
    return render_template("add_questions.html", form=form)

@app.route("/get_question")
def get_question():
    questions = query_db("SELECT * FROM questions;")
    questions = [dict(question) for question in questions]
    idx = randint(0, len(questions)-1)
    question = questions[idx]
    question_dict = {"subject": question["subject"], "question": question["question"], "options": [question["option1"], question["option2"], question["option3"], question["option4"]], "correct": question["correct_option"]}
    return jsonify(question_dict)

if __name__ == "__main__":
    app.run(debug=True)
