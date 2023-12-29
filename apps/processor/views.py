import soundfile as sf
from datetime import datetime
from pathlib import Path

# 音声を加工する関数を読み込む
import apps.processor.process as process

# Flask関連
from flask import Blueprint, render_template, request, current_app, send_from_directory

processor = Blueprint("processor", __name__, template_folder="templates", static_folder="static")

@processor.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("processor/index.html", result={})
    if request.method == "POST":
        # formの入力を辞書型で取得
        result = request.form.to_dict()
        infile = "/work/miyamoto/bthesis/wav_original/CJF04/01.wav"
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        filepath = Path(
            current_app.config["UPLOAD_FOLDER"], filename
        )
        if "RP_toggle" in result:
            threshold = int(result["RP_threshold"]) * 3 / 100
            win_len = 512 if result["RP_win_length"] == "1" else 1024
            output_audio, fs = process.robopitch(infile, win_len, threshold)
            sf.write(filepath, output_audio, fs, subtype='FLOAT')
        else:
            # 加工なしの音声をstaticに保存
            data, fs = sf.read(infile)
            sf.write(filepath, data, fs)
        
        return render_template("processor/index.html", filename=filename, result=result)
    
@processor.route("/audio/<path:filename>")
def audio_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)