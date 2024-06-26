document.addEventListener("DOMContentLoaded", function() {

    var nomsMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
    
    var dateSpan = document.getElementById('date_vue');
    var dateText = dateSpan.textContent || dateSpan.innerText;

    var components = dateText.split(' ');
    var month = components[0]; // "Feb."
    var day = components[1].replace(',', ''); // "21,"
    var year = components[2]; // "2024"

    // Convertir le mois en numéro (0-indexé)
    var monthIndex = new Date(Date.parse(month + ' 1, 2000')).getMonth() + 1;

    // Créer une chaîne de date au format "YYYY-MM-DD"
    var date_affiche = year + '-' + monthIndex.toString().padStart(2, '0') + '-' + day;
    date_affiche = date_affiche.replace(',', '')
    // var debutSemaine = new Date( date_affiche );
    var debutSemaine = new Date(Date.UTC(
        parseInt(date_affiche.substring(0, 4)), // Année
        parseInt(date_affiche.substring(5, 7)) - 1, // Mois (0-11)
        parseInt(date_affiche.substring(8, 10)) // Jour
    ));

    // console.log("Date actuelle: ", debutSemaine)

    //GetDay == 0 si dimanche, si on est un dimanche, on fait -6 sinon
    if(debutSemaine.getDay() == 0){
        debutSemaine.setDate(debutSemaine.getDate() - 6);
        // console.log("on est dimanche")
    }
    else{
        debutSemaine.setDate(debutSemaine.getDate() - debutSemaine.getDay() + 1); // +1 car on veut le lundi en premier
    }

    // console.log("Date debut de semaine: ", debutSemaine)

    var inputs = document.getElementsByClassName('date');
    for (var i = 0; i < inputs.length; i++) {
        // console.log("input: ", i,"__________", debutSemaine.toISOString().slice(0, 10), "\n");
        inputs[i].value = debutSemaine.toISOString().slice(0, 10);
    }

    function afficherSemaine() {

        console.log("afficher semaine")
 
        
        var datesSemaine = [];
        for (var i = 0; i < 7; i++) {
            var jour = new Date(debutSemaine);
            jour.setDate(jour.getDate() + i);
            datesSemaine.push(jour);
        }
        
        finSemaine = datesSemaine[ datesSemaine.length - 1]
        date_affiche = debutSemaine
        var affiche = nomsMois[debutSemaine.getMonth()];

        if (debutSemaine.getMonth() != finSemaine.getMonth()){

            affiche = affiche + " - " + nomsMois[finSemaine.getMonth()]
        }
        
        //Header
        document.getElementById('week').innerHTML = affiche

        //Jour de la semaine
        document.getElementById('lundi').innerHTML = 'Lundi ' + datesSemaine[ 0 ].getDate()
        document.getElementById('mardi').innerHTML = 'Mardi ' + datesSemaine[ 1 ].getDate()
        document.getElementById('mercredi').innerHTML = 'Mercredi ' + datesSemaine[ 2 ].getDate()
        document.getElementById('jeudi').innerHTML = 'Jeudi ' + datesSemaine[ 3 ].getDate()
        document.getElementById('vendredi').innerHTML = 'Vendredi ' + datesSemaine[ 4 ].getDate()
        document.getElementById('samedi').innerHTML = 'Samedi ' + datesSemaine[ 5 ].getDate()
    }

    afficherSemaine();

    document.getElementById('previousWeek').addEventListener('click', function() {
        var dateActuelle = debutSemaine;
        console.log('!!!', dateActuelle);
        var datePre = new Date(dateActuelle);
        datePre.setDate(dateActuelle.getDate() - 7);

        // Si on change d'heure, on rajoute un jour (Histoire de fuseau horaire)
        if(dateActuelle.toString().includes("normale") && datePre.toString().includes("été")){

            console.log("On retourne en heure d'été")
            datePre.setDate(datePre.getDate() + 1);
        }

        var dateInput = document.getElementById('date');
        // Définir la valeur de l'élément <input> avec la date actuelle
        console.log(datePre.toISOString().slice(0, 10));
        dateInput.value = datePre.toISOString().slice(0, 10);

    });

    document.getElementById('nextWeek').addEventListener('click', function() {
        var dateActuelle = debutSemaine;
        var dateSuivante = new Date(dateActuelle);
        dateSuivante.setDate(dateActuelle.getDate() + 7);

        // Prévoir les changements d'heures
        if(dateActuelle.toString().includes("normale") && dateSuivante.toString().includes("été")){

            console.log("On passe en heure d'été")
            dateSuivante.setDate(dateSuivante.getDate() + 1);
        }
        else if( dateActuelle.toString().includes("été") && dateSuivante.toString().includes("normale")){
            
            console.log("On passe en heure d'hiver")
        }
        

        var dateInput = document.getElementById('date');
        // Définir la valeur de l'élément <input> avec la date actuelle
        console.log(dateSuivante.toISOString().slice(0, 10));
        
        dateInput.value = dateSuivante.toISOString().slice(0, 10);
    });
});
