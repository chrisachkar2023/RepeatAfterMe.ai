// dropdown menu in navbar

const userDropdown = document.getElementById('userDropdown');
const dropdownMenu = document.getElementById('dropdownMenu');

if (userDropdown && dropdownMenu) {
    userDropdown.addEventListener('click', function(event) {
        event.stopPropagation(); 
        dropdownMenu.classList.toggle('show');
    });

    window.addEventListener('click', function() {
        dropdownMenu.classList.remove('show');
    });
}