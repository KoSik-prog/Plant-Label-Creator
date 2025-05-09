function createLabel() {
    const line1 = document.getElementById('line_1').value.trim();
    const line2 = document.getElementById('line_2').value.trim();
    const labelSize = document.querySelector('input[name="labelSize"]:checked')?.value;

    if (!line1 && !line2) {
        alert('Both lines are empty. Please enter at least one line.');
        return;
    }

    const linesToSend = [];
    if (line1) {
        linesToSend.push(line1);
    }
    if (line2) {
        linesToSend.push(line2);
    }

    console.log('Lines to send:', linesToSend);

    if (labelSize === 'small') {
        eel.generate_label_small(linesToSend);
    } else if (labelSize === 'big') {
        eel.generate_label_big(linesToSend);
    } else {
        alert('Please select a label size.');
    }
}


function clearFields() {
    document.getElementById('line_1').value = '';
    document.getElementById('line_2').value = '';
    document.querySelectorAll('input[name="labelSize"]').forEach(input => input.checked = false);
}