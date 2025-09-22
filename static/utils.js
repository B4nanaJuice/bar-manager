function generateSearchTag(tagName) {
    // Sanitize the tag name
    if (tagName.match(/^[a-zA-Z0-9 '_"]*$/) === null) return null;
    if (tagName === null || tagName.match(/^ *$/) !== null) return null;

    // Create the tag 
    searchTag = document.createElement('button');
    searchTag.innerText = tagName;
    searchTag.addEventListener('click', function() {
        this.remove();
    });
    searchTag.classList.add("search_tag");

    // Return the new tag
    return searchTag;
}