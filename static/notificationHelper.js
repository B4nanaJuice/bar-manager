function addNotification(title, type, content) {
    let notifications = document.querySelector('.notifications');
    notifications.innerHTML += `
        <div class="notification ${type}">
            <span class="close" onclick="this.parentElement.remove()">&times;</span>
            <h3>${title}</h3>
            <p>${content}</p>
        </div>
    `;
}