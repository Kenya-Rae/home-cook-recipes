const form = document.getElementById('form');
const usernameInput = document.getElementById('userInput');
const emailInput = document.getElementById('emailInput');
const passwordInput = document.getElementById('passwordInput');
const repeatPasswordInput = document.getElementById('repeatPasswordInput');
const errorMsg = document.getElementById('error-msg');

form.addEventListener('submit', (e) => {
    let errors = [];

    if (usernameInput) {
        // if first name input appears, sign up page is loaded
        errors = SignUpFormErrors(
            usernameInput.value,
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

function SignUpFormErrors(username, email, password, repeatPassword) {
    let errors = [];

    if (username === "" || username == null) {
        errors.push('First name Required');
        usernameInput.parentElement.classList.add('incorrect');
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

const allInputs = [usernameInput, emailInput, passwordInput, repeatPasswordInput].filter(input => input != null);

allInputs.forEach(input => {
    input.addEventListener('input', () => {
        if (input.parentElement.classList.contains('incorrect')) {
            input.parentElement.classList.remove('incorrect');
            errorMsg.innerHTML = '';
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Add more ingredients
    document.getElementById('add-ingredient').addEventListener('click', function () {
        const ingredientDiv = document.createElement('div');
        ingredientDiv.classList.add('ingredient-item', 'mb-2');
        ingredientDiv.innerHTML = `
            <input type="text" name="ingredient_name[]" placeholder="Ingredient" required class="form-control w-50" />
            <input type="text" name="ingredient_quantity[]" placeholder="Quantity" required class="form-control w-25" />
        `;
        document.getElementById('ingredients-list').appendChild(ingredientDiv);
    });

    // Add instructions
    document.getElementById('add-instruction').addEventListener('click', function () {
        const instructionTextarea = document.createElement('textarea');
        instructionTextarea.classList.add('form-control', 'mb-2');
        instructionTextarea.name = "instruction[]";
        instructionTextarea.placeholder = "Step " + (document.getElementById('instructions-list').children.length + 1);
        instructionTextarea.required = true;
        document.getElementById('instructions-list').appendChild(instructionTextarea);
    });
});
