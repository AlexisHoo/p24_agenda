document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le premier bouton image
    const firstButton = document.getElementById('first-button');
    // Définir une variable pour suivre l'état actuel de l'image du premier bouton
    let isFirstImage = true;
    
    // Écoutez le clic sur le premier bouton image
    firstButton.addEventListener('click', function() {

        event.stopPropagation();
        var hourSlot = this.parentElement;
        if (isFirstImage) {
            firstButton.style.backgroundImage = "url('../../static/img/weekly/unlock.png')";
            
            hourSlot.style.backgroundColor = 'white';
        } else {
            firstButton.style.backgroundImage = "url('../../static/img/weekly/lock.png')";
            hourSlot.style.backgroundColor = '#f0f0f0';
        }
        // Inversez l'état actuel de l'image du premier bouton
        isFirstImage = !isFirstImage;
    });


    const secondButton = document.getElementById('second-button');
    let isFirstImageSecond = true
    // Écoutez le clic sur le premier bouton image
    secondButton.addEventListener('click', function() {

        event.stopPropagation();

        var hourSlot = this.parentElement;
        if (isFirstImageSecond) {
            // Si c'est la première image, changez-la en deuxième image
            secondButton.style.backgroundImage = "url('../../static/img/weekly/bin.png')";
            hourSlot.style.backgroundColor = 'lightgreen';
        } else {
            secondButton.style.backgroundImage = "url('../../static/img/weekly/add.png')";
            hourSlot.style.backgroundColor = '#f0f0f0';
        }
        // Inversez l'état actuel de l'image du premier bouton
        isFirstImageSecond = !isFirstImageSecond;
    });
 
    
    document.getElementById('popup-button').addEventListener('click', function() {
        
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