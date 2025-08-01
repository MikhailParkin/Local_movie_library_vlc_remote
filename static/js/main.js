var menu = document.getElementById('menu');
/* Open the sidenav */
function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
    menu.style.display = 'none';
  }
  
  /* Close/hide the sidenav */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    menu.style.display = 'block';
  }

  var home = document.getElementById('home')
  home.addEventListener('click', function () 
  {
    location.href = '/home';
  });
  
  var adminPage = document.getElementById('admin')
  adminPage.addEventListener('click', function () 
  {
    location.href = '/adminpage';
  });  
  

// 
// Remote
// 
var remoteButton = document.getElementById('remote');
var remotewindow = document.getElementById('remotewindow');
var span2 = document.getElementById("close2");

span2.onclick = function() {
   remotewindow.style.display = "none";
   menu.style.display = 'block';
 }

remoteButton.addEventListener('click', function () 
{
    console.log('click');
    remotewindow.style.display = "block";
    document.getElementById("mySidenav").style.width = "0"

    remote();
});

var videoTitle = document.getElementById('videotitle');
var audioButtons = document.getElementById('audiolist');
var controlButtons = document.getElementById('control');
var seekbar = document.getElementById('seek');
var saveTime = document.getElementById('get-position');
var resume = document.getElementById('resume');

var printValue = document.getElementById('seconds');

seekbar.addEventListener('input', (event) => {
    let seekTime = event.target.value
    let hours = seekTime / 3600;
    hours = Math.floor(hours);
    let minuts = Math.floor((seekTime / 60) - (hours * 60));
    let seconds = seekTime % 60;
    // console.log(hours, minuts, seconds);
    printValue.innerText = `${hours}:${minuts}:${seconds}`;
});

seekbar.addEventListener('mouseup', (e) => {
    console.log('EEE', e.target.value);
    remote(`seek-${e.target.value}`)
});

seekbar.addEventListener("touchend", () => {
    remote(`seek-${seekbar.value}`)
});

seekbar.addEventListener("touchcancel", () => {
    remote(`seek-${seekbar.value}`)
});


var channalsVis = 0;
var navVis = 0;

var pauseButton = document.getElementById('pause');
pauseButton.addEventListener('click', function () 
{ remote(this.id)
});

var prevButton = document.getElementById('prev');
prevButton.addEventListener('click', function () 
{ remote(this.id)
});

var nextButton = document.getElementById('next');
nextButton.addEventListener('click', function () 
{ remote(this.id)
});

var quitButton = document.getElementById('quit');
quitButton.addEventListener('click', function () 
{ remote(this.id)
});

var suboffButton = document.getElementById('suboff');
suboffButton.addEventListener('click', function () 
{ remote(this.id)
});

var audioButton = document.getElementById('audio_list');
audioButton.addEventListener('click', function () 
{toggleAudiochannels(this.id)});

resume.addEventListener('click', () => {
    remote(`seek-${resumeTime - 10}`);
    console.log('resume')
});

function toggleAudiochannels(id) {
    if  (channalsVis === 0) {
        remote(id);
        channalsVis = 1;
    }
    else {
        audioButtons.innerHTML = '';
        channalsVis = 0;
    }
};


var  resumeTime = 0

async function remote(id) {
    var command = '';
    var q = '';

    if (id === undefined) {
        console.log('undefined');
        command = 'info';
    }
    else {
        
        console.log(id);
        var command = id;
        

    if (command.startsWith('atrack-')  === true  || 
        command.startsWith('seek-')  === true) {

        var commandPart = command.split('-');
        q = commandPart[1]
        command = commandPart[0]
        console.log(command);
    }
    }

    const response = await fetch(`/api/remote/${command}?q=${q}`, {
       method: "GET",
       headers: { "Accept": "application/json" }
   });
   if (response.ok === true) {
       var data = await response.json();
       console.log(data.output)
       if (command === 'info') {
       videoTitle.innerText = data.output['title']
       console.log(data.output['title'])
       rangeset(data.output['video_length'])
        if (data.output['last_position'] === null) {
            resume.style.display = "none";
            console.log('hide')
        }
        else {
            resume.style.display = "block";
            console.log('block')
            resumeTime = data.output['last_position']
        };

        if (data.output['table'] === 'Series') {
            let list_nav = document.getElementById('list_nav')
            list_nav.style.display = "block";
            console.log('block')
        }
        else {
            list_nav.style.display = "none";
            console.log('hide')
        };



       };
       if (command === 'quit') {
        remotewindow.style.display = 'none';
       };
   
       if (command === 'audio_list') {
       audioStrems(data.output);
       }
       if (command === 'time') {
        console.log(data.output);
       }
   }
}

function audioStrems(data) {
    console.log(data.length);
    audioButtons.innerHTML = '';
    for (var i=0; i < data.length; i++) {
        if (data[i].startsWith('-1') !== true) {
            console.log('audio: ', i, ' ', data[i])
            var createChannel = document.createElement('button');
            createChannel.id = `atrack-${i}`;
            createChannel.className = 'btncostum1';
            createChannel.innerText = data[i];
            audioButtons.append(createChannel);
            createChannel.addEventListener('click', function () 
            {remote(this.id)});
        }
    }
};

async function updateData(command) {
    
    const response = await fetch(`/api/remote/${command}`, 
        {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            id: videoID,
            cat: category
        })
    });
    if (response.ok === true) {
        const data = await response.json();
        
        localStorage.setItem('videoLenght', data.output.length);
        console.log('Изменения сохранены!');
        videoLenght = data.output.length;
        console.log(data.output.length);
        rangeset(data.output.length);
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }

 };

 function rangeset(length) {
    controlButtons.style.display = '';
    seekbar.max = length;
    seekbar.min = 0;
    seekbar.value = 0;

 };