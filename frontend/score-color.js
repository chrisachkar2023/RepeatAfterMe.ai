// changes percentage color color based on feedback text

window.addEventListener('DOMContentLoaded', () => {
  const feedbackEl = document.getElementById('feedback-text');
  const scoreEl = document.getElementById('score-text');
  
  if (!feedbackEl || !scoreEl) return; // safety check

  const feedback = feedbackEl.textContent.toLowerCase();

  if (feedback.includes('perfect')) {
    scoreEl.style.color = '#4caf50'; // bright green
  } 
  else if (feedback.includes('good')) {
    scoreEl.style.color = '#8bc34a'; // lighter green
  } 
  else if (feedback.includes('okay')) {
    scoreEl.style.color = '#ff9800'; // orange
  } 
  else {
    scoreEl.style.color = '#b41010ff'; // red
  }
});
