document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed");

    // Setup for adding ingredients
    const addIngredientButton = document.getElementById('add-ingredient');
    const ingredientsList = document.getElementById('ingredients-list');

    if (addIngredientButton && ingredientsList) {
        console.log("Add Ingredient Button found");
        addIngredientButton.addEventListener('click', function () {
            console.log("Add Ingredient button clicked");
            const newIngredient = document.createElement('div');
            newIngredient.classList.add('ingredient-item', 'mb-2', 'd-flex');
            newIngredient.innerHTML = `
                <input type="text" name="ingredient_name[]" placeholder="Ingredient" required class="form-control w-25 me-2" />
                <input type="text" name="ingredient_quantity[]" placeholder="Quantity" required class="form-control w-25 me-2" />
                <button type="button" class="btn btn-danger remove-ingredient">Remove</button>
            `;
            ingredientsList.appendChild(newIngredient);
            console.log("New ingredient added:", newIngredient); // Debug log
        });

        ingredientsList.addEventListener('click', function (e) {
            if (e.target && e.target.classList.contains('remove-ingredient')) {
                e.target.parentElement.remove();
                console.log("Ingredient removed"); // Debug log
            }
        });
    } else {
        console.error("Add Ingredient Button or Ingredients List not found");
    }

    // Setup for adding instructions
    const addInstructionButton = document.getElementById('add-instruction');
    const instructionsList = document.getElementById('instructions-list');

    if (addInstructionButton && instructionsList) {
        console.log("Add Instruction Button found");
        addInstructionButton.addEventListener('click', function () {
            console.log("Add Instruction button clicked");
            const newInstruction = document.createElement('div');
            newInstruction.classList.add('instruction-item', 'mb-2', 'd-flex');
            newInstruction.innerHTML = `
                <textarea class="form-control me-2" name="instruction[]" placeholder="Step" required></textarea>
                <button type="button" class="btn btn-danger remove-instruction">Remove</button>
            `;
            instructionsList.appendChild(newInstruction);
            console.log("New instruction added:", newInstruction); // Debug log
        });

        instructionsList.addEventListener('click', function (e) {
            if (e.target && e.target.classList.contains('remove-instruction')) {
                e.target.parentElement.remove();
                console.log("Instruction removed"); // Debug log
            }
        });
    } else {
        console.error("Add Instruction Button or Instructions List not found");
    }

    // Setup for removing ingredients and instructions dynamically
    const removeIngredientButtons = document.querySelectorAll('.remove-ingredient');
    removeIngredientButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.target.closest('.ingredient-item').remove();
            console.log("Ingredient removed"); // Debug log
        });
    });

    const removeInstructionButtons = document.querySelectorAll('.remove-instruction');
    removeInstructionButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.target.closest('.instruction-item').remove();
            console.log("Instruction removed"); // Debug log
        });
    });

    // Form submission validation
    const form = document.querySelector('.recipeForm');
    if (form) {
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
    }

    function validateNotEmpty(input) {
        if (input.value.trim() === "") {
            input.classList.add("is-invalid"); // Add invalid class
            return false;
        } else {
            input.classList.remove("is-invalid"); // Remove invalid class
            return true;
        }
    }
});
