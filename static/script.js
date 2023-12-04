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

window.onload = () => {
    for (let i = 0; i < inputElements.length; i++) {
        // 変更に合わせてイベントを発火する
        inputElements[i].addEventListener('input', () => {
            setCurrentValue(inputElements, currentValueElements)
        });
        // ページ読み込み時の値をセット
        setCurrentValue(inputElements, currentValueElements);
    }
}

function RobopitchOnchange() {
    if(document.getElementById("RobopitchToggle").checked) {
        document.getElementById("RobopitchThreshold").disabled = false;
        document.getElementById("RobopitchWindowLength").disabled = false;
    }else {
        document.getElementById("RobopitchThreshold").disabled = true;
        document.getElementById("RobopitchWindowLength").disabled = true;
        document.getElementById("RobopitchThreshold").value = "1";
        document.getElementById("RobopitchWindowLength").value = "1";
        setCurrentValue(inputElements, currentValueElements);
    }
}

function InharmonicWarpingOnchange() {
    if(document.getElementById("InharmonicWarpingToggle").checked) {
        document.getElementById("InharmonicWarpingParameter").disabled = false;
        document.getElementById("InharmonicWarpingSpectrum").disabled = false;
        document.getElementById("InharmonicWarpingFunction").disabled = false;
    }else {
        document.getElementById("InharmonicWarpingParameter").disabled = true;
        document.getElementById("InharmonicWarpingSpectrum").disabled = true;
        document.getElementById("InharmonicWarpingFunction").disabled = true;
        document.getElementById("InharmonicWarpingParameter").value = "1";
        document.getElementById("InharmonicWarpingSpectrum").value = "1";
        document.getElementById("InharmonicWarpingFunction").value = "1";
        setCurrentValue(inputElements, currentValueElements);
    }
}

function resetParameter() {
    // robopitchの入力をリセット
    document.getElementById("RobopitchThreshold").value = "1";
    document.getElementById("RobopitchWindowLength").value = "1";
    document.getElementById("RobopitchToggle").checked = false;
    RobopitchOnchange();
    // IWの入力をリセット
    document.getElementById("InharmonicWarpingParameter").value = "1";
    document.getElementById("InharmonicWarpingSpectrum").value = "1";
    document.getElementById("InharmonicWarpingFunction").value = "1";
    document.getElementById("InharmonicWarpingToggle").checked = false;
    InharmonicWarpingOnchange();
}