// update star icon based on star status
function updateStar(isSaved) {
    const star = document.getElementById('saveStar');
    if (!star) return;

    if (isSaved) {
        star.classList.add('fas');      // solid
        star.classList.remove('far');   // regular
    } else {
        star.classList.add('far');
        star.classList.remove('fas');
    }
}


// check with backend if current word is saved
function checkIfWordSaved(word) {
    fetch(`/api/is-word-saved?word=${encodeURIComponent(word)}`, {credentials: 'include'})
        .then(res => res.json())
        .then(data => {
            updateStar(data.saved);  // update star based on response
        })
        .catch(err => {
            console.error("Error checking if word is saved:", err);
        });
}


document.getElementById("difficulty").addEventListener("change", function () {
    const selectedDifficulty = this.value;

    fetch(`/api/word?difficulty=${selectedDifficulty}`)
        .then(response => response.text())
        .then(word => {
            document.getElementById("word").textContent = word;
            document.getElementById("hidden-word").value = word;
            checkIfWordSaved(word);
        })
        .catch(error => {
            console.error("Error fetching word:", error);
        });
});

document.getElementById("change-word-btn").addEventListener("click", () => {
    const selectedDifficulty = document.getElementById("difficulty").value;

    fetch(`/api/word?difficulty=${selectedDifficulty}`)
        .then(response => response.text())
        .then(word => {
            document.getElementById("word").textContent = word;
            document.getElementById("hidden-word").value = word;
            checkIfWordSaved(word);
        })
        .catch(error => {
            console.error("Error fetching word:", error);
        });
});

document.getElementById("upload-form").addEventListener("submit", function () {
    const selectedDifficulty = document.getElementById("difficulty").value;
    document.getElementById("hidden-difficulty").value = selectedDifficulty;
});

function refreshWord() {
    const diff = document.getElementById("difficulty").value;
    window.location.href = `/?difficulty=${diff}`;
}

window.refreshWord = refreshWord;
