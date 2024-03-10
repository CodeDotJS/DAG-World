document.addEventListener("DOMContentLoaded", function() {
    const images = [document.getElementById('image1'), document.getElementById('image2'), document.getElementById('image3'), document.getElementById('image4')];
    const questionElement = document.getElementById("question");
    const correctScoreElement = document.getElementById("correctScore");
    const wrongCountElement = document.getElementById("wrongCount");
    const resetScoreButton = document.getElementById("resetScore");
    const nextButton = document.getElementById("nextButton");
    const showStatus = document.getElementById("status");
    let correctScore = parseInt(localStorage.getItem('correctScore')) || 0;
    let wrongCount = parseInt(localStorage.getItem('wrongCount')) || 0;
    let winnerImageIndex;
    let answerSubmitted = false;

    function updateScoreboard() {
        correctScoreElement.textContent = correctScore;
        wrongCountElement.textContent = wrongCount;
    }

    function storeScore() {
        localStorage.setItem('correctScore', correctScore);
        localStorage.setItem('wrongCount', wrongCount);
    }

    function resetScore() {
        correctScore = 0;
        wrongCount = 0;
        updateScoreboard();
        storeScore();
    }

    resetScoreButton.addEventListener('click', resetScore);

    function fetchImages() {
        fetch("https://dagworld.vercel.app/artists/random")
            .then((response) => response.json())
            .then((data) => {
                const artistName = data.name;
                const winnerArtwork = data.artworks[Math.floor(Math.random() * data.artworks.length)].painting;

                const otherArtworks = [];
                fetch("https://dagworld.vercel.app/artists/random/3")
                    .then((response) => response.json())
                    .then((data) => {
                        data.forEach((artist) => {
                            const artwork = artist.artworks[Math.floor(Math.random() * artist.artworks.length)].painting;
                            otherArtworks.push(artwork);
                        });
                        displayImages(winnerArtwork, otherArtworks);
                    })
                    .catch((error) => console.error("Error fetching other images:", error));

                questionElement.textContent = `Which artwork is associated with  "${artistName}"?`;
            })
            .catch((error) => console.error("Error fetching winner image:", error));
    }

    function displayImages(winnerImage, otherImages) {
        const shuffledImages = shuffleArray([winnerImage, ...otherImages]);
        images.forEach((image, index) => {
            image.src = shuffledImages[index];
            image.style.border = 'none';
            image.addEventListener('click', function() {
                if (!answerSubmitted) {
                    handleImageClick(image, index);
                }
            });
            if (shuffledImages[index] === winnerImage) {
                winnerImageIndex = index; // Store index of correct image
            }
        });
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    function changeOpacity() {
        images.forEach((image, i) => {
            if (i !== winnerImageIndex) {
                image.style.opacity = 0.3;
            }
        });
        images[winnerImageIndex].style.border = '2px solid green';
    }

    function handleImageClick(clickedImage, index) {
        answerSubmitted = true; // Set answer submitted flag
        if (index === winnerImageIndex) {
            correctScore++;
            showStatus.textContent = "CORRECT!"
            changeOpacity();
        } else {
            wrongCount++;
            showStatus.textContent = "WRONG!"
            changeOpacity();
        }
        updateScoreboard();
        storeScore();
    }

    nextButton.addEventListener('click', function() {
        showStatus.textContent = "";
        answerSubmitted = false; // Reset answer submitted flag
        images.forEach((image) => {
            image.style.opacity = 1;
        });
        fetchImages();
    });

    updateScoreboard();
    fetchImages();
});
