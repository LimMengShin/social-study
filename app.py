from flask import Flask, render_template, g, request, jsonify, redirect
import sqlite3
from random import randint
import datetime

app = Flask(__name__)

database = "database.db"
page_num = 0

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

@app.route("/add_questions")
def add_questions():
    pass

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
