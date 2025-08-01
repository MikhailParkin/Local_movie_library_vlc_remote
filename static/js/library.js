var select = document.getElementById('select-path')
var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
    select.style.display = "none";
};

window.onclick = function (event) {
    if (event.target === select) {
        select.style.display = "none";
    }
};

var addPathButtons = document.getElementsByClassName('select')
for (var i = 0; i < addPathButtons.length; i++) {
    let keyValue = addPathButtons[i].parentNode.id.split('-')[0];
    console.log(keyValue)
    addPathButtons[i].addEventListener('click', function () {
        clickPlus(keyValue);
        findPath(keyValue);
    });

};

var libName = document.getElementById('lib-name');
var addButton = document.getElementById('button-add')
addButton.addEventListener('click', addPath);

function clickPlus(key) {
    console.log(key)
};

function findPath(key) {

    select.style.display = "block";
    libName.innerText = `Добавить в библиотеку ${key}`
    addButton.value = key;
    get_path();

};


var depth_path = 0;
var list_paths = {};
var textPathBack = {};

async function get_path(dir) {
    console.log('DIR', dir)

    const response = await fetch(`api/library/getPath`, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            path: dir
        })
    });
    if (response.ok === true) {
        const data = await response.json();


        if (dir !== undefined) {
            depth_path++;

        }
        list_paths[`${depth_path}`] = data.result;
        textPathBack[`${depth_path}`] = dir;
        list_path(data.result);

    }
};


var textPath = document.getElementById('text-area');
var resultList = document.getElementById('list-path');

function list_path(data) {

    console.log('LIST:', list_paths);
    console.log('DATA:', data);
    resultList.innerHTML = '';

    if (depth_path > 0) {
        var newLi = document.createElement('li');
        newLi.className = "list-group-item d-flex justify-content-between align-items-center";
        var newNameDiv = document.createElement('div');
        newNameDiv.className = "ms-2 me-auto";
        newNameDiv.innerHTML = '&#x1f4c2; .. ';

        newNameDiv.style.cursor = 'pointer';
        newNameDiv.addEventListener('click', () => get_up_path());

        newLi.append(newNameDiv);
        resultList.append(newLi);

    }

    for (let i = 0; i < data.length; i++) {

        var newLi = document.createElement('li');
        newLi.className = "list-group-item d-flex justify-content-between align-items-center";
        var newNameDiv = document.createElement('div');
        newNameDiv.className = "ms-2 me-auto";
        newNameDiv.innerHTML = `&#128193; ${data[i]}`;

        newNameDiv.style.cursor = 'pointer';
        newNameDiv.addEventListener('click', () => {
            get_path(data[i]);
            textPath.value = data[i];

        });


        newLi.append(newNameDiv);
        resultList.append(newLi);

    }
    console.log(depth_path);
};

function get_up_path() {
    console.log('--', depth_path)
    depth_path = depth_path - 1;
    console.log('DEPTH:', depth_path, 'select', list_paths[`${depth_path}`])
    list_path(list_paths[`${depth_path}`]);
    if (textPathBack[`${depth_path}`] === undefined) {
        textPath.value = '';
    }
    else {
        textPath.value = textPathBack[`${depth_path}`];
    }
};


var deletePathButton = document.getElementsByClassName('delete')
for (var i = 0; i < deletePathButton.length; i++) {
    let keyValue = deletePathButton[i].id.split('-')[0];
    console.log(keyValue)
    deletePathButton[i].addEventListener('click', function () {
        clickPlus(keyValue);
        deletePath(keyValue);
    });

};


async function deletePath(id) {
    const response = await fetch(`api/library/delete/${id}`, {
        method: "DELETE",
        headers: { "Accept": "application/json" }
    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data);
        location.reload();
    }
};

async function addPath() {

    const response = await fetch(`api/library/add`, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            path: textPath.value,
            service: addButton.value
        })
    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data)
        select.style.display = "none";
        location.reload();
    }
};

var reloadButtons = document.getElementsByClassName('reload')
for (var i = 0; i < reloadButtons.length; i++) {
    let keyValue = reloadButtons[i].parentNode.id.split('-')[0];
    console.log(keyValue)
    reloadButtons[i].addEventListener('click', function () {
        clickPlus(keyValue);
        updateRecords(keyValue);
    });

};

async function updateRecords(key) {
    const response = await fetch(`api/library/update/${key}`, {
        method: "GET",
        headers: { "Accept": "application/json" }
    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data);
    }
};

