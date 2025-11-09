let modal = document.querySelector(".modal");
let modalContent = document.querySelector(".modal-content");

let modalHeader = document.querySelector(".modal-header");
let modalBody = document.querySelector(".modal-body");
let modalFooter = document.querySelector(".modal-footer");

function openModal() {
    modal.classList.add("open");
}

function closeModal() {
    modal.classList.remove("open")
}

function createModal(title, body, footer) {
    modalHeader.innerText = title;
    modalBody.innerText = body;
    modalFooter.innerText = footer;

    openModal();
}