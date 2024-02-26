document.addEventListener("DOMContentLoaded", function() {

    // var inputs = document.getElementsByClassName('popup-button');
    
    // for (var i = 0; i < inputs.length; i++) {
    //     inputs[i].addEventListener('click', function() {

    //         document.getElementById('myPopup').style.display = 'block';
    //     });
    // }

    document.getElementById('close').addEventListener('click', function() {

        document.getElementById('myPopup').style.display = 'none';
    })

    window.addEventListener('click', function() {

        if (event.target == document.getElementById('myPopup')) {
            document.getElementById('myPopup').style.display = 'none';
        }
    
    })

    const popup_rdv = document.querySelectorAll('.popup-button');

    // Ajouter un écouteur de clic à chaque élément
    popup_rdv.forEach(pop => {
        pop.addEventListener('click', () => {

            document.getElementById('myPopup').style.display = 'block';

            var nom = document.querySelector('.nom-pop');
            var tel = document.querySelector('.tel-pop');
            var adresse = document.querySelector('.adresse-pop');
            var email = document.querySelector('.email-pop');
            var vitale = document.querySelector('.vitale-pop');
            var respo = document.querySelector('.respo-pop');
            var notes = document.querySelector('.note');

            slot = pop.dataset.slotInfo
            console.log(slot)

            slot = slot.split("_")
            nom_str = slot[0]
            tel_str = slot[1]
            adresse_str = slot[2]
            email_str = slot[3]
            vitale_str = slot[4]
            notes_str = slot[5]

            nom.querySelector('p').textContent = nom_str;
            tel.querySelector('p').textContent = tel_str;
            adresse.querySelector('p').textContent = adresse_str;
            email.querySelector('p').textContent = email_str;
            vitale.querySelector('p').textContent = vitale_str;
            // respo.querySelector('p').textContent = respo_str;
            notes.querySelector('p').textContent = notes_str;
           



        });

    });


});