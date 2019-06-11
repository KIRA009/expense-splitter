var pass = document.getElementById('password');
var show_pass = document.getElementById('show-pass');

show_pass.addEventListener('click', toggle);

function toggle() {
	if (pass.attributes['type'].value == 'password') {
		pass.attributes['type'].value = 'text';
		show_pass.innerHTML = 'Hide password';
	}
	else {
		pass.attributes['type'].value = 'password';
		show_pass.innerHTML = 'Show password';
	}
}
