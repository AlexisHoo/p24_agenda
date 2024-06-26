document.addEventListener("DOMContentLoaded", function() {

    document.getElementById('ajouter-patient').addEventListener('click', function() {

        document.getElementById('bouton-patient').value = "ajout";

        document.getElementById('username_span').style.visibility = 'visible';
        document.getElementById('email_span').style.visibility = 'visible';
        document.getElementById('firstname_span').style.visibility = 'visible';
        document.getElementById('lastname_span').style.visibility = 'visible';
        document.getElementById('id_username').readOnly = false;
        document.getElementById('id_email').readOnly = false;
        document.getElementById('id_last_name').readOnly = false;
        document.getElementById('id_first_name').readOnly = false;

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
        document.getElementById('id_type_rdv').value = '';

        document.getElementById('myPopup').style.display = 'block';
    });

    document.getElementById('close').addEventListener('click', function() {

        document.getElementById('myPopup').style.display = 'none';
    })

    document.getElementById('close-invit').addEventListener('click', function() {

        document.getElementById('popup-invit').style.display = 'none';
    })

    window.addEventListener('click', function() {

        if (event.target == document.getElementById('myPopup')) {
            document.getElementById('myPopup').style.display = 'none';
        }
        if (event.target == document.getElementById('popup-invit')) {
            document.getElementById('popup-invit').style.display = 'none';
        }
    
    })

    

});

function openInvit(patientId, nbr_rdv, nbr_semaine, modif_RDV){

    document.getElementById('popup-invit').style.display = 'block';
    console.log("ID PATIEZNT: ", patientId)
    document.getElementById('id_patient').value = patientId;

    console.log("NBR RDV: ", nbr_rdv)
    document.getElementById('id_nbr_RDV').value = nbr_rdv;
    document.getElementById('id_nbr_semaine').value = nbr_semaine;
    document.getElementById('id_modif_RDV').value = modif_RDV;
}

function afficheInvit(nbr_rdv, nbr_semaine, modif_RDV){

    document.getElementById('popup-invit').style.display = 'block';

    document.getElementById('id_nbr_RDV').value = nbr_rdv;
    document.getElementById('id_nbr_semaine').value = nbr_semaine;
    document.getElementById('id_modif_RDV').value = modif_RDV;
}

function openPopup(lastName, firstName, telPatient, username , email, numero_secu, sexe, date_naissance, couleur_patient, adresse_patient, type_rdv) {
    // console.log("HEYYYYYE")
    document.getElementById('bouton-patient').value = "modif"; 
    document.getElementById('username_modif').value = username; 
    document.getElementById('email_modif').value = email;
    

    document.getElementById('myPopup').style.display = 'block';

    document.getElementById('username_span').style.visibility = 'hidden';
    document.getElementById('email_span').style.visibility = 'hidden';
    document.getElementById('id_username').readOnly = true;
    document.getElementById('id_email').readOnly = true;

    document.getElementById('firstname_span').style.visibility = 'hidden';
    document.getElementById('lastname_span').style.visibility = 'hidden';
    document.getElementById('id_last_name').readOnly = true;
    document.getElementById('id_first_name').readOnly = true;

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
    document.getElementById('id_type_rdv').value = type_rdv;
}