function searchCocktails() {
    ingredientListDiv = document.querySelector(".ingredient_list");
    tagsSpan = [...ingredientListDiv.querySelectorAll("span p")];
    ingredientList = tagsSpan.map(span => span.innerText);

    // Take the cocktail type

    // Send the request and refresh the page
}