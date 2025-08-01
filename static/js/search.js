var searchField = document.getElementById('search-field');
var searchBtn = document.getElementById('searchBtn');

searchBtn.addEventListener('click', function () {

    
    fetchSearch(searchField.value)
    searchField.value = '';

})

var listvideo  = document.getElementById('listvideo');

async function fetchSearch(value) {
    console.log(value);
    // var apiUrl = `/search/api/${value}`

    //     const response = await fetch(apiUrl, {
    //     method: "GET",
    //     headers: { "Accept": "application/json" }

    // });

    // if (response.ok === true) {
    //     const data = await response.json();
    //     console.log(data)
    //     createCard(data)
    // }
}