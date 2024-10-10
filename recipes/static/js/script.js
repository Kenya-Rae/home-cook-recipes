const form = document.getElementById('form');
const firstnameInput = document.getElementById('firstnameInput');
const emailInput = document.getElementById('emailInput');
const passwordInput = document.getElementById('passwordInput');
const repeatPasswordInput = document.getElementById('repeatPasswordInput');
const errorMsg = document.getElementById('error-msg');

form.addEventListener('submit', (e) => {
    let errors = [];

    if (firstnameInput) {
        // if first name input appears, sign up page is loaded
        errors = SignUpFormErrors(
            firstnameInput.value,
            emailInput.value,
            passwordInput.value,
            repeatPasswordInput.value)
    }
    else {
        // if first name input is not present, sign in page is loaded
        errors = SignInFormErrors(emailInput.value, passwordInput.value)
    }

    if (errors.length > 0) {
        // prevent submission
        e.preventDefault()
        errorMsg.innerText = errors.join(". \n")
    }
});

function SignUpFormErrors(firstname, email, password, repeatPassword) {
    let errors = [];

    if (firstname === "" || firstname == null) {
        errors.push('First name Required');
        firstnameInput.parentElement.classList.add('incorrect');
    }
    if (email === "" || email == null) {
        errors.push('Email Required');
        emailInput.parentElement.classList.add('incorrect');
    }
    if (password === "" || password == null) {
        errors.push('Password Required');
        passwordInput.parentElement.classList.add('incorrect');
    }
    if (password.length < 8) {
        errors.push('Password MUST be 8 characters long.');
        passwordInput.parentElement.classList.add('incorrect');
    }
    if (password !== repeatPassword) {
        errors.push('Repeated password dont match');
        passwordInput.parentElement.classList.add('incorrect');
        repeatPasswordInput.parentElement.classList.add('incorrect');
    }

    return errors;
}

function SignInFormErrors(email, password) {
    let errors = [];
    if (email === "" || email == null) {
        errors.push('Email Required');
        emailInput.parentElement.classList.add('incorrect');
    }
    if (password === "" || password == null) {
        errors.push('Password Required');
        passwordInput.parentElement.classList.add('incorrect');
    }
    return errors;
}

const allInputs = [firstnameInput, emailInput, passwordInput, repeatPasswordInput].filter(input => input != null);

allInputs.forEach(input => {
    input.addEventListener('input', () => {
        if (input.parentElement.classList.contains('incorrect')) {
            input.parentElement.classList.remove('incorrect');
            errorMsg.innerHTML = '';
        }
    });
});
