# 音声を加工する関数を読み込む
import process

# Flask関連
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    methods = [
            {"display": "robopitch, 窓長512サンプル", "code": "robopitch_512"},
            {"display": "robopitch, 窓長1024サンプル", "code": "robopitch_1024"},
            {"display": "Inharmonic Warping, all, 一次関数", "code": "iw_all_1"},
            {"display": "Inharmonic Warping, vib, 一次関数", "code": "iw_vib_1"},
            {"display": "Inharmonic Warping, all, 二次関数", "code": "iw_all_2"},
            {"display": "Inharmonic Warping, vib, 二次関数", "code": "iw_vib_2"}
        ]
    if request.method == "GET":
        return render_template("index.html", methods=methods)
    if request.method == "POST":
        select_method = request.form["process_method"]
        for i in range(len(methods)):
            if methods[i]["code"] == select_method:
                methods[i]["selected"] = True
        result = int(request.form["parameter"])
        infile = "/work/miyamoto/bthesis/wav_original/CJF04/01.wav"
        if select_method == "robopitch_512":
            threshold = result * 3 / 100
            filepath = process.robopitch(infile, 512, threshold)
        elif select_method == "robopitch_1024":
            threshold = result * 3 / 100
            filepath = process.robopitch(infile, 1024, threshold)
        elif select_method == "iw_all_1":
            threshold = result * 120 / 100
            filepath = process.inharmonic_warping(infile, "all", 1, threshold)
        elif select_method == "iw_all_2":
            threshold = (101-result) * 64 / 100
            filepath = process.inharmonic_warping(infile, "all", 2, threshold)
        elif select_method == "iw_vib_1":
            threshold = result * 120 / 100
            filepath = process.inharmonic_warping(infile, "vib", 1, threshold)
        elif select_method == "iw_vib_2":
            threshold = (101-result) * 64 / 100
            filepath = process.inharmonic_warping(infile, "vib", 2, threshold)
        
        return render_template("index.html", methods=methods, filepath=filepath, result=result)

if __name__ == "__main__":
    app.run(port=8000, debug=True)