inputTags = document.querySelector(".input-tags");
inputTags.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        tagName = inputTags.value;
        addTag(tagName);
    }
})

function addTag(tagName) {
    newTag = document.createElement('span');
    newTag.innerHTML = `
        <p>${tagName}</p>
        <button onclick='this.parentElement.remove()'>X</button>
    `

    inputTags.parentElement.insertBefore(newTag, inputTags);
    inputTags.value = '';
}