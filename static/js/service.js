var serviceButtons = document.getElementsByClassName('home');
for (var i = 0; i < serviceButtons.length; i++) {
    console.log(serviceButtons[i].id)
    var sButton  =  document.getElementById(serviceButtons[i].id)
    sButton.addEventListener('click', function () {
    console.log(`Button ${this.id} clicked!`);
    location.href = `/${this.id}`;
    });
}


