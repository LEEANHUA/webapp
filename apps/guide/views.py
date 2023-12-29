from flask import Blueprint, render_template

guide = Blueprint("guide", __name__, template_folder="templates")

@guide.route("/")
def index():
    return render_template("guide/index.html")

@guide.route("/end")
def end():
    return render_template("guide/end.html")