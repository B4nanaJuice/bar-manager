inputTags = document.querySelector(".input-tags");

inputTags.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        triggerNewTag();
    }
})

function triggerNewTag() {
    newTagName = inputTags.value;
    addTag(newTagName);
}

function isEmptyOrSpaces(str) {
    return str === null || str.match(/^ *$/) !== null;
}

function addTag(tagName) {
    if (isEmptyOrSpaces(tagName)) return;

    newTag = document.createElement('span');
    newTag.innerHTML = `
        <p>${tagName}</p>
        <button onclick='this.parentElement.remove()'>X</button>
    `

    inputTags.parentElement.insertBefore(newTag, inputTags);
    inputTags.value = '';
}