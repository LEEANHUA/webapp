from flask import Blueprint, render_template, session
import random

guide = Blueprint("guide", __name__, template_folder="templates")

@guide.route("/")
def index():
    robot_names = ["man", "woman", "cyborg_man", "cyborg_woman", "cyborg", "robot_with_al_1", "robot_with_al_2", "robot_without_al_1", "robot_without_al_2", "thing"]
    imagefiles = []
    total = 10
    for i in range(total):
        robot_name = robot_names[random.randint(0, 9)]
        imagefile = "robot_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        imagefiles.append(imagefile)
    session["imagefiles"] = imagefiles
    session["total"] = total
    return render_template("guide/index.html")

@guide.route("/end")
def end():
    return render_template("guide/end.html")