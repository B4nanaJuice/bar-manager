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
    newTag = generateSearchTag(tagName);
    if (newTag === null) return;

    inputTags.parentElement.insertBefore(newTag, inputTags);
    inputTags.value = '';
}