document.addEventListener("DOMContentLoaded", function() {

    var inputs = document.getElementsByClassName('popup-button');
    
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('click', function() {

            document.getElementById('myPopup').style.display = 'block';
        });
    }

    document.getElementById('close').addEventListener('click', function() {

        document.getElementById('myPopup').style.display = 'none';
    })

    window.addEventListener('click', function() {

        if (event.target == document.getElementById('myPopup')) {
            document.getElementById('myPopup').style.display = 'none';
        }
    
    })


});