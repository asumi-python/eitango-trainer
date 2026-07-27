from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.word_service import get_all_active_words, create_word, soft_delete_word

bp = Blueprint("words", __name__)


@bp.route("/words")
def list_words():
    words = get_all_active_words()
    return render_template("words/list.html", words=words)


@bp.route("/words/new", methods=["GET", "POST"])
def new_word():
    if request.method == "POST":
        english = request.form["english"].strip()
        meaning = request.form["meaning"].strip()
        if english and meaning:
            create_word(english, meaning)
            flash(f"「{english}」を登録しました", "success")
            return redirect(url_for("words.new_word"))
        flash("英単語と意味を両方入力してください", "error")
    return render_template("words/new.html")


@bp.route("/words/<word_id>/delete", methods=["POST"])
def delete_word(word_id):
    english = request.form.get("english", "")
    soft_delete_word(word_id)
    flash(f"「{english}」を削除しました", "success")
    return redirect(url_for("words.list_words"))
