let modal = document.querySelector(".modal");
let modalContent = document.querySelector(".modal-content");

modalHeader = document.querySelector(".modal-header");
modalBody = document.querySelector(".modal-body");
modalFooter = document.querySelector(".modal-footer");

function openModal() {
    modal.classList.add("open");
}

function closeModal() {
    modal.classList.remove("open")
}

function createModal(title, body, footer) {
    modalHeader.innerText = title;
    document.querySelector(".modal-body").innerHTML = body;
    modalFooter.innerText = footer;

    openModal();
}

function createCocktailOrderModal(cocktailId, cocktailName, cocktailIngredients) {
    modalBody = `
        <div class="flex flex-column">
            <p>Ingrédients : ${cocktailIngredients.join(' - ')}</p>
            <div class="flex flex-row justify-around">
                <input type="text" name="name" id="name" class="col col-6" placeholder="Entre ton nom" required>
                <button onclick="orderCocktail(${cocktailId}, this.parentElement.querySelector('input').value)" class="button-outline button-primary col col-4">Commander</button>
            </div>
        </div>    
    `

    createModal(cocktailName, modalBody, "");
}

async function orderCocktail(cocktailId, name) {
    orderUrl = `${window.location.origin}/api/order-cocktail?cocktail-id=${cocktailId}&client-name=${name}`;
    try {
        let response = await fetch(orderUrl);
        if (!response.ok) {
            addNotification("Something went wrong...", "error", "Something went wrong while trying to fetch the URL.")
        }
        result = await response.json()

        addNotification({200: 'Success !', 400: 'Oops..'}[result.status], {200: 'success', 400: 'error'}[result.status], result.response);
        closeModal();
    } catch (error) {
        console.log(error)
    }
}