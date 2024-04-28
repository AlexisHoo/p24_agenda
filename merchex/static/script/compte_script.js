document.addEventListener("DOMContentLoaded", function() {

    document.getElementById('ajouter-patient').addEventListener('click', function() {

        document.getElementById('username_span').style.visibility = 'visible';
        document.getElementById('email_span').style.visibility = 'visible';
        document.getElementById('id_username').readOnly = false;
        document.getElementById('id_email').readOnly = false;

        document.getElementById('id_username').value = '';
        document.getElementById('id_email').value = '';
    
        document.getElementById('id_last_name').value = '';
        document.getElementById('id_first_name').value = '';
    
        document.getElementById('id_tel_patient').value = '';
        document.getElementById('id_numero_secu').value = '';
    
        document.getElementById('id_sexe').value = '';
        document.getElementById('id_date_naissance').value = '';
    
        document.getElementById('id_couleur_patient').value = '';
        document.getElementById('id_adresse_patient').value = '';

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

function openPopup(lastName, firstName, telPatient, username , email, numero_secu, sexe, date_naissance, couleur_patient, adresse_patient) {
    // console.log("HEYYYYYE")

    document.getElementById('myPopup').style.display = 'block';

    document.getElementById('username_span').style.visibility = 'hidden';
    document.getElementById('email_span').style.visibility = 'hidden';
    document.getElementById('id_username').readOnly = true;
    document.getElementById('id_email').readOnly = true;

    document.getElementById('id_username').value = username;
    document.getElementById('id_email').value = email;
    

    document.getElementById('id_last_name').value = lastName;
    document.getElementById('id_first_name').value = firstName;

    document.getElementById('id_tel_patient').value = telPatient;
    document.getElementById('id_numero_secu').value = numero_secu;

    document.getElementById('id_sexe').value = sexe;

    var dateString = date_naissance;
    var dateObj = new Date(dateString);
    var formattedDate = dateObj.getFullYear() + '-' + ('0' + (dateObj.getMonth() + 1)).slice(-2) + '-' + ('0' + dateObj.getDate()).slice(-2);
    document.getElementById('id_date_naissance').value = formattedDate;

    document.getElementById('id_couleur_patient').value = couleur_patient;
    document.getElementById('id_adresse_patient').value = adresse_patient;
}