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
    if (ingredientList.length > 0) { url.searchParams.set("ingredient_preferences", ingredientList.join(",")); }

    window.location = url;
}