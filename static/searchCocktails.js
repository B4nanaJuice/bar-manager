// Prefill search engine from url parameters
let params = new URLSearchParams(document.location.search);
let cocktail_type = params.get("cocktail_type") || "";
let ingredient_preferences = params.get("ingredient_preferences") || "";
let mocktail = (params.get("no_alcohol") || false) != false;
let cocktail_name = params.get("cocktail_name") || "";

window.onload = function() {
    if (cocktail_type != "") {
        document.querySelector(".cocktail_type").value = cocktail_type;
    }

    if (ingredient_preferences != "") {

        ingredient_preferences = ingredient_preferences.split(',');
        inputTags = document.querySelector(".input_tags");

        for (_ = 0; _ < ingredient_preferences.length; _++) {
            ingredient = ingredient_preferences[_];

            newTag = generateSearchTag(ingredient);

            if (newTag !== null ) {
                inputTags.parentElement.insertBefore(newTag, inputTags);
            }
        }
    }

    if (mocktail) {
        document.querySelector(".no_alcohol_option").checked = true;
    }

    if (cocktail_name) {
        document.querySelector(".cocktail_name").value = cocktail_name;
    }
}

function searchCocktails() {
    ingredientListDiv = document.querySelector(".ingredient_list");
    tagsSpan = [...ingredientListDiv.querySelectorAll(".search_tag")];
    ingredientList = tagsSpan.map(span => span.innerText);

    // Take the cocktail type
    cocktailTypeSelect = document.querySelector(".cocktail_type");
    cocktailType = cocktailTypeSelect.value || "";
    cocktailName = document.querySelector(".cocktail_name").value || "";

    // Send the request and refresh the page
    var url = new URL(window.location);
    if (cocktailType != "") { url.searchParams.set("cocktail_type", cocktailType); }
    else { url.searchParams.delete("cocktail_type"); }

    if (ingredientList.length > 0) { url.searchParams.set("ingredient_preferences", ingredientList.join(",")); }
    else { url.searchParams.delete("ingredient_preferences"); }

    if (document.querySelector(".no_alcohol_option").checked) { url.searchParams.set("no_alcohol", "true"); }
    else { url.searchParams.delete("no_alcohol"); }

    if (cocktailName != "") { url.searchParams.set("cocktail_name", cocktailName); }
    else { url.searchParams.delete("cocktail_name"); }

    window.location = url;
}