var editButtons = document.getElementsByClassName('edit');
var activeButtons = document.getElementsByClassName('active');

for (let i = 0; i  <  editButtons.length; i++) {
    editButtons[i].addEventListener('click', function () {
        localStorage.setItem('fileID', this.parentNode.id);
        fetchKPinfo();
    })
    
};

for (let i = 0; i  <  activeButtons.length; i++) {
    activeButtons[i].addEventListener('click', function () {
        localStorage.setItem('fileID', this.parentNode.id);
        editFilePath(this.parentNode.id, 'active');
    })
};



async function fetchKPinfo() {
    var apiUrl = '/localbase/api/kpinfo_all'

    const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        createKPList(data)
    }
};

var listKPcontainer = document.getElementById('kpinfo');
var listModal = document.getElementById('kp-list');

function createKPList(data) {
    listModal.style.display = 'block';
    listKPcontainer.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
    
    var newLi = document.createElement('li');
    newLi.className = "list-group-item d-flex justify-content-between align-items-center";
    var newNameDiv = document.createElement('div');
    newNameDiv.className = "ms-2 me-auto";
    newNameDiv.innerText = data[i].name;
    newNameDiv.style.cursor = 'pointer';
    newNameDiv.id = data[i].id
    newNameDiv.addEventListener('click', () => editFilePath(`${data[i].id}`, "addValue"));
    newLi.append(newNameDiv);
    listKPcontainer.append(newLi);
    }
    };

var span3 = document.getElementById('close2');

span3.onclick = function() {
    listModal.style.display = "none";
    listKPcontainer.innerHTML = '';
   };

window.onclick = function(event) {
    if (event.target == listModal) {
    listModal.style.display = "none";
    listKPcontainer.innerHTML = '';
    }
 };

 var action = '';
 var file_id = '';
 var q = '';

 async function editFilePath(id, act) {
    
    if (act === 'addValue') {
        action = 'addValue';
        file_id = localStorage.getItem('fileID');
        q = id;
    }

    if ( act === 'active') {
        action = 'deactive';
        file_id = id;
    }

    var apiUrl = `/manage_kp_db/api/kpinfo/${action}/${file_id}?q=${q}`

    const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        alert('Изменения сохранены!');
        if (act === 'addValue') {
            listModal.style.display = "none";
        }
        else {
            location.reload();
        }
    }
};

var serialLinks = document.getElementsByClassName('serials');
for (let i = 0; i  <  serialLinks.length; i++) {
    serialLinks[i].addEventListener('click', function () {
        fetchMultiSeries(this.parentNode.id);
        
    })
    
};

var serialsModal = document.getElementById('serial-list')
var serialsListContainer = document.getElementById('serials')

var span4 = document.getElementById('close3');

span4.onclick = function() {
    serialsModal.style.display = "none";
    serialsListContainer.innerHTML = '';
   };


   async function fetchMultiSeries(file_id) {

    localStorage.setItem('FileID', file_id);
    var apiUrl = `/localbase/api/multiseries/${file_id}`

    const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        createMultiSeriesList(data)
    }
};

function createMultiSeriesList(data) {
    console.log(data)
    serialsModal.style.display = "block";
    for (let key of  Object.keys(data)) {
        if (key === 'Seasons') {
            var seasons = data[key]
            
        }
    }
    
    for (let i = 0; i < seasons.length; i++) {
        var createOlSeason = document.createElement('ol');
            createOlSeason.className = 'list-group list-group-numbered';
            createOlSeason.id = seasons[i].id;
            createOlSeason.value = seasons[i].file_name;
            let newSeasonTitle = document.createElement('h3');
            newSeasonTitle.style.cursor = 'pointer';
            newSeasonTitle.innerText = seasons[i].file_name;
            newSeasonTitle.addEventListener('click', () => editMultiSeriesData(`seasonID-${seasons[i].id}`, "Seasons"))
            serialsListContainer.append(newSeasonTitle);
            serialsListContainer.append(createOlSeason);
        var series =  data[seasons[i].file_name]
        for (let y = 0; y < series.length; y++){
            let newList = document.createElement('li');
            newList.className = "list-group-item d-flex justify-content-between align-items-center";
            let newDiv = document.createElement('div');
            newDiv.id = `episodeID-${series[y].id}`;
            newDiv.className = "ms-2 me-auto series";
            newDiv.innerText = series[y].file_name;
            newDiv.style.cursor = 'pointer';
            newList.append(newDiv);
            createOlSeason.append(newList);
        }
        
    }
    var seriesLinks  = document.getElementsByClassName('series');
    for (let i =  0; i < seriesLinks.length; i++) {
        seriesLinks[i].addEventListener('click', () => editMultiSeriesData(seriesLinks[i].id, "Series"));
    }
};


var searchForm = document.forms["editForm"];
var editForm = document.getElementById('editform');
var nameRus = searchForm.elements['nameRus'];
var image = document.getElementById('image');



async function editMultiSeriesData(id, base) {
    
    var recID = id.split('-')[1]
    localStorage.setItem('Base', base)
    localStorage.setItem('RecID', recID)
    var apiUrl = `/localbase/api/multiseries/${base}/${recID}`

        const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data)
        editForm.style.display = "block";
        nameRus.value = data.file_name;
        image.setAttribute('src', data.poster);
    }
}


var span5 = document.getElementById("close4");

span5.onclick = function() {
   editForm.style.display = "none";
   serialsListContainer.innerHTML = '';
   fetchMultiSeries(localStorage.getItem('FileID'))

 };

 window.onclick = function(event) {
   if (event.target == editForm) {
      editForm.style.display = "none";
      serialsListContainer.innerHTML = '';
      fetchMultiSeries(localStorage.getItem('FileID'))
   }
 };

 var saveBtn = document.getElementById('EditsaveBtn');
 saveBtn.addEventListener('click', saveData)
 const fileField = document.querySelector('input[type="file"]');


 async function saveData() {
    var newPoster = '';
    if ( fileField.files[0] !== undefined) {
        newPoster=fileField.files[0].name;
        console.log(newPoster)

    }
    let base = localStorage.getItem('Base')
    let recID = localStorage.getItem('RecID')
    if ( fileField.files[0] !== undefined) {
        uploadFile();
    }
    const response = await fetch(`/localbase/api/multiseries/${base}/${recID}`, 
        {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            
            file_name: nameRus.value,
            poster: newPoster,
        })
    });
    if (response.ok === true) {
        const data = await response.json();
    }
    else {
        const error = await response.json();
        console.log(error.message);
        
    }

 };

 async function uploadFile() {
    let base = localStorage.getItem('Base')
    let recID = localStorage.getItem('RecID')
    var apiUpload = `/localbase/api/upload/${base}/${recID}`;

    if ( fileField.files[0] !== undefined) {
        const formData = new FormData();
        formData.append('name', nameRus.value)
        formData.append("poster", fileField.files[0])

        try  {
        const uploadFile = await fetch(apiUpload, {
            method: "POST",
            body: formData,
        });
        const result = await uploadFile.json();
    console.log("Success:", result);
    editMultiSeriesData(`reload-${recID}`, base)
    fileField.value = '';
    fileField.files[0] = '';
    console.log(fileField)

    
    } catch (error) {
    console.error("Error:", error);
    }
    }

 }
