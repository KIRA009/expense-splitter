// Toggling between tabs

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

// Toggling add friend modal
var add = document.getElementById('add');
var add_friend = document.querySelector('button[data-target="#add"]');
var exit = document.getElementsByClassName('exit')[0];
exit.addEventListener('click', toggle_add_friend);
add_friend.addEventListener('click', toggle_add_friend);

function toggle_add_friend() {
	if (add.classList.contains('show')) {
		add.classList.remove('display');
		add.classList.remove('show');
		add_exp.style.display = 'block';
	}
	else {
		add.classList.add('display');
		add.classList.add('show');
		add_exp.style.display = 'none';
	}
}

// toggling add expense modal
var add_exp = document.querySelector('button[data-target="#exp"]');
var exp = document.getElementById('exp');
var exit = document.getElementsByClassName('exit')[1];
exit.addEventListener('click', toggle_add_exp);
add_exp.addEventListener('click', toggle_add_exp);

function toggle_add_exp() {
	if (add_exp.classList.contains('clicked')) {
		exp.classList.remove('display');
		exp.classList.remove('show');
		add_exp.classList.remove('clicked');
		remove_emails(email_ids);
	}
	else {
		exp.classList.add('display');
		exp.classList.add('show');
		add_exp.classList.add('clicked');
		add_emails(email_ids);
	}
}


// toggling friends dropdown
var friendsdropbut = document.getElementById('friendsdrop');
friendsdropbut.addEventListener('click', toggle_friendsdropdown);
var friendsdropdown = document.getElementsByClassName('dropdown')[0];
var friendsdrop = document.querySelector('div[aria-labelledby="friendsdrop"]');

function toggle_friendsdropdown() {
	if (friendsdropdown.classList.contains('show')) {
		friendsdropdown.classList.remove('show');
		friendsdrop.classList.remove('show');
	}
	else {
		friendsdropdown.classList.add('show');
		friendsdrop.classList.add('show');
	}
}


// adding and removing emails
var emails = document.getElementById('emails');
var expense = document.querySelector('input[name="expense"]');
expense.setAttribute('disabled', true);
var email_ids = new Object();
email_ids[emails.getAttribute('name')] = 0;
var even = document.getElementById('even');
even.onclick = (evt) => {
	if (even.checked) {
		for (var key in email_ids)
			email_ids[key] = expense.value / Object.keys(email_ids).length;
		expense.removeAttribute('disabled');
	}
	else
		expense.setAttribute('disabled', true);
	add_emails(email_ids);
}

expense.oninput = () => {
	if (even.checked) {
		for (var key in email_ids)
			email_ids[key] = expense.value / Object.keys(email_ids).length;
	}
	add_emails(email_ids);
}

document.querySelectorAll('.friend .name').forEach(function(el) {
	el.addEventListener('click', add_email);
})

friendsdrop.querySelectorAll('a').forEach(function(el) {
	el.addEventListener('click', add_email);
});

function add_email(evt) {
	var email = evt.target.innerHTML;
	if (evt.target.nodeName == 'A')
		evt.preventDefault();
	else
		toggle_add_exp();
	for (var key in emails) {
		if (key == email)
			return;
	}
	email_ids[email] = 0;
	friendsdrop.querySelectorAll('a').forEach(function(el) {
		if (el.innerHTML == email) {
			el.remove();
			return;
		}
	});
	add_emails(email_ids);
}

function remove_email(evt) {
	var email = evt.target.previousElementSibling.childNodes[0].textContent;
	var a = document.createElement('a');
	a.classList.add('dropdown-item');
	a.setAttribute('href', '#');
	a.textContent = email;
	a.addEventListener('click', add_email);
	friendsdrop.appendChild(a);

	evt.preventDefault();
	evt.target.previousElementSibling.remove();
	evt.target.remove();

	delete email_ids[email];
	add_emails(email_ids);
}

function add_emails(arr) {

	emails.innerHTML = '';
	for (var key in arr) {
		var span = document.createElement('span');
		span.textContent = key;
		var input = document.createElement('input');
		input.setAttribute('type', 'number');
		input.style.width = '60px';
		input.style.marginLeft = '10px';
		if (even.checked) {
			input.setAttribute('disabled', true);
			arr[key] = expense.value / Object.keys(arr).length;
		}
		else {
			input.removeAttribute('disabled');
		}
		input.setAttribute('value', arr[key]);
		input.oninput = get_total;
		span.appendChild(input);
		emails.appendChild(span);

		if (key == emails.getAttribute('name'))
			continue;
		var a = document.createElement('a');
		a.classList.add('remove');
		a.addEventListener('click', remove_email);
		a.textContent = ' x';
		emails.appendChild(a);
	}
}

function get_total(evt) {
	email_ids[evt.target.previousSibling.textContent] = evt.target.value;
	expense.value = parseInt(0, 10);
	for (var key in email_ids) {
		expense.value = parseInt(expense.value, 10) + parseInt(email_ids[key], 10);
	}
}

function remove_emails(arr) {
	for (var key in arr) {
		if (key == emails.getAttribute('name'))
			continue;
		var a = document.createElement('a');
		a.classList.add('dropdown-item');
		a.setAttribute('href', '#');
		a.textContent = key;
		a.addEventListener('click', add_email);
		friendsdrop.appendChild(a);
	}
	email_ids = new Object();
	email_ids[emails.getAttribute('name')] = 0;
	add_emails(email_ids);
}


// add expense
var form = document.querySelector('#exp form');
form.onsubmit = (evt) => {
	var sum = expense.value;
	for (var key in email_ids)
		sum -= email_ids[key];
	if (sum != 0) {
		evt.preventDefault();
		return;
	}
	var input = document.createElement('input');
	input.setAttribute('name', 'emails');
	input.setAttribute('value', JSON.stringify(email_ids));
	input.setAttribute('type', 'hidden');
	form.appendChild(input);
	form.submit();
}