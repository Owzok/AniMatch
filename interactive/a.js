// Fetch and parse the CSV file
let suggestions = [];
let animeData = {};
let scoreData = {};
let genresData = {};

let id_mapper = {};

// Read file and get suggestions 
// TODO: Take popularity into consideration
fetch('../apis/data/interactive.csv')
    .then(response => response.text()).then(data => {
        Papa.parse(data, {
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                results.data.forEach(row => {
                    let id = row.MAL_ID;
                    let title = row.Name;
                    let score = row.Score;
                    let genres = row.Genres;
                    let synopsis = row.sypnopsis;
                    let members = row.Members;
                    let type = row.Type;
                    let episodes = row.Episodes;
                    let studios = row.Studios;
                    console.log(id, title, score, genres, synopsis, members, type, episodes, studios);
                    if (id && title) {
                        // Hash table where key is the id and value is the title
                        id_mapper[id.trim()] = {
                            title: title.trim()
                        };
                        // Hash table where key is the title and value is everything
                        suggestions.push(title.trim());
                        animeData[title.trim()] = {
                            id: id.trim(),
                            score: score.trim(),
                            genres: genres.trim(),
                            synopsis: synopsis.trim(),
                            members: members.trim(),
                            type: type.trim(),
                            episodes: episodes.trim(),
                            studios: studios.trim()
                        };
                    }
                });
            },
            error: function(error) {
                console.error('Error parsing the CSV file:', error);
            }
        });
    })
    .catch(error => console.error('Error fetching the CSV file:', error));

// Getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const submitButton = document.querySelector(".submit button");
// HTML elemnts for information about the selected anime
const anime_info = document.querySelector(".container-info");
const animeImg = document.getElementById("anime-img");
const animeTitle = document.getElementById("anime-title");
const animeRating = document.getElementById("anime-rating");
const animeGenres = document.getElementById("anime-genres");
const animeMembers = document.getElementById("anime-members");
const animeType = document.getElementById("anime-type");
const animeEpisodes = document.getElementById("anime-episodes");
const animeStudios = document.getElementById("anime-studios");
const animeSynopsis = document.getElementById("anime-synopsis");
// Where the selected shows stack up
const selectedAnimeContainer = document.getElementById("selected-anime-container");
const animeContainerBackground = document.getElementById("anime-bg");
const instructionContainer = document.getElementById("instruction");

let selection = false;              // Hides / Shows the anime info panel
let selectedAnimeTitle = "";
let selectedAnimeId = "";
let selectedRating = "";
let selectedAnimeScore = "0"
let selectedAnimeGenres = ""
let selectedAnimeSynopsis = ""

let selectedAnimes = [];            // Contains the record of animes and their ratings
let selectedRatings = [];

// Rating buttons (amazing, good, meh, bad)
const buttons = document.querySelectorAll(".button");

// Foreach rating button, if clicked add .selected class and store the rating
for (let i = 0; i < buttons.length; i++) {
    let button = buttons[i];
    button.addEventListener("click", function() {
        buttons.forEach(function(item){ item.classList.remove("selected", "amazing", "good", "meh", "bad"); });
        button.classList.add("selected");
        selectedRating = button.textContent.toLowerCase().trim();
        applyRatingStyle(button, selectedRating);
    });
}

// Check if the anime info panel should be shown or hidden
function checkSelection(){
    if (selection) { anime_info.style.display = 'block'; } 
    else { anime_info.style.display = 'none'; }
}

checkSelection();

// === Search Bar ===
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

// Select anime from left container titles and recommendation images
function selectAnimeByClick(container) {
    if (event.target.classList.contains('remove-btn')) return;
    let animeTitle = container.querySelector('.anime-title').textContent;
    inputBox.value = animeTitle;
    select(container.querySelector('.anime-title'));
}

// Updates anime info panel by retrieving the title from the element
function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    selectedRating = "";
    animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%)';

    const selectedAnime = animeData[selectData]; 

    if (selectedAnime) {
        selectedAnimeTitle = selectData;
        selectedAnimeId = selectedAnime.id;
        selectedAnimeScore = selectedAnime.score;
        selectedAnimeGenres = selectedAnime.genres;
        selectedAnimeSynopsis = selectedAnime.synopsis;
        selectedAnimeMembers = formatScore(selectedAnime.members);
        selectedAnimeStudio = selectedAnime.studios;
        selectedAnimeType = selectedAnime.type;
        selectedAnimeEps = selectedAnime.episodes;

        animeImg.src = `../public/download/profiles/${selectedAnimeId}.jpg`;

        animeTitle.textContent = selectedAnimeTitle;
        animeRating.textContent = selectedAnimeScore;
        animeStudios.textContent = selectedAnimeStudio;
        animeMembers.textContent = selectedAnimeMembers;
        animeType.textContent = selectedAnimeType;
        animeEpisodes.textContent = selectedAnimeEps;

        animeGenres.innerHTML = '';
        selectedAnimeGenres.split(',').forEach(genre => {
            let span = document.createElement('span');
            span.className = 'genre';
            span.textContent = genre.trim();
            animeGenres.appendChild(span);
        });

        animeSynopsis.textContent = selectedAnimeSynopsis;

        searchWrapper.classList.remove("active");
        const autocomBox = document.querySelector('.autocom-box');
        autocomBox.innerHTML = '';
        selection = true;

        checkSelection();
    } else {
        console.error('Selected anime not found in data.');
    }
}

