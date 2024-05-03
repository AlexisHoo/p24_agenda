const days = ['lundi','mardi','mercredi','jeudi','vendredi','samedi'];

for(let i = 0; i < list_days.length; i++){

    const dayDiv = document.getElementById(days[i]);
    const hourSlots = dayDiv.querySelectorAll('.hour-slot');

    index = 0

    hourSlots.forEach( (slot, index) => {
        
        //Ici faire une requête pour voir s'il existe un slot existant à cette div et index là
        slot.style.backgroundColor = "red";
    });
}