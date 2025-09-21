// Prefill search engine from url parameters
let params = new URLSearchParams(document.location.search);
let cocktail_type = params.get("cocktail_type") || "";
let ingredient_preferences = params.get("ingredient_preferences") || "";

if (cocktail_type != "") {
    document.querySelector(".cocktail_type").value = cocktail_type;
}

if (ingredient_preferences != "") {
    ingredient_preferences = ingredient_preferences.split(',');
    inputTags = document.querySelector(".input-tags");
    for (ingredient of ingredient_preferences) {
        newTag = document.createElement('span');
        newTag.innerHTML = `
            <p>${ingredient}</p>
            <button onclick='this.parentElement.remove()'>X</button>
        `

        inputTags.parentElement.insertBefore(newTag, inputTags);
    }
}

function searchCocktails() {
    ingredientListDiv = document.querySelector(".ingredient_list");
    tagsSpan = [...ingredientListDiv.querySelectorAll("span p")];
    ingredientList = tagsSpan.map(span => span.innerText);

    // Take the cocktail type
    cocktailTypeSelect = document.querySelector(".cocktail_type");
    cocktailType = cocktailTypeSelect.value || "";

    // Send the request and refresh the page
    var url = new URL(window.location);
    if (cocktailType != "") { url.searchParams.set("cocktail_type", cocktailType); }
    else { url.searchParams.delete("cocktail_type"); }
    if (ingredientList.length > 0) { url.searchParams.set("ingredient_preferences", ingredientList.join(",")); }
    else { url.searchParams.delete("ingredient_preferences"); }

    window.location = url;
}