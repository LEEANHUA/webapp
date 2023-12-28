import soundfile as sf
from scipy import signal
from scipy import interpolate
import numpy as np
import pyworld as pw
import pysptk
import math
import librosa
import sys
from datetime import datetime

# 音声加工に使用する関数を定義

#---------------------------robopirch---------------------------
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
def robotization(input_audio, win_size, f0_fs, fs):
    N = len(input_audio)
    #窓の種類
    window = signal.blackman(win_size)
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

def robopitch(infile, win_size, threshold):
    input_audio, fs = sf.read(infile)
    voice_len = len(input_audio)
    fs, f0, ap, sp = feature_extract(infile)
    f0_fs = norm_threshold(infile, f0, voice_len, threshold)
    output_audio = robotization(input_audio, win_size, f0_fs, fs)
    outfile = "/home/miyamoto/public_html/webapp/apps/static/audio/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
    sf.write(outfile, output_audio, fs, subtype='FLOAT')
    return outfile

#---------------------------Inharmonic Warping---------------------------
#基本周波数抽出
#harvestかdio
def calc_f0(data, fs, function, frame_shift):
    if function == "harvest":
        f0_harvest, t = pw.harvest(data, fs, frame_period=frame_shift)
        return f0_harvest
    elif function == "dio":
        _f0, t = pw.dio(data, fs, frame_period=frame_shift)
        f0_dio = pw.stonemask(data, _f0, t, fs)
        return f0_dio
    else:
        raise ValueError("third argument must be \"harvest\" or \"dio\"")

