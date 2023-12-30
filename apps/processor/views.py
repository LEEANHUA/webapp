import soundfile as sf
from datetime import datetime
from pathlib import Path

# 音声を加工する関数を読み込む
import apps.processor.process as process

# Flask関連
from flask import Blueprint, render_template, request, current_app, send_from_directory, session, url_for, redirect

processor = Blueprint("processor", __name__, template_folder="templates", static_folder="static")

@processor.route("/<number>", methods=["GET", "POST"])
def index(number):
    number = int(number)
    if request.method == "GET":
        return render_template("processor/index.html", result={}, imagefile=session["imagefiles"][number])
    if request.method == "POST":
        # formの入力を辞書型で取得
        result = request.form.to_dict()
        print(result)
        infile = "/work/miyamoto/bthesis/wav_original/CJF04/01.wav"
        filename = "audio/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        filepath = Path(
            current_app.config["UPLOAD_FOLDER"], filename
        )
        if result["button"] == "加工":
            if "RP_toggle" in result:
                threshold = int(result["RP_threshold"]) * 3 / 100
                win_len = 512 if result["RP_win_length"] == "1" else 1024
                output_audio, fs = process.robopitch(infile, win_len, threshold)
                sf.write(filepath, output_audio, fs, subtype='FLOAT')
            else:
                # 加工なしの音声をstaticに保存
                data, fs = sf.read(infile)
                sf.write(filepath, data, fs)
            return render_template("processor/index.html", filename=filename, result=result, imagefile=session["imagefiles"][number])
        else:
            if number + 1 == session["total"]:
                return redirect(url_for("guide.end"))
            else:
                return redirect(url_for("processor.index", number=number+1))
    
@processor.route("/audio/<path:filename>")
def audio_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@processor.route("/image/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)