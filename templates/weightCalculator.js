


function setType() {

    var choices = document.getElementById('shapeChoices');
    var choice = choices.elements["shapeChoices"].value;

    if (choice === 'Prism') {
        document.getElementById("prismForm").style.display = "block";
        document.getElementById("cylinderForm").style.display = "none";
        document.getElementById("drumForm").style.display = "none";
        document.getElementById("yardBoxForm").style.display = "none";
        document.getElementById("gallonForm").style.display = "none";

    }

    else if (choice === 'Cylinder') {
        document.getElementById("prismForm").style.display = "none";
        document.getElementById("cylinderForm").style.display = "block";
        document.getElementById("drumForm").style.display = "none";
        document.getElementById("yardBoxForm").style.display = "none";
        document.getElementById("gallonForm").style.display = "none";
    }

    else if (choice === 'Drum') {
        document.getElementById("prismForm").style.display = "none";
        document.getElementById("cylinderForm").style.display = "none";
        document.getElementById("drumForm").style.display = "block";
        document.getElementById("yardBoxForm").style.display = "none";
        document.getElementById("gallonForm").style.display = "none";
    }

    else if (choice === 'Yard Box') {
        document.getElementById("prismForm").style.display = "none";
        document.getElementById("cylinderForm").style.display = "none";
        document.getElementById("drumForm").style.display = "none";
        document.getElementById("yardBoxForm").style.display = "block";
        document.getElementById("gallonForm").style.display = "none";
    }

    else if (choice === 'Gallon') {
        document.getElementById("prismForm").style.display = "none";
        document.getElementById("cylinderForm").style.display = "none";
        document.getElementById("drumForm").style.display = "none";
        document.getElementById("yardBoxForm").style.display = "none";
        document.getElementById("gallonForm").style.display = "block";
    }

}



function clearForm() {
    document.getElementById("prismForm").style.display = "none";
    document.getElementById("cylinderForm").style.display = "none";
    document.getElementById("drumForm").style.display = "none";
    document.getElementById("yardBoxForm").style.display = "none";
    document.getElementById("gallonForm").style.display = "none";
    document.getElementById('answer').innerHTML = ' '

}




//================================
//the following functions need to return volume in cubic feet
//================================


function prismCalc() {

    var length = document.getElementById('priLength').value;
    var width = document.getElementById('priWidth').value;
    var height = document.getElementById('priHeight').value;
    var answer = parseFloat(length) * parseFloat(width) * parseFloat(height)
    return answer

}


function cylinderCalc() {
    var diameter = document.getElementById('cylDiameter').value;
    var height = document.getElementById('cylHeight').value;
    var answer = (parseFloat(diameter) / 2)**2 * 3.14 * parseFloat(height)
    return answer
}


function drumCalc() {
    var numberOfDrums = document.getElementById('numDrums').value;
    var answer = parseFloat(numberOfDrums) * 7.35
    return answer
}


function yardBoxCalc() {
    var numberOfBoxes = document.getElementById('numBoxes').value;
    var answer = parseFloat(numberOfBoxes) * 27
    return answer
}


function gallonCalc() {
    var numberOfGallons = document.getElementById('numGallons').value;
    var answer = parseFloat(numberOfGallons) * 0.133681
    return answer

}


//========================
//end
//========================




//what this function does is take the value of substance input and the correct volume function
//and output the total weight

function getSubstance(s, volFunc) {
    var subs = {
        water: 62.42718356,
        dirt: 76.5,
        diesel: 53.11,
        ice: 56,
        kerosene: 52,
        mud: 115,
        asbestos: 153,
    }

    var vol = volFunc()
    var Weight = vol * subs[s]
    var totalWeight = Weight.toFixed(2)

    if (isNaN(totalWeight)) {
        document.getElementById('answer').innerHTML = 'Something is wrong';
    } else {
        document.getElementById('answer').innerHTML = totalWeight + ' LBS';
    }
}
