// select difficulty
document.getElementById("difficulty").addEventListener("change", function () {
    const selectedDifficulty = this.value;

    fetch(`/api/word?difficulty=${selectedDifficulty}`)  // pass selected difficulty
        .then(response => response.text())  // receive plain text (the word)
        .then(word => {
            document.getElementById("word").textContent = word;      // update displayed word
            document.getElementById("hidden-word").value = word;     // update hidden input value
        })
        .catch(error => {
            console.error("Error fetching word:", error);
        });
});


// change word button
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