var backUp = document.getElementById('backup');
var restore = document.getElementById('restore');
var lengthBtn = document.getElementById('length');
var backUplist = document.getElementById('cat');
var playlistText = document.getElementById('playlist-url');
var playlistConfirm = document.getElementById('playlist-confirm');
var playlistUpdate = document.getElementById('playlist-update');
var epgUpdate = document.getElementById('epg-update');

window.addEventListener('load', function () 
{
    get_playlist_url();
    });

async function get_playlist_url() {
       const response = await fetch(`adminpage/api/playlist`, 
        {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            
            playlist: playlistText.value,
            
        })
    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data);
        playlistText.value = data
    }
};

playlistConfirm.addEventListener('click', function () {
    get_playlist_url();

});

playlistUpdate.addEventListener('click', function () {
    updateLists('playlist');

});

epgUpdate.addEventListener('click', function () {
    updateLists('epg');

});


async function updateLists(key) {
    const response = await fetch(`/adminpage/api/playlist_update/${key}`, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data);
        alert(data)
    }
};


backUp.addEventListener('click', function () {
    console.log(this.id)
    action(this.id, '')
})

restore.addEventListener('click', function () {
    console.log(this.id)
    console.log(backUplist.value)
    if (backUplist.value !== '') {
        action(this.id, backUplist.value)
    }
})

lengthBtn.addEventListener('click', function () {
    console.log(this.id)
    action(this.id, '')
})

async function action(action, value) {
    var q = value
    var apiUrl = `/localbase/api/adminpage/${action}?q=${q}`

        const response = await fetch(apiUrl, {
        method: "GET",
        headers: { "Accept": "application/json" }

    });

    if (response.ok === true) {
        const data = await response.json();
        console.log(data)
        alert(data.output)
        location.reload()
    }
}

var kpbase = document.getElementById('kpbase')
kpbase.addEventListener('click', function () 
{
  location.href = '/kpbase';
});

var localBase = document.getElementById('local-base')
localBase.addEventListener('click', function () 
{
  location.href = '/localbase';
});

var lib = document.getElementById('lib')
lib.addEventListener('click', function () 
{
  location.href = '/manage_local_db/library';
});