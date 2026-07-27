from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.word_service import get_random_word, record_answer, mark_mastered
from app.services.settings_service import get_settings

bp = Blueprint("quiz", __name__)


@bp.route("/")
def index():
    word = get_random_word()
    settings = get_settings()
    return render_template("quiz/index.html", word=word, settings=settings)


@bp.route("/score", methods=["POST"])
def score():
    word_id = request.form["word_id"]
    correct = request.form["result"] == "correct"
    settings = get_settings()

    word_english = request.form.get("word_english", "")
    mastered = record_answer(word_id, correct, settings)

    if mastered:
        flash(f"「{word_english}」を覚えた単語として除外しました！", "success")

    return redirect(url_for("quiz.index"))


@bp.route("/master", methods=["POST"])
def master():
    word_id = request.form["word_id"]
    word_english = request.form.get("word_english", "")
    mark_mastered(word_id)
    flash(f"「{word_english}」を覚えた単語として除外しました！", "success")
    return redirect(url_for("quiz.index"))
