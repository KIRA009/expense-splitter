document.querySelectorAll('nav a').forEach(function(el) {
	el.addEventListener('click', toggle);
})

function toggle(evt) {
	evt.preventDefault();
	document.querySelectorAll('nav a').forEach(function(el) {
		if (el == evt.target) {
			document.getElementById(el.attributes['href'].value.slice(1, )).classList.add('display');
			el.classList.add('active');
		}
		else {
			document.getElementById(el.attributes['href'].value.slice(1, )).classList.remove('display');
			el.classList.remove('active');
		}
	})
}


var modal = document.getElementById('add');
var add_friend = document.querySelector('button[data-target="#add"]');
var exit = document.getElementsByClassName('exit')[0];
exit.addEventListener('click', toggle_display);
add_friend.addEventListener('click', toggle_display);

function toggle_display() {
	if (modal.classList.contains('show')) {
		modal.classList.remove('display');
		modal.classList.remove('show');
	}
	else {
		modal.classList.add('display');
		modal.classList.add('show');
	}
}
