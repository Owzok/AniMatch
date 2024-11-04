<script>
    import { anime_links, anime_ids, all_data } from '../store'; // Import store
	import { Link, Router, navigate } from 'svelte-routing'; // Import the navigation

    import { onMount } from "svelte";
    import Papa from 'papaparse';

    let suggestions = [];
    let animeData = {};
    let id_mapper = {};
    
    let selectedAnimes = [];
    let selectedRatings = [];
    
    let inputBox;
    let inputValue = '';
    let searchActive = false;
    let selection = false;
    let selectedAnime = null;
    let genresList = null;
    let selectedRating = '';
    let instructionText = "Rate 5 more shows to get recommendations. The more you rate, the better the recommendations will be!";
    let recommendations = [];
    
    onMount(async () => {
        document.body.style.backgroundColor = 'black';
        const response = await fetch('/interactive.csv');
        const data = await response.text();


        inputBox = document.querySelector(".search-input input");
     
        Papa.parse(data, {
          header: true,
          skipEmptyLines: true,
          complete: function (results) {
            results.data.forEach((row) => {
              let id = row.MAL_ID;
              let title = row.Name.trim();
    
              if (id && title) {
                id_mapper[id.trim()] = { title };
                suggestions.push(title);
    
                animeData[title] = {
                  id: id.trim(),
                  title: title.trim(),
                  score: row.Score.trim(),
                  genres: row.Genres.trim(),
                  synopsis: row.sypnopsis.trim(),
                  members: row.Members.trim(),
                  type: row.Type.trim(),
                  episodes: row.Episodes.trim(),
                  studios: row.Studios.trim(),
                };
              }
            });
          },
          error: function (error) {
            console.error('Error parsing the CSV file:', error);
          },
        });
    });
    
        function handleInput(e) {
            inputValue = e.target.value;
            searchActive = inputValue.length > 0;
        }
    
        function selectSuggestion(suggestion) {
            selectedAnime = animeData[suggestion];
            genresList = selectedAnime.genres.split(',').map(genre => genre.trim());
            searchActive = false;
            if (selectedAnime) {
                selectedRating = '';  // Reset selected rating
            } else {
                console.error('Selected anime not found in data.');
            }
            selection = true;
        }
    
        function handleRatingClick(rating){
            selectedRating = rating.toLowerCase();
            applyRatingStyle(selectedRating);
        }
    
        function applyRating(rating) {
            selectedRating = rating;
            applyRatingStyle(rating);
        }
    
        function applyRatingStyle(rating) {
            let background = '';
    
            switch (rating) {
                case 'amazing':
                    background = 'repeating-linear-gradient(45deg, #50bb2c 0, #50bb2c 1px, #131313 0, #131313 50%)';
                    break;
                case 'good':
                    background = 'repeating-linear-gradient(45deg, #7ea80b 0, #7ea80b 1px, #131313 0, #131313 50%)';
                    break;
                case 'meh':
                    background = 'repeating-linear-gradient(45deg, #c09426 0, #c09426 1px, #131313 0, #131313 50%)';
                    break;
                case 'bad':
                    background = 'repeating-linear-gradient(45deg, #ff1867 0, #ff1867 1px, #131313 0, #131313 50%)';
                    break;
                default:
                    background = 'repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%)';
            }
            document.getElementById('anime-bg').style.backgroundImage = background;
        }
    
        function submitSelection() {
            if (selectedAnime && selectedRating) {
                addSelectedAnime(selectedAnime.title, selectedAnime.id, selectedRating);
                clearSelection();
                if (selectedAnimes.length >= 5) {
                    collectAndSendData();
                    instructionText = '';
                } else {
                    instructionText = `Rate ${5 - selectedAnimes.length} more shows to get recommendations.`;
                }
            } else {
                instructionText = "Please select an anime and a rating before submitting!";
            }
        }
    
        function select(title) {
            selectedAnime = animeData[title];
            inputBox.value = title;
            selectedRating = "";
            document.getElementById('anime-bg').style.backgroundImage = 'repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%)';
            selection = true;
        }
    
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
    
        function addSelectedAnime(animeTitle, id, rating) {
            const index = selectedAnimes.findIndex(anime => anime.id === id);
    
            if (index !== -1) {
                // Remove existing anime if already selected
                selectedAnimes = selectedAnimes.filter(anime => anime.id !== id);
                selectedRatings = selectedRatings.filter((_, i) => i !== index);
            } else {
                // Add new anime to the selection
                selectedAnimes = [
                    ...selectedAnimes,
                    { title: animeTitle, id, rating }
                ];
                selectedRatings = [...selectedRatings, rating];
            }
            console.log(selectedAnimes, selectedRatings);
        }
    
        // Function to remove a selected anime
        function removeSelectedAnime(id) {
            // Find the index of the anime to remove
            const index = selectedAnimes.findIndex(anime => anime.id === id);
    
            if (index !== -1) {
                // Remove the anime from selectedAnimes
                selectedAnimes.splice(index, 1);
    
                // Remove the corresponding rating from selectedRatings
                selectedRatings.splice(index, 1);
            }
        }
    
        function clearSelection() {
            inputValue = '';
            selectedAnime = null;
            selectedRating = '';
            selection = false;
            document.getElementById('anime-bg').style.backgroundImage = 'repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%)';
        }
    
    async function collectAndSendData() {
        try {
            console.log("Calling model.");
            const ratings = selectedRatings.map((rating) => {
            switch (rating) {
                case 'amazing': return 10;
                case 'good': return 7;
                case 'meh': return 4;
                case 'bad': return 1;
                default: return 0;
            }
            });
            
            const selectedAnimeIds = selectedAnimes.map(anime => anime.id);
        
            const response = await fetch('http://127.0.0.1:5000/interec', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                anime_ids: selectedAnimeIds,
                ratings: ratings,
            }),
            });
            if (!response.ok) {
            console.error('Network response was not ok:', response.statusText);
            return;
            }
        const data = await response.json();
        console.log("Response data received:", data);
        console.log("Response received:", response); // Log the entire response object

        if (data && data.results) {
            //const parsedResults = data.results; // Remove JSON.parse if data.results is already an object
            //console.log("<animatch>:", parsedResults);
            //const top10Animes = parsedResults.slice(0, 10);
            //console.log("<animatch> Top 10:", top10Animes);
            const parsedResults = JSON.parse(data.results);
            const restOfUrls = parsedResults.map(entry => entry.anime_image_url);
            const anime_IDS = parsedResults.map(entry => entry.anime_id);
            const for_filter = parsedResults.map(entry => entry.score);

            anime_ids.set(anime_IDS);
            anime_links.set(restOfUrls);
            all_data.set(for_filter);

            console.log("<animatch> Anime id:", anime_IDS);
            console.log("<animatch> Image urls:", restOfUrls);

            
        } else {
            console.error('Invalid response format or no results found.');
        }
        // Navigation
        navigate('/about');
    } catch (error) {
        console.error('<animatch> Error:', error);
    }
    }
    
    </script>

    <head>
        <meta charset="utf-8">
        <title>AniMatch Interactive Recommender</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
    </head>
    <body>
        <header style="font-size: 40px; color: white; font-weight: 100;">
            <b>AniMatch</b> Interactive Recommender
        </header>
        <p id="instruction" class="instruction">{instructionText}</p>
        <div class="container">
            <div class="container-right">
                <div class="b-container">
                    <a 
                        class="button {selectedRating === 'amazing' ? 'selected' : ''}" 
                        href="#" 
                        alt=""
                        style="--color: #50bb2c;" 
                        on:click={() => handleRatingClick('Amazing')}
                        on:keydown={(event) => handleRatingClick(event, 'Amazing')}
                    >Amazing</a>
            
                    <a 
                        class="button {selectedRating === 'good' ? 'selected' : ''}" 
                        href="#" 
                        style="--color:#7ea80b;" 
                        on:click={() => handleRatingClick('Good')}
                        on:keydown={(event) => handleRatingClick(event, 'Good')}
    
                    >Good</a>
            
                    <a 
                        class="button {selectedRating === 'meh' ? 'selected' : ''}" 
                        href="#" 
                        style="--color:#c09426;" 
                        on:click={() => handleRatingClick('Meh')}
                        on:keydown={(event) => handleRatingClick(event, 'Meh')}
    
                    >Meh</a>
            
                    <a 
                        class="button {selectedRating === 'bad' ? 'selected' : ''}" 
                        href="#" 
                        style="--color: #ff1867;" 
                        on:click={() => handleRatingClick('Bad')}
                        on:keydown={(event) => handleRatingClick(event, 'Bad')}
    
                    >Bad</a>
                </div>
    
                <div class="wrapper">
    
                    <div class="search-input">
                        <input type="text" bind:value={inputValue} on:input={handleInput} placeholder="Search for an anime..."/>
                        {#if searchActive}
                          <ul class="autocom-box">
                            {#each suggestions.filter(s => s.toLowerCase().startsWith(inputValue.toLowerCase())) as suggestion}
                              <li on:click={() => selectSuggestion(suggestion)}>{suggestion}</li>
                            {/each}
                          </ul>
                        {/if}
                    </div>  
    
                    <div class="container-info" id="anime-bg" style:display={selection ? 'block' : 'none'}>
                        {#if selectedAnime}
                            <div class="animu">
                                <div class="anime-img">
                                    <img id="anime-img" src={`./download/profiles/${selectedAnime.id}.jpg`} alt="Anime image"/>
                                </div>
                                
                                <div class="anime-info">
    
                                    <h1 id="anime-title">{selectedAnime.title}</h1>
                                    <ul class="metadata">
                                        <li><p>Score</p><b id="anime-rating">{selectedAnime.score}</b></li>
                                        <li><p>Members</p><b id="anime-members">{formatScore(selectedAnime.members)}</b></li>
                                        <li><p>Type</p><b id="anime-type">{selectedAnime.type}</b></li>
                                        <li><p>Episodes</p><b id="anime-episodes"></b>{selectedAnime.episodes}</li>
                                        <li><p>Studio</p><b id="anime-studios">{selectedAnime.studios}</b></li>
                                    </ul>
    
                                    <div class="desc-container">
                                        <p id="anime-synopsis">{selectedAnime.synopsis}</p>
                                    </div>
    
                                    <div class="genre-container">
                                        <p class="Genres" id="anime-genres">
                                            {#each genresList as genre}
                                                <span class="genre">{genre}</span>
                                            {/each}
                                        </p>
                                        
                                    </div>
                                    
                                </div>
    
                            </div>
                            <div class="submit"><button on:click={submitSelection}>Submit</button></div>
    
                        {/if}
                    </div>
            </div>
            </div>
            <div class="container-left">
    
                <p style="margin-left: 15px;">Selected Shows:</p>
                <div id="selected-anime-container" class="selected-anime-container">
                    {#each selectedAnimes as anime, index}
                        <div 
                            class="selected-anime rating-{anime.rating}" 
                            on:click={() => select(anime.title)}>
                            <!--  on:keydown={(event) => select(event, anime.title)}--> 
                            <p class="anime-title">{anime.title}</p>
                            <button 
                                class="remove-btn" 
                                on:click|stopPropagation={() => removeSelectedAnime(anime.id)}>
                                <!-- on:keydown={(event) => removeSelectedAnime(event, anime.id)} --> 
                                X
                            </button>
                        </div>
                    {/each}
                </div>
            </div>
    
        </div>
        
        <div class="recommendations">
            {#each recommendations as anime (anime.id)}
                <div class="anime-recommendation">
                <img 
                    src={`./download/profiles/${anime.id}.jpg`} 
                    alt={`Recommendation for ${anime.title}`} 
                    data-anime-id={anime.id}
                    on:click={() => select(anime.title)}/>
                    <!-- on:keydown={(event) => select(event, anime.id)} -->
                
                <p class="anime-title" style="display: none;">{anime.title}</p>
                </div>
            {/each}
        </div>
    
        <input type="hidden" id="user-id">
    </body>
    
    <style>
    /* === Font Imports === */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;300;400;500;600;700;800;900&display=swap');
    
    /* === Global Styles === */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }
    
    body {
        background: #0b0b0b; 
        color: #e0e0e0; 
        padding: 0 20px;
        overflow-y: hidden;
    }
    
    /* === Layout === */
    
    header {
        text-align: center;
        padding: 20px 0;
    }
    
    .instruction {
        color: #fff;
        text-align: center;
        margin-top: 20px;
    }
    
    .container {
        display: flex;
        justify-content: space-between;
        height: 470px;
    }
    
    .container-right {
        display: flex;
        flex-direction: row;
        width: 1050px;
        padding: 20px 0px 20px 0px;
    }
    
    .container-left{
        width: 39%;
        padding: 20px;
    }
    
    .recommendations {
        display: flex;
        flex-direction: row;
        background: #131313;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        margin-top: 20px;
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* === Container Left - Selected Shows === */
    
    .selected-anime-container {
        background: #2c2c2c;
        padding: 20px;
        border-radius: 10px;
        width: 100%;
        max-height: 450px;
        overflow-y: auto;
    }
    
    .selected-anime {
        display: flex;
        justify-content: space-between;
        padding: 5px;
        width: 95%;
        margin-bottom: 10px;
        margin-left: 15px;
        border-radius: 10px;
        color: white;
        transition: 0.3s;
    }
        .selected-anime:hover {
            transform: scale(1.1);
            text-shadow: white 2px 0 15px;
        }
        .selected-anime p {
            margin-left: 11px;
            font-size: 18px;
            letter-spacing: 2px;
        }
    
    .rating-amazing { background-color: #50bb2c; box-shadow: 0px 0px 15px #50bb2c; }
    .rating-good { background-color: #7ea80b; box-shadow: 0px 0px 15px #7ea80b; }    
    .rating-meh { background-color: #c09426; box-shadow: 0px 0px 15px #c09426; }    
    .rating-bad { background-color: #ff1867; box-shadow: 0px 0px 15px #ff1867; }
    
    .remove-btn {
        background-color: transparent;
        font-size: 16px;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
        .remove-btn:hover {
            background-color: #ffcccc;  /* Light red background on hover */
            color: darkred;
        }
    
    /* === Container Right - Anime Info === */
    
    /* - Buttons                            */
    
    .b-container{
        margin-top: 53px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 35px;
    }
    
    .button {
        position: relative;
        width: 150px;
        padding: 16px 30px;
        color: var(--color);
        border: 2px solid rgba(0, 0, 0, 0.5);
        border-radius: 4px;
        text-shadow: 0 0 15px var(--color);
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        transition: .5s;
        z-index: 1;
        text-align: center;
      }
      .button:hover {
        color: #fff;
        border: 2px solid rgba(0, 0, 0, 0);
        box-shadow: 0 0 0px var(--color);
      }
      .button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--color);
        z-index: -1;
        transform: scale(0);
        transition: 0.3s;
      }
      .button:hover::before {
        transform: scale(1);
        box-shadow: 0 0 10px var(--color),
          0 0 30px var(--color),
          0 0 60px var(--color);
      }
    
    /* - Anime Info Search Bar              */
    
    .wrapper {
        width: 800px;
        background: #131313;
        border-radius: 10px;
        z-index: 3;
    }
    .search-input {
        display: flex;
        position: relative;
        border-radius: 5px;
    }
        .search-input input {
            width: 100%;
            padding: 10px;
            letter-spacing: 1px;
            border: none;
            border-radius: 5px 0 0 5px; /* Border only for the top corners */
            background: #2c2c2c;
            color: #fff;
        }
        .search-input .autocom-box {
            max-height: 200px;
            overflow-y: auto;
            position: absolute;
            top: 100%;
            width: 100%;
            background: #2c2c2c;
            border-radius: 0 0 5px 5px;
            z-index: 99;
        }
        .search-input .autocom-box li{
            cursor: pointer;
            list-style: none;
            height: 50px;
            border-bottom: 1px solid gray;
            padding-top: 15px;
            padding-left: 15px;
            transition: .5s;
        }
        .search-input .autocom-box li:hover{
            background-color: rgba(255,255,255,0.2);
        }
    
    /* - Anime Info Data                    */
    .container-info {
        padding-top: 30px;
        background-size: 25px 25px;
        background-image: repeating-linear-gradient(45deg, #323232 0, #323232 1px, #131313 0, #131313 50%);
    }
    
    .animu {
        display: flex;
        margin-bottom: 20px;
    }
    
    .anime-img {
        margin-left: 30px;
        width: 25%;
    }
        .anime-img img {
            height: 290px;
            width: 205px;
            border: 2px solid #333;
            border-radius: 10px;
        }
        .anime-info{
            margin-left: 45px;
            padding-right: 30px;
        }
        .anime-info h1 {
            text-transform: uppercase;
            white-space: nowrap;
            max-width: 500px;
            overflow-x: auto;
            padding-left: 10px;
            background-color: #131313;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .anime-info ul { margin: 10px 0 10px 0; }
        .anime-info li {
            display: inline-block;
            font-size: 18px;
            margin-right: 10px;
        }
        .anime-info ul li p { font-size: 14px; }
    
    .metadata{
        display: flex;
    }
        .metadata li{
            padding-left: 10px;
            padding-right: 10px;
            white-space: nowrap;
            background-color: #131313;
            border: 1px solid rgba(255,255,255,0.3);
        }
    
    .submit button {
        width: 100%;
        height: 40px;
        background-color: #333;
        color: #fff;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        padding: 10px;
        transition: background-color 0.3s;
    }
        .submit button:hover {
            background-color: #515151;
        }
    
    .desc-container{
        height: 155px;
        width: 500px;
        overflow-y: auto;   
        padding: 10px;      
        background-color: #131313;  
        color: white;     
        border: 1px solid rgba(255,255,255,0.3);
        line-height: 1.5;
    }
        .desc-container p{
        font-weight: 100;
        font-family: 'LatoLight', sans-serif;
        opacity: 0.7;
        }
    
    .genre-container {
        font-size: 14px;
        margin-top: 10px;
        white-space: nowrap;
        overflow-x: auto;
        max-width: 500px;
        background-color: #131313;
    }
        .genre-container p span {
            margin-right: 5px;
            background-color: rgba(255,255,255,0.35);
            border-radius: 5px;
            padding: 5px 10px 5px 10px;
            font-weight: 500;
        }
    
    /* === Recommendations === */
    
    .recommendations img {
        width: 170px;
        margin: 10px;
        border-radius: 10px;
        transition: 0.3s;
    }
    
    .recommendations img:hover { transform: scale(1.2); box-shadow: 0px 0px 40px 10px black; }
    </style>