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

    document.getElementById('inviter-button').addEventListener('click', function() {
        
        document.getElementById('myPopup-invit').style.display = 'block';
        console.log("Hello");
    });



    document.getElementById('close-invit').addEventListener('click', function() {

        document.getElementById('myPopup-invit').style.display = 'none';
    })

    window.addEventListener('click', function() {

        if (event.target == document.getElementById('myPopup-invit')) {
            document.getElementById('myPopup-invit').style.display = 'none';
        }
    
    })


});