document.addEventListener("DOMContentLoaded", function() {

    var nomsMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
    date_affiche = new Date()


    function afficherSemaine(date) {

        console.log("afficher semaine")
        var debutSemaine = new Date(date);
        debutSemaine.setDate(debutSemaine.getDate() - debutSemaine.getDay() + 1);//+1 car on veut le lundi en premier 
        
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

    afficherSemaine(new Date());

    document.getElementById('previousWeek').addEventListener('click', function() {
        var dateActuelle = new Date(date_affiche);
        dateActuelle.setDate(dateActuelle.getDate() - 7);
        date_affiche = dateActuelle
        afficherSemaine(dateActuelle);
    });

    document.getElementById('nextWeek').addEventListener('click', function() {
        var dateActuelle = new Date(date_affiche);
        dateActuelle.setDate(dateActuelle.getDate() + 7); 
        date_affiche = dateActuelle
        afficherSemaine(dateActuelle);
    });
});
