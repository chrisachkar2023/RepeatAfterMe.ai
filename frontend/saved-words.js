document.addEventListener('DOMContentLoaded', function () {
    const star = document.getElementById('saveStar');
    if (star) {
        star.addEventListener('click', async function () {
            const word = document.getElementById('word').innerText.trim();  // FIXED
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
});