#スペクトルをケプストラムに
def spec2cep(spec):
    target_logSpec = np.log10(abs(spec))
    for i in range(len(target_logSpec) // 2):
        target_logSpec[-i] = target_logSpec[i]
    cep = np.fft.ifft(target_logSpec)
    cep = cep.real
    return cep

#ケプストラムをスペクトルに
def cep2spec(cep):
    _logSpec = np.fft.fft(cep)
    logSpec = np.zeros(len(_logSpec))
    spec = np.zeros(len(_logSpec))
    for i in range(len(_logSpec)):
        logSpec[i] = _logSpec[i].real
        spec[i] = np.power(10, logSpec[i])
    return spec

#二次関数型
def expand_function_quadratic(i, window_len, f0, alpha, fs):
    if (i * fs / window_len < f0):
        return i
    else:
        f0_bin = f0 * window_len / fs
        return i + (window_len // 2- i) * (i - f0_bin) / (window_len // 2 - f0_bin) / alpha

#一次関数型
def expand_function_linear(i, window_len, f0, f_plus, fs):
    if (i * fs / window_len < f0):
        return i
    else:
        return i + f_plus * window_len / fs

#非線形変換
def expand_spectrum(target_spec, window_len,function, f0, parameter, fs):    
    #0:変換なし 1:一次関数型 2:二次関数型
    expand_freq = [0]
    for i in range(1, window_len // 2):
        if function == 0:
            expand_freq.append(i)
        elif function == 1:
            expand_freq.append(expand_function_linear(i, window_len, f0, parameter, fs))
        elif function == 2:
            expand_freq.append(expand_function_quadratic(i, window_len, f0, parameter, fs))
    #非線形に伸ばしたスペクトルの補間をする
    nonlinear = interpolate.interp1d(expand_freq, target_spec[:window_len // 2], kind="cubic")
    linear_freq = np.arange(0, window_len // 2)
    nonlinear_expanded_spec_half = nonlinear(linear_freq)
    #スペクトルの反転部分を追加する 
    nonlinear_expanded_spec = np.zeros(window_len, dtype=np.complex128)
    for i in range(len(nonlinear_expanded_spec_half)):
        nonlinear_expanded_spec[i] = nonlinear_expanded_spec_half[i]
        nonlinear_expanded_spec[-i-1] = nonlinear_expanded_spec_half[i]
    return nonlinear_expanded_spec

#inharmonicityを上昇させる
def increase_inharmonicity(data, spectrum, function, parameter, fs):
    window_len = 2048
    window_shift = window_len // 4
    window = signal.blackman(window_len)
    start = 0
    end = len(data)
    target_stft = []
    #基本周波数抽出のフレームシフトは0.5ms
    #48kHzで揃えるなら、1 / 48 ms
    frame_shift = 0.5
    f0_vector = calc_f0(data, fs, "harvest", frame_shift)
    if spectrum == "all":
        while (start + window_len < end) :
            target_signal = data[start:(start + window_len)] * window
            target_spec = np.fft.fft(target_signal)
            #非線形変換
            f0 = f0_vector[int((start + window_len / 2) / (48000 * 0.001 * frame_shift))]
            nonlinear_expanded_spec = expand_spectrum(target_spec, window_len, function, f0, parameter, fs)

            target_stft.append(nonlinear_expanded_spec[0:window_len // 2 + 1].tolist())
            start += window_shift
    elif spectrum == "vib":
        while (start + window_len < end) :
            flag = False
            target_signal = data[start:(start + window_len)] * window
            for i in target_signal:
                if i != 0:
                    flag = True
            #ケプストラムを用いて振動成分のみを抽出する
            target_spec_original = np.fft.fft(target_signal)
            cepstrum_vibration = spec2cep(target_spec_original)
            cepstrum_envelope = spec2cep(target_spec_original)
            for i in range(len(cepstrum_vibration) // 2):
                if i <= 30:
                    cepstrum_vibration[i] = 0
                    cepstrum_vibration[-i] = 0
                if i > 30:
                    cepstrum_envelope[i] = 0
                    cepstrum_envelope[-i] = 0
            target_envelope = cep2spec(cepstrum_envelope)
            target_spec = cep2spec(cepstrum_vibration)
            f0 = f0_vector[int((start + window_len / 2) / (48000 * 0.001 * frame_shift))]
            #非線形変換
            nonlinear_expanded_spec = expand_spectrum(target_spec, window_len, function, f0, parameter, fs)
            #非線形変換したスペクトルのケプストラムと元の音声のスペクトル包絡のケプストラムを足し合わせる
            nonlinear_expanded_cep = spec2cep(nonlinear_expanded_spec)
            target_cep = nonlinear_expanded_cep + cepstrum_envelope
            high_inharmonicity_spec = cep2spec(target_cep)
            if not flag:
                for i in range(window_len // 2 + 1):
                    high_inharmonicity_spec[i] = 0
            target_stft.append(high_inharmonicity_spec[0:window_len // 2 + 1].tolist())
            start += window_shift
    else:
        raise Exception("spectrum must be \"all\" or \"vib\"")
    return np.array(target_stft).T

def inharmonic_warping(infile, spectrum, function, parameter):
    data, fs = sf.read(infile)
    STFT = np.abs(increase_inharmonicity(data, spectrum, function, parameter, fs))
    data_griffinlim = librosa.griffinlim(STFT, n_iter=100, window="blackman", init = None)
    outfile = "/home/miyamoto/public_html/webapp/apps/static/audio/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
    sf.write(outfile, data_griffinlim/max(data_griffinlim), fs)
    return outfile

def robopitch_IW(infile, win_size, threshold, spectrum, function, parameter):
    # robopitch
    input_audio, fs = sf.read(infile)
    voice_len = len(input_audio)
    fs, f0, ap, sp = feature_extract(infile)
    f0_fs = norm_threshold(infile, f0, voice_len, threshold)
    data = robotization(input_audio, win_size, f0_fs, fs)
    # IW
    STFT = np.abs(increase_inharmonicity(data, spectrum, function, parameter, fs))
    data_griffinlim = librosa.griffinlim(STFT, n_iter=100, window="blackman", init = None)
    outfile = "/home/miyamoto/public_html/webapp/apps/static/audio/" + datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
    sf.write(outfile, data_griffinlim/max(data_griffinlim), fs)
    return outfile