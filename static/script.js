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