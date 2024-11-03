document.addEventListener('DOMContentLoaded', function () {
    // Form elements
    const form = document.getElementById('form');
    const usernameInput = document.getElementById('userInput');
    const emailInput = document.getElementById('emailInput');
    const passwordInput = document.getElementById('passwordInput');
    const repeatPasswordInput = document.getElementById('repeatPasswordInput');
    const errorMsg = document.getElementById('error-msg');

    // Check if form exists to avoid TypeError
    if (form) {
        form.addEventListener('submit', (e) => {
            let errors = [];

            // Check if usernameInput exists (only for sign-up)
            if (usernameInput) {
                errors = SignUpFormErrors(
                    usernameInput.value,
                    emailInput.value,
                    passwordInput.value,
                    repeatPasswordInput.value
                );
            } else {
                // If usernameInput is not present, it's a sign-in page
                errors = SignInFormErrors(emailInput.value, passwordInput.value);
            }

            // Handle errors
            if (errors.length > 0) {
                e.preventDefault();
                errorMsg.innerText = errors.join(". \n");
            }
        });

        // Attach input event listeners to handle real-time validation
        const allInputs = [usernameInput, emailInput, passwordInput, repeatPasswordInput].filter(input => input != null);
        allInputs.forEach(input => {
            input.addEventListener('input', () => {
                // Perform real-time validation
                validateInput(input);
                if (input.parentElement.classList.contains('incorrect')) {
                    input.parentElement.classList.remove('incorrect');
                    errorMsg.innerHTML = '';
                }
            });
        });
    }

    // Ingredient and instruction functionality
    let ingredientCounter = 1; // Initialize counter for ingredients
    let instructionCounter = 1; // Initialize counter for instructions

    function setupIngredientButtons(addIngredientButton, ingredientsList) {
        addIngredientButton.addEventListener('click', function () {
            ingredientCounter++;
            let newIngredient = document.createElement('div');
            newIngredient.classList.add('ingredient-item', 'mb-2', 'd-flex');
            newIngredient.innerHTML = `
                <input type="text" name="ingredient_name[]" placeholder="Ingredient" required class="form-control w-25 me-2" />
                <input type="text" name="ingredient_quantity[]" placeholder="Quantity" required class="form-control w-25 me-2" />
                <button type="button" class="btn btn-danger remove-ingredient">Remove</button>
            `;
            ingredientsList.appendChild(newIngredient);
        });

        ingredientsList.addEventListener('click', function (e) {
            if (e.target && e.target.classList.contains('remove-ingredient')) {
                e.target.parentElement.remove();
            }
        });
    }

    function setupInstructionButtons(addInstructionButton, instructionsList) {
        addInstructionButton.addEventListener('click', function () {
            instructionCounter++;
            let newInstruction = document.createElement('div');
            newInstruction.classList.add('instruction-item', 'mb-2', 'd-flex');
            newInstruction.innerHTML = `
                <textarea class="form-control me-2" name="instruction[]" placeholder="Step" required></textarea>
                <button type="button" class="btn btn-danger remove-instruction">Remove</button>
            `;
            instructionsList.appendChild(newInstruction);
        });

        instructionsList.addEventListener('click', function (e) {
            if (e.target && e.target.classList.contains('remove-instruction')) {
                e.target.parentElement.remove();
            }
        });
    }

    // Setting up ingredient and instruction functionalities for add recipes
    const addIngredientButton = document.getElementById('add-ingredient');
    const ingredientsList = document.getElementById('ingredients-list');
    if (addIngredientButton && ingredientsList) {
        setupIngredientButtons(addIngredientButton, ingredientsList);
    }

    // Setting up ingredient and instruction functionalities for edit recipes
    const addInstructionButton = document.getElementById('add-instruction');
    const instructionsList = document.getElementById('instructions-list');
    if (addInstructionButton && instructionsList) {
        setupInstructionButtons(addInstructionButton, instructionsList);
    }

    // Validate the form before submission
    form.addEventListener('submit', function (e) {
        let valid = true;

        // Check all ingredient fields
        document.querySelectorAll("input[name='ingredient_name[]']").forEach(function (input) {
            if (!validateNotEmpty(input)) valid = false;
        });

        // Check all ingredient quantity fields
        document.querySelectorAll("input[name='ingredient_quantity[]']").forEach(function (input) {
            if (!validateNotEmpty(input)) valid = false;
        });

        // Check all instruction fields
        document.querySelectorAll("textarea[name='instruction[]']").forEach(function (input) {
            if (!validateNotEmpty(input)) valid = false;
        });

        if (!valid) {
            e.preventDefault(); // Prevent form submission
            alert("Please fill in all required fields."); // Alert user
        }
    });
});

// Form validation functions
function SignUpFormErrors(username, email, password, repeatPassword) {
    let errors = [];
    if (username === "" || username == null) {
        errors.push('First name Required');
    }
    if (email === "" || email == null) {
        errors.push('Email Required');
    }
    if (password === "" || password == null) {
        errors.push('Password Required');
    }
    if (password.length < 8) {
        errors.push('Password MUST be 8 characters long.');
    }
    if (password !== repeatPassword) {
        errors.push('Repeated password don’t match');
    }
    return errors;
}

function SignInFormErrors(email, password) {
    let errors = [];
    if (email === "" || email == null) {
        errors.push('Email Required');
    }
    if (password === "" || password == null) {
        errors.push('Password Required');
    }
    return errors;
}

// New validation helper functions
function validateNotEmpty(input) {
    if (input.value.trim() === "") {
        input.classList.add("is-invalid"); // Add invalid class
        return false;
    } else {
        input.classList.remove("is-invalid"); // Remove invalid class
        return true;
    }
}

function validateInput(input) {
    // Perform any specific validations here if needed
    validateNotEmpty(input);
}
