const searchInput = document.getElementById('search');
const resultsContainer = document.getElementById('results-container');

function addClickListener(div) {
    div.addEventListener('click', () => {
        console.log("clique");
        searchInput.value = div.id.replace("_", " ");
    });
}

searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    if (query.length === 0) {
        resultsContainer.innerHTML = '';
        return;
    }

    fetch(`/add_rdv/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = '';
            data.forEach(patient => {
                const result = document.createElement('div');
                result.textContent = `${patient.nom} ${patient.prenom}`;
                result.id = `${patient.nom}_${patient.prenom}`;
                addClickListener(result);
                resultsContainer.appendChild(result);
            });
        })
        .catch(error => console.error('Error fetching search results:', error));
});

// Toutes les div des patients trouvés
var div_patients = resultsContainer.querySelectorAll('div')

div_patients.forEach( div => {

    div.addEventListener('click', () => {
        addClickListener(div);
    });
});