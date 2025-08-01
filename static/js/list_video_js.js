var listvideo  = document.getElementById('listvideo');
var title = document.title;
var videosList = {};
findBar = document.getElementsByClassName('sticky2');

fetch_data(title)

async function fetch_data(category) {
    var apiUrl = `/api/list_video/${category}`

        const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        // console.log(data);
        createCard(data);
        videosList = data;
        findBar[0].style.display = 'flex';
    }
}

function createCard(data) {
    listvideo.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
        // console.log(data[i].file_name)
    let createDiv = document.createElement('div');
    createDiv.className = 'card';
    let createImg = document.createElement('img');
    createImg.setAttribute('src', data[i].poster);
    let createInnerDiv = document.createElement('div');
    createInnerDiv.className = 'card-body';
    let createCardName = document.createElement('h3')
    createCardName.innerText = data[i].file_name;
    createDiv.id = `${title}-${data[i].id}`;

    if (title === 'Serials') {
        createDiv.id = `Seasons-${data[i].id}`;
    }
    
    if (title === 'Seasons') {
        createDiv.id = `Series-${data[i].id}`;
        createCardName.innerText = data[i].name;
    }

    if (title === 'Series') {
        createDiv.id = `Series-${data[i].id}`; 
        createCardName.innerText = data[i].name;
    }
  
    
    createDiv.addEventListener('click', cardAction)
    createDiv.append(createImg);
    createDiv.append(createInnerDiv);
    createInnerDiv.append(createCardName);
    listvideo.append(createDiv);
    }
}

function cardAction() {
    console.log(this.id);
    console.log(title);
    if (title === 'Serials' || title === 'MultSerial' || title === 'Seasons') {
            fetchMultiSeries(this.id)
    }
    else {
    console.log(`Movie ${this.id} clicked!`);
    console.log(title);
    playVideo(this.id)
    
}
}

async function fetchMultiSeries(id) {
    console.log('fetch: ', id)
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
        // console.log(data)
        // console.log('TITLE: ', base)
        title = base;
        // console.log('NEW TITLE: ', title)
        findBar[0].style.display = 'none'
        createCard(data)
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

 var finder = document.getElementById('finder');
 finder.addEventListener('input', function () {
    const findedVideo = [];   
    for (let i = 0; i < videosList.length; i++) {
       if (videosList[i].file_name.toLowerCase().includes(finder.value.toLowerCase())) {
            console.log(videosList[i].file_name);
            findedVideo.push(videosList[i]);
       }

    }
    console.log(finder.value);
    console.log(findedVideo);
    if (findedVideo.length === 0) {
        listvideo.style.height = "1000px";
        listvideo.innerHTML = "<h1>Ничего нет((</h1>";
    }
    else {
        listvideo.style.height = null;
        createCard(findedVideo);
    }
 });



var alfabet = document.getElementById('alphabet');
var premiere = document.getElementById('year');
var kpRate = document.getElementById('rate');

alfabet.addEventListener('click', sortContent);
premiere.addEventListener('click', sortContent);
kpRate.addEventListener('click', sortContent);

var pressedButton = '';
var countClick = 0;

function sortContent() {
   console.log(this.id)
   let sortButton = document.getElementById(this.id);
   const sortType = ['А - Я', 'Год выпуска', 'Рейтинг'];
   const sortTextDesc = ['А - Я \u2191', 'Год \u2191', 'Рейтинг \u2191']
   const sortTextAsc = ['А - Я \u2193', 'Год \u2193', 'Рейтинг \u2193']
   const listSortButtons = ['alphabet', 'year', 'rate']
   
   
   var buttonIndex = listSortButtons.indexOf(this.id);

   let data = videosList;
   let field = this.id;
   if (this.id === 'alphabet') {
      field = 'file_name';
   };

   
   if (pressedButton ===  '') {
      var newData = data.sort((a, b) => a[field] > b[field] ? 1 : -1);
      sortButton.innerText = sortTextAsc[buttonIndex];
      console.log('FIRST IF');
      
   }

   else if (pressedButton !== this.id) {
      let OLDsortButton = document.getElementById(pressedButton);
      var OLDbuttonIndex = listSortButtons.indexOf(pressedButton);
      OLDsortButton.innerText = sortType[OLDbuttonIndex];
      var newData = data.sort((a, b) => a[field] > b[field] ? 1 : -1);
      sortButton.innerText = sortTextAsc[buttonIndex];
      console.log("SECOND IF");
   }

   else if (pressedButton === this.id && countClick === 0) {
      var newData = data.sort((a, b) => a[field] < b[field] ? 1 : -1);
      sortButton.innerText = sortTextDesc[buttonIndex];
      countClick = 1

      console.log('THIRD IF');

   }

   else if (pressedButton === this.id && countClick === 1) {
      var newData = data.sort((a, b) => a[field] > b[field] ? 1 : -1);
      sortButton.innerText = sortTextDesc[buttonIndex];
      countClick = 0

      console.log('fourth IF');
   }
    pressedButton = this.id;
    // newData.forEach(item => console.log(item));
    createCard(newData);
};
