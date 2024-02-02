from flask import Blueprint, render_template, session
import random
import uuid

guide = Blueprint("guide", __name__, template_folder="templates")

robot_names = ["man", "woman", "cyborg_man", "cyborg_woman", "cyborg", "robot_with_al_1", "robot_with_al_2", "robot_without_al_1", "robot_without_al_2", "thing"]
male_speaker = "EJM11"
female_speaker = "CJF04"
speakers = [male_speaker, female_speaker]
total = 10

@guide.route("/average_fullbody")
def index_average_fullbody():
    target_images = []
    original_audio = []
    for i in range(total):
        robot_name = robot_names[random.randint(0, len(robot_names)-1)]
        image = "robot_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        target_images.append(image)
        audio_number = format(random.randint(1, 50), '02')
        audio = "average_audio/" + audio_number + ".wav"
        original_audio.append(audio)
    session["target_images"] = target_images
    session["original_audio"] = original_audio
    session["total"] = total
    session["uuid"] = str(uuid.uuid4())
    return render_template("guide/index.html")

@guide.route("/average_face")
def index_average_face():
    target_images = []
    original_audio = []
    for i in range(total):
        robot_name = robot_names[random.randint(0, len(robot_names)-1)]
        image = "robot_face_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        target_images.append(image)
        audio_number = format(random.randint(1, 50), '02')
        audio = "average_audio/" + audio_number + ".wav"
        original_audio.append(audio)
    session["target_images"] = target_images
    session["original_audio"] = original_audio
    session["total"] = total
    session["uuid"] = str(uuid.uuid4())
    return render_template("guide/index.html")

@guide.route("/real_fullbody")
def index_real_fullbody():
    target_images = []
    original_audio = []
    for i in range(total):
        robot_name = robot_names[random.randint(0, len(robot_names)-1)]
        image = "robot_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        target_images.append(image)
        if robot_name == "man" or robot_name == "cyborg_man":
            speaker = male_speaker
        elif robot_name == "woman" or robot_name == "cyborg_woman":
            speaker = female_speaker
        else:
            speaker = speakers[random.randint(0, len(speakers)-1)]
        audio_number = format(random.randint(1, 50), '02')
        audio = "wav_original/" + speaker + "/" + audio_number + ".wav"
        original_audio.append(audio)
    session["target_images"] = target_images
    session["original_audio"] = original_audio
    session["total"] = total
    session["uuid"] = str(uuid.uuid4())
    return render_template("guide/index.html")

@guide.route("/real_face")
def index_real_face():
    target_images = []
    original_audio = []
    for i in range(total):
        robot_name = robot_names[random.randint(0, len(robot_names)-1)]
        image = "robot_face_image/" + robot_name + "/" + robot_name + "_" + str(random.randint(1, 10)) + ".png"
        target_images.append(image)
        if robot_name == "man" or robot_name == "cyborg_man":
            speaker = male_speaker
        elif robot_name == "woman" or robot_name == "cyborg_woman":
            speaker = female_speaker
        else:
            speaker = speakers[random.randint(0, len(speakers)-1)]
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