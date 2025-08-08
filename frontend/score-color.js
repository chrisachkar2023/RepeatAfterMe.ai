// changes percentage color color based on feedback text

window.addEventListener('DOMContentLoaded', () => {
  const feedbackEl = document.getElementById('feedback-text');
  const scoreEl = document.getElementById('score-text');
  
  if (!feedbackEl || !scoreEl) return;

  const feedback = feedbackEl.textContent.toLowerCase();

  if (feedback.includes('perfect')) {
    scoreEl.style.color = '#4caf50';
  } 
  else if (feedback.includes('good')) {
    scoreEl.style.color = '#8bc34a';
  } 
  else if (feedback.includes('okay')) {
    scoreEl.style.color = '#ff9800';
  } 
  else {
    scoreEl.style.color = '#b41010ff';
  }
});
