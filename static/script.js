function RobopitchOnchange() {
    if(document.getElementById("RobopitchToggle").checked) {
        document.getElementById("RobopitchThreshold").disabled = false;
        document.getElementById("RobopitchWindowLength").disabled = false;
    }else {
        document.getElementById("RobopitchThreshold").disabled = true;
        document.getElementById("RobopitchWindowLength").disabled = true;
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