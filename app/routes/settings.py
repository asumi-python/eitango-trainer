from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.settings_service import get_settings, save_settings

bp = Blueprint("settings", __name__)


@bp.route("/settings", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mastery_mode = request.form.get("mastery_mode", "manual")
        streak_target = int(request.form.get("streak_target", 3))
        streak_target = max(1, min(20, streak_target))
        save_settings(mastery_mode, streak_target)
        flash("設定を保存しました", "success")
        return redirect(url_for("settings.index"))

    current = get_settings()
    return render_template("settings/index.html", settings=current)
