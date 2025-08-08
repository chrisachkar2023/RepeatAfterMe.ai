// word history tab when signed in

document.addEventListener("DOMContentLoaded", function () {
    const wordHistoryBtn = document.getElementById('wordHistoryBtn');
    const sidebar = document.getElementById('wordHistorySidebar');
    const historyContent = document.getElementById('historyContent');
    const closeSidebar = document.getElementById('closeSidebar');

    if (wordHistoryBtn) {
        wordHistoryBtn.addEventListener('click', function (event) {
            event.preventDefault();
            const isVisible = sidebar.style.display === 'block';
            sidebar.style.display = isVisible ? 'none' : 'block';

            if (!isVisible) {
                fetch('/history')
                    .then(res => res.text())
                    .then(html => {
                        historyContent.innerHTML = html;
                    });
            }
        });
    }

    if (closeSidebar) {
        closeSidebar.addEventListener('click', function () {
            sidebar.style.display = 'none';
        });
    }
});