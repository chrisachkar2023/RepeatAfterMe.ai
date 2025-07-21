document.addEventListener('DOMContentLoaded', function () {
    const star = document.getElementById('saveStar');
    if (star) {
        star.addEventListener('click', async function () {
            const word = document.getElementById('word').innerText.trim(); 
            try {
                const res = await fetch('/api/save-word', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ word })
                });
                if (res.ok) {
                    star.classList.toggle('fas');
                    star.classList.toggle('far');
                } else {
                    alert('Failed to save word');
                }
            } catch (err) {
                console.error('Error saving word:', err);
            }
        });
    }

    const savedWordsBtn = document.getElementById('savedWordsBtn');
    const savedSidebar = document.getElementById('savedWordsSidebar');
    const savedContent = document.getElementById('savedWordsContent');
    const closeSavedSidebar = document.getElementById('closeSavedSidebar');

    if (savedWordsBtn) {
        savedWordsBtn.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent navigation
            const isVisible = savedSidebar.style.display === 'block';
            savedSidebar.style.display = isVisible ? 'none' : 'block';

            if (!isVisible) {
                fetch('/saved')
                    .then(res => res.text())
                    .then(html => {
                        savedContent.innerHTML = html;
                    })
            }
        });
    }

    if (closeSavedSidebar) {
        closeSavedSidebar.addEventListener('click', function () {
            savedSidebar.style.display = 'none';
        });
    }
});