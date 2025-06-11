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
