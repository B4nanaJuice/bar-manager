function resetFilters(button) {
    searchEngine = button.parentElement;

    // Remove tags from box
    searchEngine.querySelectorAll(".search_tag").forEach(tag => {
        tag.remove();        
    });

    // Remove the value of the select
    searchEngine.querySelectorAll("select").forEach(select => {
        select.value = "";
    });

    // Remove the value of inputs
    searchEngine.querySelectorAll("input[type=text]").forEach(input => {
        input.value = "";
    });

    // Uncheck all checkboxes
    searchEngine.querySelectorAll("input[type=checkbox]").forEach(input => {
        input.checked = false;
    });
}