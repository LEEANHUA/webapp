from flask import Blueprint, render_template, session
import random
import uuid

guide = Blueprint("guide", __name__, template_folder="templates")

@guide.route("/")
def index():
    robot_names = ["man", "woman", "cyborg_man", "cyborg_woman", "cyborg", "robot_with_al_1", "robot_with_al_2", "robot_without_al_1", "robot_without_al_2", "thing"]
    speakers = ["CJF04", "CJF101", "EJF01", "EJF101", "EJF102", "CJM01", "EJM07", "EJM08", "EJM11", "EJM101"]
    male_speakers = ["CJM01", "EJM07", "EJM08", "EJM11", "EJM101"]
    female_speakers = ["CJF04", "CJF101", "EJF01", "EJF101", "EJF102"]
    target_images = []
    original_audio = []
    total = 10
    for i in range(total):
        robot_name = robot_names[random.randint(0, 9)]
        image = "robot_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        target_images.append(image)
        if robot_name == "man" or robot_name == "cyborg_man":
            speaker = male_speakers[random.randint(0, 4)]
        elif robot_name == "woman" or robot_name == "cyborg_woman":
            speaker = female_speakers[random.randint(0, 4)]
        else:
            speaker = speakers[random.randint(0, 9)]
        audio_number = format(random.randint(1, 50), '02')
        audio = "wav_original/" + speaker + "/" + audio_number + ".wav"
        original_audio.append(audio)
    session["target_images"] = target_images
    session["original_audio"] = original_audio
    session["total"] = total
    session["uuid"] = str(uuid.uuid4())
    return render_template("guide/index.html")

@guide.route("/end")
def end():
    return render_template("guide/end.html")