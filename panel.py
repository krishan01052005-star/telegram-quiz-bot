from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_admin_key"

ADMIN_USERNAME = "krishan3341"
ADMIN_PASSWORD = "krish3341"

QUESTIONS_FILE = "questions.json"
SCORES_FILE = "scores.json"


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_files():
    if not os.path.exists(QUESTIONS_FILE):
        save_json(QUESTIONS_FILE, [])
    if not os.path.exists(SCORES_FILE):
        save_json(SCORES_FILE, [])


ensure_files()


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["username"] = username
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


# ------------ QUESTIONS CRUD ------------

@app.route("/question-form", methods=["GET", "POST"])
def question_form():
    if "username" not in session:
        return redirect(url_for("login"))

    # for edit mode
    qid = request.args.get("id")
    questions = load_json(QUESTIONS_FILE, [])
    editing = None
    if qid:
        try:
            qid = int(qid)
            editing = next((q for q in questions if q["id"] == qid), None)
        except Exception:
            editing = None

    if request.method == "POST":
        # Gather form
        question_text = request.form.get("question").strip()
        opt1 = request.form.get("opt1").strip()
        opt2 = request.form.get("opt2").strip()
        opt3 = request.form.get("opt3").strip()
        opt4 = request.form.get("opt4").strip()
        answer = request.form.get("answer").strip()
        image = request.form.get("image").strip()  # optional url/path
        lang = request.form.get("lang") or "hi"

        # load existing
        questions = load_json(QUESTIONS_FILE, [])
        if request.form.get("id"):  # update existing
            try:
                uid = int(request.form.get("id"))
                for q in questions:
                    if q["id"] == uid:
                        q["question"] = question_text
                        q["options"] = [opt1, opt2, opt3, opt4]
                        q["answer"] = answer
                        q["image"] = image
                        q["lang"] = lang
                        break
                save_json(QUESTIONS_FILE, questions)
                flash("Question updated", "success")
            except Exception:
                flash("Update failed", "error")
        else:  # add new
            new_id = (max([q["id"] for q in questions]) + 1) if questions else 1
            new_q = {
                "id": new_id,
                "question": question_text,
                "options": [opt1, opt2, opt3, opt4],
                "answer": answer,
                "image": image,
                "lang": lang
            }
            questions.append(new_q)
            save_json(QUESTIONS_FILE, questions)
            flash("Question added", "success")

        return redirect(url_for("questions"))

    return render_template("question_form.html", editing=editing)


@app.route("/questions")
def questions():
    if "username" not in session:
        return redirect(url_for("login"))
    questions = load_json(QUESTIONS_FILE, [])
    return render_template("questions.html", questions=questions)


@app.route("/questions/delete/<int:qid>", methods=["POST"])
def question_delete(qid):
    if "username" not in session:
        return redirect(url_for("login"))
    questions = load_json(QUESTIONS_FILE, [])
    questions = [q for q in questions if q["id"] != qid]
    save_json(QUESTIONS_FILE, questions)
    flash("Question deleted", "success")
    return redirect(url_for("questions"))


# ------------ Scores page (view) ------------

@app.route("/scores")
def scores():
    if "username" not in session:
        return redirect(url_for("login"))
    scores = load_json(SCORES_FILE, [])
    return render_template("scores.html", scores=scores)


# ------------ API for bot ------------

@app.route("/api/questions")
def api_questions():
    # returns JSON list of questions (bot can request)
    # optionally support ?lang=hi
    lang = request.args.get("lang")
    questions = load_json(QUESTIONS_FILE, [])
    if lang:
        questions = [q for q in questions if q.get("lang") == lang]
    return jsonify({"questions": questions})


@app.route("/api/scores", methods=["GET", "POST"])
def api_scores():
    # GET: return scores
    # POST: bot sends {"user_id": 123, "username": "abc", "score": 2, "total": 5}
    if request.method == "GET":
        data = load_json(SCORES_FILE, [])
        return jsonify({"scores": data})
    else:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"error": "invalid payload"}), 400

        user_id = payload.get("user_id")
        username = payload.get("username", "unknown")
        score = payload.get("score", 0)
        total = payload.get("total", 0)

        scores = load_json(SCORES_FILE, [])
        # append new record
        record = {"user_id": user_id, "username": username, "score": score, "total": total}
        scores.append(record)
        save_json(SCORES_FILE, scores)
        return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
