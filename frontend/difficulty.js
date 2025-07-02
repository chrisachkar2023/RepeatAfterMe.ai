document.getElementById("difficulty").addEventListener("change", function () {
    const selectedDifficulty = this.value;

    fetch(`/api/word?difficulty=${selectedDifficulty}`)
        .then(response => response.text())
        .then(word => {
            document.getElementById("word").textContent = word;
            document.getElementById("hidden-word").value = word;
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
