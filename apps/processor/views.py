import soundfile as sf
from datetime import datetime
from pathlib import Path
from apps.app import db
from apps.processor.models import Answer

# 音声を加工する関数を読み込む
import apps.processor.process as process

# Flask関連
from flask import Blueprint, render_template, request, current_app, send_from_directory, session, url_for, redirect

processor = Blueprint("processor", __name__, template_folder="templates", static_folder="static")

@processor.route("/<number>", methods=["GET", "POST"])
def index(number):
    number = int(number)
    if request.method == "GET":
        return render_template("processor/index.html", result={}, imagefile=session["target_images"][number], number=number)
    if request.method == "POST":
        # formの入力を辞書型で取得
        result = request.form.to_dict()
        infile = current_app.config["UPLOAD_FOLDER"] + "/" + session["original_audio"][number]
        filename = "processed_audio/" + session["uuid"] + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        filepath = Path(
            current_app.config["UPLOAD_FOLDER"], filename
        )
        if result["button"] == "再生":
            input_audio, fs = sf.read(infile)
            if "pitch_toggle" in result:
                shift = int(result["pitch_shift"])
                input_audio, fs = process.pitch_shift(input_audio, fs, shift)
            if "RP_toggle" in result:
                # 入力の範囲は1~100なので、それを1~2になるように調整
                threshold = (int(result["RP_threshold"]) + 98) / 99
                # 処理速度を早めるため、窓長は1024で固定
                win_len = 1024
                output_audio, fs = process.robopitch(input_audio, fs, win_len, threshold)
                sf.write(filepath, output_audio, fs, subtype='FLOAT')
            else:
                # 加工なしの音声をstaticに保存
                sf.write(filepath, input_audio, fs)
            return render_template("processor/index.html", filename=filename, result=result, imagefile=session["target_images"][number], number=number)
        else:
            answer = Answer(
                uuid=session["uuid"],
                image_path=session["target_images"][number],
                audio_path=session["original_audio"][number],
                processed="RP_toggle" in result,
                threshold=(int(result["RP_threshold"]) + 98) / 99 if "RP_toggle" in result else "",
                window_length=1024 if "RP_toggle" in result else "",
                pitch_shifted="pitch_toggle" in result,
                pitch_shift=int(result["pitch_shift"]) if "pitch_toggle" in result else "",
            )
            db.session.add(answer)
            db.session.commit()
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