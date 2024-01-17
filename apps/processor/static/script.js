// input要素
const inputElements = document.getElementsByClassName('range');

// 埋め込む先の要素
const currentValueElements = document.getElementsByTagName("span");

// 現在の値を埋め込む関数
const setCurrentValue = (elements, targets) => {
    for (let i = 0; i < elements.length; i++) {
        targets[i].innerText = elements[i].value;
    }
}

// rangeの値をhiddenにコピーする関数
// 再生時に使用
function rangeValueCopy() {
    const hiddenElements = document.getElementsByClassName('hidden');
    for (let i = 0; i < inputElements.length; i++) {
        hiddenElements[i].value = inputElements[i].value;
    }
    return true;
}

// Robopitchのトグルがオンになったときに使用
function RobopitchOnchange() {
    if(document.getElementById("RobopitchToggle").checked) {
        document.getElementById("RobopitchThreshold").disabled = false;
        // document.getElementById("RobopitchWindowLength").disabled = false;
    }else {
        document.getElementById("RobopitchThreshold").disabled = true;
        // document.getElementById("RobopitchWindowLength").disabled = true;
        setCurrentValue(inputElements, currentValueElements);
    }
}

// リセットボタンが押された時に使用
function resetParameter() {
    // robopitchの入力をリセット
    document.getElementById("RobopitchThreshold").value = "1";
    // document.getElementById("RobopitchWindowLength").value = "1";
    document.getElementById("RobopitchToggle").checked = false;
    RobopitchOnchange();
}

window.addEventListener("DOMContentLoaded", function() {
    // ページ読み込み時の値をセット
    setCurrentValue(inputElements, currentValueElements);

    for (let i = 0; i < inputElements.length; i++) {
        // 変更に合わせてイベントを発火する
        inputElements[i].addEventListener('input', () => {
            setCurrentValue(inputElements, currentValueElements)
        });
    }

    const currentPosition = document.getElementById("currentPosition");
    const endPosition = document.getElementById("endPosition");
    const audioElement = document.querySelector("audio");

    let playtimer = null;

    // 再生開始したときに実行
    const startTimer = () => {
        // setInterval(関数, 時間)で一定時間毎に関数の処理を行う
        playtimer = setInterval(() => {
            currentPosition.textContent = convertTime(audioElement.currentTime);
        }, 500);
    };

    // 停止したときに実行
    const stopTimer = () => {
        this.clearInterval(playtimer);
    };

    // 再生時間の表記を[mm:ss]に整える
    const convertTime = (timePosition) => {
        timePosition = Math.floor(timePosition);
        let result = null;

        if (timePosition >= 60) {
            result = Math.floor(timePosition / 60);
            result += ":" + Math.floor(timePosition % 60).toString().padStart(2, '0');
        } else {
            result = "0:" + Math.floor(timePosition).toString().padStart(2, '0');
        }

        return result;
    };

    window.onload = () => {
        currentPosition.textContent = convertTime(audioElement.currentTime);
        endPosition.textContent = convertTime(audioElement.duration);
        startTimer();
        audioElement.play();
    };

    // 音声ファイルが最後まで再生されたときに実行
    audioElement.addEventListener("ended", e => {
        stopTimer();
        currentPosition.textContent = convertTime(audioElement.currentTime);
    });
  
})