// Formats members from 300,000 to 300k and 2,5000,000 to 2.5 for example.
function formatScore(score) {
    const numericScore = parseInt(score, 10);
    if (numericScore >= 1000000) {
      return (numericScore / 1000000).toFixed(1) + 'M';
    } else if (numericScore >= 1000) {
      return (numericScore / 1000).toFixed(1) + 'k';
    } else {
      return numericScore.toString();
    }
}

// Shows animes that start with what is written on the searchbar
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

// Submit if rating, id and title, else console.log
submitButton.addEventListener("click", function() {
    if (selectedAnimeTitle && selectedAnimeId && selectedRating) 
    {           // console.log(`Show Name: ${selectedAnimeTitle}, ID: ${selectedAnimeId}, Rating: ${selectedRating}`);
        addSelectedAnime(selectedAnimeTitle, selectedAnimeId, selectedRating);
        clearSelection();
        
        if (selectedAnimes.length >= 5) { 
            collectAndSendData(); 
            instructionContainer.textContent = '';
        } else {
            instructionContainer.textContent = `Rate ${5 - selectedAnimes.length} more shows to get recommendations. The more you rate, the better the recommendations will be!`
        }
    } else {
        instructionContainer.textContent = "Please select an anime and a rating before submitting!";
    }
});

// Store Anime ID & Rating, create card for it too
function addSelectedAnime(animeTitle, id, rating) {
    const index = selectedAnimes.indexOf(id);
    if (index !== -1) {
        const container = selectedAnimeContainer.children[index];
        document.getElementById('selected-anime-container').removeChild(container);
        selectedAnimes.splice(index, 1);
        selectedRatings.splice(index, 1);
    }
    const container = document.createElement('div');
    container.className = 'selected-anime';
    container.classList.add(`rating-${rating}`);
    container.setAttribute('onclick', 'selectAnimeByClick(this)');

    const title = document.createElement('p');
    title.className = 'anime-title';
    title.textContent = animeTitle;

    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.textContent = 'X';
    removeBtn.addEventListener('click', () => {
        selectedAnimeContainer.removeChild(container);
        removeSelectedAnime(id);
    })

    container.appendChild(title);
    container.appendChild(removeBtn);

    selectedAnimeContainer.appendChild(container);
    selectedAnimes.push(id);
    selectedRatings.push(rating);

    document.getElementById('selected-anime-container').appendChild(container);
}

// Applying color style to the main panel
function applyRatingStyle(button, rating) {
    switch (rating) {
        case 'amazing':
            button.classList.add('amazing');
            animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #50bb2c 0, #50bb2c 1px, #131313 0, #131313 50%)';
            break;
        case 'good':
            button.classList.add('good');
            animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #7ea80b 0, #7ea80b 1px, #131313 0, #131313 50%)';            
            break;
        case 'meh':
            button.classList.add('meh');
            animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #c09426 0, #c09426 1px, #131313 0, #131313 50%)';
            break;
        case 'bad':
            button.classList.add('bad');
            animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #ff1867 0, #ff1867 1px, #131313 0, #131313 50%)';
            break;
        default:
            console.error('Invalid rating:', rating);
            animeContainerBackground.style.backgroundImage = 'repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%)';
    }
}

// Remove the anime and rating from data and call the model again
function removeSelectedAnime(id) {
    const index = selectedAnimes.indexOf(id);
    if (index !== -1) {
        selectedAnimes.splice(index, 1);
        selectedRatings.splice(index, 1);
        if (selectedAnimes.length > 4) {
            collectAndSendData(); 
        }
    }
}

// Clear the anime panel and local variables
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
    animeContainerBackground.style.backgroundImage = '';
}

// Call the model and retrieve the top 10 recommendations
function collectAndSendData() {
    console.log("Calling model.");
    const anime_ids = selectedAnimes;
    const ratings = selectedRatings.map(rating => {
        switch (rating) {
            case 'amazing': return 10;
            case 'good': return 7;
            case 'meh': return 5;
            case 'bad': return 3;
            default: return 0;
        }
    });

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
                const imgContainer = document.createElement('div');
                imgContainer.className = 'anime-recommendation'; // Optional, for styling

                const imgElement = document.createElement('img');
                imgElement.src = `../public/download/profiles/${anime.anime_id}.jpg`;
                imgElement.alt = `Recommendation ${index + 1}`;
                imgElement.setAttribute('data-anime-id', anime.anime_id);

                // Create and add the hidden title element
                const titleElement = document.createElement('p');
                titleElement.className = 'anime-title';

                console.log(anime.anime_id);
                console.log(id_mapper[anime.anime_id]);
                titleElement.textContent = id_mapper[anime.anime_id].title; // Ensure `anime.title` is available
                titleElement.style.display = 'none'; // Make the title invisible

                imgElement.setAttribute("onclick", "selectAnimeByClick(this)");

                imgContainer.appendChild(imgElement);
                imgElement.appendChild(titleElement);

                recommendationsDiv.appendChild(imgContainer);
            });
        }
    })
    .catch(error => {
        console.error('<animatch> Error:', error);
    });
}