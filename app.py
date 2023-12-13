import soundfile as sf
from datetime import datetime

# 音声を加工する関数を読み込む
import process

# Flask関連
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html", result={})
    if request.method == "POST":
        # formの入力を辞書型で取得
        result = request.form.to_dict()
        infile = "/work/miyamoto/bthesis/wav_original/CJF04/01.wav"
        if "RP_toggle" in result and "IW_toggle" in result:
            # robopitchで加工
            threshold = int(result["RP_threshold"]) * 3 / 100
            win_len = 512 if result["RP_win_length"] == "1" else 1024
            # IWで加工
            spectrum = "all" if result["IW_spectrum"] == "1" else "vib"
            function = int(result["IW_function"])
            if function == 1:
                parameter = int(result["IW_parameter"]) * 120 / 100
            else:
                parameter = (101 - int(result["IW_parameter"])) * 64 / 100
            filepath = process.robopitch_IW(infile, win_len, threshold, spectrum, function, parameter)
        elif "RP_toggle" in result:
            threshold = int(result["RP_threshold"]) * 3 / 100
            win_len = 512 if result["RP_win_length"] == "1" else 1024
            filepath = process.robopitch(infile, win_len, threshold)
        elif "IW_toggle" in result:
            spectrum = "all" if result["IW_spectrum"] == "1" else "vib"
            function = int(result["IW_function"])
            if function == 1:
                parameter = int(result["IW_parameter"]) * 120 / 100
            else:
                parameter = (101 - int(result["IW_parameter"])) * 64 / 100
            filepath = process.inharmonic_warping(infile, spectrum, function, parameter)
        else:
            # 加工なしの音声をstaticに保存
            data, fs = sf.read(infile)
            filepath = "./static/audio/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
            sf.write(filepath, data, fs)
        
        return render_template("index.html", filepath=filepath, result=result)

if __name__ == "__main__":
    app.run(debug=True)