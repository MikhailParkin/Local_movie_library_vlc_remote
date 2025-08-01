var addButton = document.getElementById('add')
addButton.addEventListener('click', function () {
    console.log(`${this.id} clicked!`);
    localStorage.setItem('kpID', 'new');
    let  newData = {
        "kp_id": 'new',
        "kp_id": '',
        "year": '',
        "rate": '',
        "name": '',
        "describe": '',
        "list_files": [],
        "poster": '/static/img/categories/kinopoisk.jpg'
    }
    editProperties(newData);
});

var editButtons = document.getElementsByClassName('edit')

for (var i = 0; i < editButtons.length; i++) {
    editButtons[i].addEventListener('click', function () {
        console.log(`${this.id} clicked!`);
        fetchKP(this.id)
    })
}

var searchForm = document.forms["editForm"];
var editForm = document.getElementById('editform');

var kpId = searchForm.elements['kpId'];
var year = searchForm.elements['year'];
var rate = searchForm.elements['rate'];
var nameRus = searchForm.elements['nameRus'];
var describe = searchForm.elements['describe'];
var image = document.getElementById('image');
var filePath = document.getElementById('file-list')
var pathList = document.getElementById('list')

var addButtonPath = document.getElementById('add-filepath');
addButtonPath.addEventListener('click',function () {
    editFilePath(this.value, 'add')
})


function editProperties(data) {
    editForm.style.display = "block";
    pathList.innerHTML = '';
    videoID = data.id;
    kpId.value = data.kp_id;
    year.value = data.year;
    rate.value = data.rate;
    nameRus.value = data.name;
    describe.value = data.describe;
    image.setAttribute('src', data.poster);
    addButtonPath.value = data.id;
    if  (data.list_files.length === 0) {
        filePath.style.display = 'none';

    }
    else {
        filePath.style.display = 'block';
        for  (let i = 0; i < data.list_files.length; i++) {
            console.log(data.list_files[i].id)
            var newLi = document.createElement('li');
            newLi.className = 'list-group-item d-flex justify-content-between align-items-center';

            var newDiv = document.createElement('div');
            newDiv.className = "file ms-2 me-auto";
            newDiv.innerHTML = data.list_files[i]['file_path']

            var newSpan = document.createElement('span');
            newSpan.id = data.list_files[i]['id'];
            
            newSpan.className = "btn btn-secondary deletefilepath";
            newSpan.innerText = 'Delete';
            pathList.append(newLi);
            newLi.append(newDiv);
            newLi.append(newSpan);

            newSpan.addEventListener('click', function () {
                console.log(`Button ${this.id} clicked!`);
                editFilePath(this.id, 'delete');
                newLi.remove();
                });
        }
    }
    
};

var action = '';
var file_id = '';
var q = '';

async function editFilePath(id, act) {
    
    console.log(`Button ${id} clicked! Action: ${act}`);
    if (act === 'delete') {
        action = 'deletepath';
        file_id = id;
    }
    if (act === 'add') {
        action = 'addpath';
        file_id = id;
    }

    if (act === 'addValue') {
        action = 'addValue';
        file_id = id;
        q = localStorage.getItem('kpID');
    }
    
    var apiUrl = `/manage_kp_db/api/kpinfo/${action}/${file_id}?q=${q}`

    console.log(apiUrl)


    const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        if (act === 'add') {
            createFileList(data.result);
            console.log(data.result)
        }

        if (act === 'addValue') {
            console.log(data.result);
            fileList.style.display = "none";
        }
        fetchKP(localStorage.getItem('kpID'))
    }
};


async function fetchKP(id) {
    var apiUrl = `/manage_kp_db/api/kpinfo/${id}`
    localStorage.setItem('kpID', id);


    const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data.result);
        editProperties(data.result);

    }
};

var span = document.getElementsByClassName("close")[0];

span.onclick = function() {
   editForm.style.display = "none";
   pathList.innerHTML = '';

 };

 window.onclick = function(event) {
   if (event.target == editForm) {
      editForm.style.display = "none";
      pathList.innerHTML = '';
   }
 };


var fileList = document.getElementById('filelist');
var span3 = document.getElementById('close2');
var files = document.getElementById('files');
var selectCat = document.getElementById('cat');


span3.onclick = function() {
    fileList.style.display = "none";
    location.reload();
   };

window.onclick = function(event) {
    if (event.target == fileList) {
    fileList.style.display = "none";
    }
 };

function createFileList(data) {
    fileList.style.display = 'block';
    files.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
    
        console.log(data[i])
    
    var newLi = document.createElement('li');
    newLi.className = "list-group-item d-flex justify-content-between align-items-center";
    var newNameDiv = document.createElement('div');
    newNameDiv.className = "ms-2 me-auto";
    newNameDiv.innerText = data[i].file_name;
    newNameDiv.style.cursor = 'pointer';
    newNameDiv.addEventListener('click', () => editFilePath(`${data[i].id}`, "addValue"));
    newLi.append(newNameDiv);
    files.append(newLi);
    }
    };


let saveBtn = document.getElementById('saveBtn');
saveBtn.addEventListener("click", showPosterDialog);

var dialogPoster = document.getElementById("dialog-poster");
var checkPoster = document.getElementById('check-poster');
var checkLablePoster = document.getElementById('checklable-poster');
const fileField = document.querySelector('input[type="file"]');
dialogPoster.addEventListener('close', dialogFunc); 


function showPosterDialog() {

    if ( fileField.files[0] !== undefined) {
        dialogPoster.showModal();

    }
    else {
        saveData();
    }
    
};

function dialogFunc() {
        let q = 'n';
        console.log(dialogPoster.returnValue);
        if (dialogPoster.returnValue === 'OK') {
        
        if (checkPoster.checked === true)  {
            console.log('Checkbox checked!');
            q = 'y';
            checkPoster.checked = false;
        }

        console.log(`Upload!!!! checked?: ${q}`);
        saveData();
        uploadFile(q);
        }
        else {
            console.log('NOT Upload!!!!');
        }
        fileField.value = null;
        dialogPoster.close();

 };
 


 async function saveData() {
    var newPoster = '';
    if ( fileField.files[0] !== undefined) {
        newPoster=fileField.files[0].name;
        console.log(newPoster)

    }
    const response = await fetch(`/manage_kp_db/api/kpinfo/${localStorage.getItem('kpID')}`, 
        {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            
            kp_id: kpId.value,
            poster: newPoster,
            year: year.value,
            rate: rate.value,
            name: nameRus.value,
            describe: describe.value,
            
        })
    });
    if (response.ok === true) {
        const data = await response.json();
        console.log(data)
        if (localStorage.getItem('kpID') === 'new') {
            alert('Запись добавлена!');
            editForm.style.display = "none";
            fetchKP(data);
            
        }
        else {
        alert('Изменения сохранены!');
        editForm.style.display = "none";
        if (localStorage.getItem('kpID') === 'new') {
            location.reload();
        }
        else {
        fetchKP(localStorage.getItem('kpID'));
        }
        }
    }
    else {
        const error = await response.json();
        console.log(error.message);
        
    }

 };

 async function uploadFile(q) {
    var apiUpload = `/manage_kp_db/api/kpinfo/upload/${localStorage.getItem('kpID')}?q=${q}`;

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
    
    } catch (error) {
    console.error("Error:", error);
    }
    }

 }
