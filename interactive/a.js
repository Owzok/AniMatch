// Fetch and parse the CSV file
let suggestions = [];
let animeData = {};
let scoreData = {};
let genresData = {};

// Read file and get suggestions 
// TODO: Take popularity into consideration
fetch('../apis/data/anime_with_synopsis.csv')
    .then(response => response.text())
    .then(data => {
        let lines = data.split('\n');
        lines.forEach(line => {
            let [id, title, score, genres, synopsis] = line.split(',');
            console.log(id);
            console.log(title);
            console.log(score);
            console.log(genres);
            console.log(synopsis);
            if (id && title) {
                suggestions.push(title.trim());
                animeData[title.trim()] = id.trim();
                scoreData[id.trim()] = score.trim();
                genresData[id.trim()] = genres.trim();
            }
        });
    })
    .catch(error => console.error('Error fetching the CSV file:', error));

// Getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");

const anime_info = document.querySelector(".info");
const animeImg = document.getElementById("anime-img");
const animeTitle = document.getElementById("anime-title");
const animeRating = document.getElementById("anime-rating");
const animeGenres = document.getElementById("anime-genres");

const selectedAnimeContainer = document.getElementById("selected-anime-container");

let webLink;
let selection = false;
let selectedAnimeTitle = "";
let selectedAnimeId = "";
let selectedRating = "";
let selectedAnimeScore = "0"
let selectedAnimeGenres = ""

let selectedAnimes = [];
let selectedRatings = [];
let animecount = 0;

const buttons = document.querySelectorAll(".btn");

for (let i = 0; i < buttons.length; i++) {
    let button = buttons[i];
    button.addEventListener("click", function() {
        buttons.forEach(function(item){
            item.classList.remove("selected");
        });
        button.classList.add("selected");
        selectedRating = button.textContent.toLowerCase(); // Update the selected rating
    });
}

function checkSelection(){
    if (selection) { anime_info.style.display = 'block'; } 
    else { anime_info.style.display = 'none'; }
}

checkSelection();

inputBox.onkeyup = (e) => {
    let userData = e.target.value;
    let emptyArray = [];
    if (userData) {
        emptyArray = suggestions.filter((data) => {
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data) => {
            return data = `<li>${data}</li>`;
        });
        searchWrapper.classList.add("active");
        showSuggestions(emptyArray);
        let allList = suggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            allList[i].setAttribute("onclick", "select(this)");
        }
    } else {
        searchWrapper.classList.remove("active");
    }
}

function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    selectedAnimeTitle = selectData; // Update the selected anime title
    selectedAnimeId = animeData[selectData]; // Update the selected anime ID
    selectedAnimeScore = scoreData[selectedAnimeId];
    selectedAnimeGenres = genresData[selectedAnimeId];
    animeImg.src = `../public/download/profiles/${selectedAnimeId}.jpg`;

    console.log(animeTitle);
    console.log(animeRating);
    console.log(animeGenres);

    // >>>>> Logic to update info panel too

    animeTitle.textContent = selectedAnimeTitle;
    animeRating.textContent = selectedAnimeScore;
    animeGenres.textContent = selectedAnimeGenres;

    searchWrapper.classList.remove("active");
    selection = true;

    const autocomBox = document.querySelector('.autocom-box');
    autocomBox.innerHTML = '';
    checkSelection();
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}

// Add event listener for the submit button
const submitButton = document.querySelector(".submit button");
submitButton.addEventListener("click", function() {
    if (selectedAnimeTitle && selectedAnimeId && selectedRating) {
        console.log(`Show Name: ${selectedAnimeTitle}, ID: ${selectedAnimeId}, Rating: ${selectedRating}`);
        addSelectedAnime(selectedAnimeTitle, selectedAnimeId, selectedRating);
        clearSelection();
        
        if (selectedAnimes.length >= 5) {
            collectAndSendData();
        } else {
            console.log("Remaining animes to generate recommendations:", 5 - selectedAnimes.length);
        }
    } else {
        console.log("Please select an anime and a rating.");
    }
});

function addSelectedAnime(title, id, rating) {
    const animeElement = document.createElement("div");
    animeElement.className = `selected-anime ${rating} selected`;
    animeElement.setAttribute("data-id", id); // Add data attribute for ID
    animeElement.innerHTML = `
        ${title}
        <span class="close-btn">&times;</span>
    `;
    selectedAnimeContainer.appendChild(animeElement);
    selectedAnimes.push(id)
    selectedRatings.push(rating);

    animeElement.querySelector(".close-btn").addEventListener("click", function() {
        selectedAnimeContainer.removeChild(animeElement);
        removeSelectedAnime(id);
    });
}

function removeSelectedAnime(id) {
    const index = selectedAnimes.indexOf(id);
    if (index !== -1) {
        selectedAnimes.splice(index, 1);
    }
}

function clearSelection() {
    inputBox.value = "";
    animeImg.src = "../public/download/profiles/1.jpg";
    buttons.forEach(button => button.classList.remove("clicked"));
    selectedAnimeTitle = "";
    selectedAnimeId = "";
    selectedRating = "";
    selection = false;
    checkSelection();
    buttons.forEach(function(item){
        item.classList.remove("selected");
    });
}

// Function to collect the selected anime data and send to the server
function collectAndSendData() {
    console.log("Calling model.");
    const anime_ids = selectedAnimes
    const ratings = selectedRatings.map(rating => {
        switch (rating) {
            case 'amazing': return 10;
            case 'good': return 7;
            case 'meh': return 5;
            case 'bad': return 3;
            default: return 0;
        }
    });

    console.log(anime_ids);
    console.log(ratings);

    fetch('http://127.0.0.1:5000/interec', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            anime_ids: anime_ids,
            ratings: ratings
        }),
    })
    .then(response => response.json())
    .then(data => {
        if ('results' in data) {
            const parsedResults = JSON.parse(data.results);
            console.log("<animatch>:", parsedResults);

            const top10Animes = parsedResults.slice(0, 10);
            const recommendationsDiv = document.querySelector('.recommendations');

            recommendationsDiv.innerHTML = ''; // Clear existing images
            console.log(top10Animes);

            top10Animes.forEach((anime, index) => {
                const imgElement = document.createElement('img');
                imgElement.src = `../public/download/profiles/${anime.anime_id}.jpg`;
                imgElement.alt = `Recommendation ${index + 1}`;
                recommendationsDiv.appendChild(imgElement);
            });

        }
    })
    .catch(error => {
        console.error('<animatch> Error:', error);
    });
}

function generateRandomId() {
    return Math.random().toString(36).substring(2, 10);
}
