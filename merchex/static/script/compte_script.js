document.addEventListener("DOMContentLoaded", function() {

    document.getElementById('ajouter-patient').addEventListener('click', function() {
        
        document.getElementById('myPopup').style.display = 'block';
    });

    document.getElementById('close').addEventListener('click', function() {

        document.getElementById('myPopup').style.display = 'none';
    })

    window.addEventListener('click', function() {

        if (event.target == document.getElementById('myPopup')) {
            document.getElementById('myPopup').style.display = 'none';
        }
    
    })

});