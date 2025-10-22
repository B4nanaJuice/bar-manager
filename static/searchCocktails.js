// Prefill search engine from url parameters
let params = new URLSearchParams(document.location.search);
let cocktail_type = params.get("cocktail_type") || "";
// let ingredient_preferences = params.get("ingredient_preferences") || "";
let mocktail = (params.get("no_alcohol") || false) != false;
let cocktail_name = params.get("cocktail_name") || "";

document.querySelector(".cocktail_type").value = cocktail_type;
document.querySelector(".no_alcohol_option").checked = mocktail;
document.querySelector(".cocktail_name").value = cocktail_name;

function searchCocktails() {
    // ingredientListDiv = document.querySelector(".ingredient_list");
    // tagsSpan = [...ingredientListDiv.querySelectorAll(".search_tag")];
    // ingredientList = tagsSpan.map(span => span.innerText);

    // Take the cocktail type
    cocktailTypeSelect = document.querySelector(".cocktail_type");
    cocktailType = cocktailTypeSelect.value || "";
    cocktailName = document.querySelector(".cocktail_name").value || "";

    // Send the request and refresh the page
    var url = new URL(window.location);
    if (cocktailType != "") { url.searchParams.set("cocktail_type", cocktailType); }
    else { url.searchParams.delete("cocktail_type"); }

    // if (ingredientList.length > 0) { url.searchParams.set("ingredient_preferences", ingredientList.join(",")); }
    // else { url.searchParams.delete("ingredient_preferences"); }

    if (document.querySelector(".no_alcohol_option").checked) { url.searchParams.set("no_alcohol", "true"); }
    else { url.searchParams.delete("no_alcohol"); }

    if (cocktailName != "") { url.searchParams.set("cocktail_name", cocktailName); }
    else { url.searchParams.delete("cocktail_name"); }

    url.searchParams.delete("page");

    window.location = url;
}