import soundfile as sf
from scipy import signal
import numpy as np
import pyworld as pw
import pysptk
import math
import sys
from datetime import datetime

# Flask関連
from flask import Flask, render_template, request

#特徴量抽出
def feature_extract(file_name):
    f0_type = "harvest"
    data, fs = sf.read(file_name)
    if f0_type == "dio":
        _f0, t = pw.dio(data, fs)
        f0 = pw.stonemask(data, _f0, t, fs)
        ap = pw.d4c(data, f0, t, fs)
        sp = pw.cheaptrick(data, f0, t, fs)
        return fs, f0, ap, sp
    elif f0_type == "harvest":
        f0, t = pw.harvest(data, fs)
        ap = pw.d4c(data, f0, t, fs)
        sp = pw.cheaptrick(data, f0, t, fs)
        return fs, f0, ap, sp
    else:
        raise ValueError("third argument must be \"harvest\" or \"dio\"")

#メルケプ抽出
def wav2mcep(file_name):
    fs, f0, ap, sp = feature_extract(file_name)
    mcep = pysptk.sp2mc(sp, order=40, alpha = 0.55)
    mcep = np.delete(mcep, 0, 1)
    return mcep

#デルタ特徴量のノルム抽出
def delta_norm_feature(file_name):
    mcep = wav2mcep(file_name)
    delta = mcep
    n = len(mcep)
    m = len(mcep[0])
    for i in range(n):
        if i == 0:
            delta[i] = (mcep[1] - mcep[0]) * 0.5
        elif i == len(mcep) - 1:
            delta[i] = (mcep[i] - mcep[i-1]) * 0.5
        else:
            delta[i] = (mcep[i+1] - mcep[i-1]) * 0.5
    delta_norm = [0 for i in range(n)]
    for i in range(n):
        norm = 0
        for j in range(m):
            norm += delta[i][j] * delta[i][j]
        norm = np.sqrt(norm)
        delta_norm[i] = norm
    return delta_norm

#平均律
def f0_equal_temperament(f):
    if f <= 0:
        return 0
    else:
        log_f = math.log2(f/440.0)
        scale = round(log_f * 12, 0) / 12.0 + math.log2(440.0)
        return math.pow(2, scale)

#部分配列の0を除いた平均を計算
def f_mean_without_0(j, i, f):
    count = 0
    for k in range(j, i):
        if f[k] != 0:
            count += 1
    if count != 0:
        return np.sum(f[j:i])/count
    else:
        return 0

#動的特徴量のノルムと閾値からf0を変換、ただしf0_fsはfsベース
def norm_threshold(IN_FILE, f0, voice_len, threshold):
    delta_norm = delta_norm_feature(IN_FILE)
    f0_fs = [0 for i in range(voice_len)]
    j = 0
    for i in range(len(delta_norm)):
        if delta_norm[i] > threshold or i == (len(delta_norm)-1):
            f_mean = f_mean_without_0(j, i, f0)
            j_fs = int(j * voice_len / len(f0))
            i_fs = int(i * voice_len / len(f0))
            for k_fs in range(j_fs, i_fs):
                if int(f0[int(k_fs * len(f0) / voice_len )]) != 0:
                    f0_fs[k_fs] = f0_equal_temperament(f_mean)
            j = i
    return f0_fs

#robotizationを基本周波数離散化を元に適用する
def robotization(input_audio, win_size, window_type, f0_fs, fs):
    N = len(input_audio)
    #窓の種類
    window = np.hanning(win_size)
    if window_type == "hamming":
        window = signal.hamming(win_size)
    elif window_type == "blackman":
        window = signal.blackman(win_size)
    elif window_type == "bartlett":
        window = signal.bartlett(win_size)
    #input_audioの正規化
    input_audio = input_audio / max(np.abs(input_audio))
    output_audio = np.zeros(len(input_audio))
    #STFT部分
    pin = 0
    pend = len(input_audio)
    while (pin + win_size)  < pend:
        #grainは現在注目している系列
        #FFT→絶対値をとる（位相ゼロ）→IFFT→出力に足す
        grain = input_audio[pin:pin+win_size] * window
        f = np.fft.fft(grain)
        r = np.abs(f)
        grain = np.fft.fftshift(np.fft.ifft(r).real) * window
        output_audio[pin:pin+win_size] = output_audio[pin:pin+win_size] + grain
        if (int(f0_fs[pin]) != 0):
            pin += int(fs / f0_fs[pin])
        else:
            pin += win_size
            #pin += 1000
    output_audio = output_audio / max(np.abs(output_audio))
    return output_audio

# if __name__ == '__main__':
#     #入力
#     if len(sys.argv) != 6:
#         raise Exception('robopitch1.py infile outfile win_size threshold window_type')

#     IN_FILE = sys.argv[1]
#     OUT_FILE = sys.argv[2]
#     win_size = int(sys.argv[3])
#     threshold = float(sys.argv[4])
#     window_type = sys.argv[5]

#     input_audio, fs = sf.read(IN_FILE)
#     voice_len = len(input_audio)
#     fs, f0, ap, sp = feature_extract(IN_FILE)
#     f0_fs = norm_threshold(IN_FILE, f0, voice_len)
#     output_audio = robotization(input_audio, win_size, window_type, f0_fs)
#     sf.write(OUT_FILE, output_audio, fs, subtype='FLOAT')

def robopitch(infile, win_size, threshold, win_type):
    input_audio, fs = sf.read(infile)
    voice_len = len(input_audio)
    fs, f0, ap, sp = feature_extract(infile)
    f0_fs = norm_threshold(infile, f0, voice_len, threshold)
    output_audio = robotization(input_audio, win_size, win_type, f0_fs, fs)
    outfile = "./static/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
    sf.write(outfile, output_audio, fs, subtype='FLOAT')
    return outfile
    
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        
        result = int(request.form["parameter"])
        infile = "/work/miyamoto/bthesis/wav_original/CJF04/01.wav"
        threshold = result * 3 / 100
        filepath = robopitch(infile, 512, threshold, "blackman")
        
        return render_template("index.html", filepath=filepath, result=result)

if __name__ == "__main__":
    app.run(port=8000, debug=True)