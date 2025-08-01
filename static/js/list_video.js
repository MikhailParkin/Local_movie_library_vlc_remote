var videoCards = document.getElementsByClassName('card');
var title = document.title
for (var i = 0; i < videoCards.length; i++) {
    var card  =  document.getElementById(videoCards[i].id)
    if (title === 'Serials' || title === 'MultSerial' || title === 'Seasons') {
        card.addEventListener('click', function () {
            console.log(`Serial ${this.id} clicked!`);
            console.log(title);
            fetchMultiSeries(`Seasons-${this.id.split('-')[1]}`)
            });
    }
    else {
    card.addEventListener('click', function () {
    console.log(`Movie ${this.id} clicked!`);
    console.log(title);
    playVideo(this.id)
    
    });
}
}

var listvideo  = document.getElementById('listvideo');

async function fetchMultiSeries(id) {
    let base = id.split('-')[0];
    let recID = id.split('-')[1];
    localStorage.setItem('Base', base)
    localStorage.setItem('RecID', recID)
    var apiUrl = `/localbase/api/listmultiseries/${base}/${recID}`

        const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data)
        createCard(data)
    }
}


function createCard(data) {

    listvideo.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
    let createDiv = document.createElement('div');
    
    let createImg = document.createElement('img');
    createImg.setAttribute('src', data[i].poster);
    let createInnerDiv = document.createElement('div');
    createInnerDiv.className = 'card-body';
    let createCardName = document.createElement('h3')
    createCardName.innerText = data[i].file_name;
    
    if (localStorage.getItem('Base') === 'Seasons') {
        createDiv.id = `Series-${data[i].id}`;
        createCardName.innerText = data[i].name;
        createDiv.addEventListener('click', () =>  fetchMultiSeries(`Series-${data[i].id}`))
    }
    if (localStorage.getItem('Base') === 'Series') {
        createDiv.id = `Series-${data[i].id}`; 
        createCardName.innerText = data[i].name;
        createDiv.addEventListener('click', () =>  playVideo(`Series-${data[i].id}`))
    }
    createDiv.className = 'card';
    createDiv.append(createImg);
    createDiv.append(createInnerDiv);
    createInnerDiv.append(createCardName);
    listvideo.append(createDiv)
    }

}

async function playVideo(videoID) {
    console.log('play',  videoID);
    let category = videoID.split('-')[0]
    let file_id  = videoID.split('-')[1]

    const response = await fetch(`/api/play/${category}/${file_id}`, {
       method: "GET",
       headers: { "Accept": "application/json" }
   });
   if (response.ok === true) {
       var data = await response.json();
   }
 
 };
