document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleFeedback');
    const feedbackBox = document.getElementById('feedbackBox');

    if (toggleBtn && feedbackBox) {
        toggleBtn.addEventListener('click', function () {
            const isHidden = feedbackBox.style.display === 'none';
            feedbackBox.style.display = isHidden ? 'block' : 'none';
            toggleBtn.textContent = isHidden ? 'Hide AI Feedback' : 'Show AI Feedback';
        });
    }
});