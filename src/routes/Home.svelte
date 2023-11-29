<script>
	import { Link, Router, navigate } from 'svelte-routing'; // Import the navigation
	import { anime_links, anime_ids, all_data } from '../store'; // Import store
  import { onMount } from 'svelte'; // Import void start
  // Local variables
	let inputValueValue = '';
  let selectedModel = 'model1';
  let overlay = null;
  // Reactive variable, whenever inputValueValue changes, it also tries to.
  // $: is the reactive shorthand syntax of Svelte
	$: disabled = inputValueValue === '';
  // Select which model to use, called inline by the div's onclick function
  function selectModel(modelId) {
    selectedModel = modelId;
    console.log('<animatch> Selected model:', modelId);
  }
  // Should be used when content-based is selected (model2)
	async function anime_search() {
		try {
      showOverlay(`Getting recommendations for ${ inputValueValue }`)
      // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
			const response = await fetch('http://127.0.0.1:5000/anirec', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ title: inputValueValue }),
			});
      // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
			if (response.ok) {
				const json = await response.json();
        if ('results' in json){
          const parsedResults = JSON.parse(json.results);
          const restOfUrls = parsedResults.map(entry => entry.anime_image_url);
          const anime_IDS = parsedResults.map(entry => entry.anime_id);

          anime_links.set(restOfUrls);
          anime_ids.set(anime_IDS);

          console.log("<animatch> Anime id:", anime_IDS);
          console.log("<animatch> Image urls:", restOfUrls);
        }
        // Navigation
        navigate('/about');
			}
		} catch (error) {
			console.error('<animatch> Error:', error);
		}
	}

  // Should be used when collaborative-filtering is selected or by default (model1)
  async function getrec(route) {
    try {
      showOverlay(`Searching user ${ inputValueValue }`)
      // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
      const response = await fetch(`http://127.0.0.1:5000/${ route }`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: inputValueValue }),
      });
      // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
      if(response.ok) {
        const json = await response.json();
        if ('results' in json) {
          const parsedResults = JSON.parse(json.results);
          const firstAnimeId = parsedResults[0].anime_id;
          const restOfUrls = parsedResults.map(entry => entry.anime_image_url);
          const for_filter = parsedResults.map(entry => entry.score);

          // firstAnimeId <<store>>: ID of the best recommendation to then get its data
          // restOfUrls <<store>>: image links of the other 9 recommendations to show
          anime_ids.set(parsedResults.map(entry => entry.anime_id));
          anime_links.set(restOfUrls);
          all_data.set(for_filter);
          //console.log("<animatch> First anime id:", firstAnimeId);
          //console.log("<animatch> Rest of the anime image urls:", restOfUrls);
          // Navigation
          navigate('/about');
        }
      }
    } catch (error) {
      console.error('<animatch> Error', error)
    }
  }

  function findMethod(){
    if(selectedModel === "model2"){
      anime_search();
    } else if(selectedModel === "model1"){
      searchMalUser("recommend");
    } else {
      searchMalUser("recommendae");
    }
  }

  // Scrap user data from MAL
  async function searchMalUser(route) {
    // Checks first if the user data have'been already scrapped
    const filePath = `./users/${inputValueValue}.csv`;
    try {
      const response = await fetch(filePath);
      const dataExists = response.ok;
      if (dataExists){
        console.log("<animatch> File exists: good");  
        // If exists executes
        // await its necessary since collab has some fetch functions
        await getrec(route);
        //
      } else {
        showOverlay(`Retrieving data from ${ inputValueValue }`)
        // Scrap
        console.log(`Searching for user ${inputValueValue}`)
        // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        const response = await fetch('http://127.0.0.1:5000/scrap_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username: inputValueValue }),
        });
        // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        if (response.ok) {
          console.log('<animatch> User scrapped successfully');
          // Execute
          await getrec(route);
          //
        } else {
          console.error(`<animatch> Error sending request: ${response.statusText}`);
        }
      }
    } catch (error) {
      console.error('<animatch> Error:', error);
    }
  }

  function showOverlay(loadingText) {
    overlay.style.display = 'flex';
    overlay.querySelector('.loading-text').textContent = loadingText;
  }

  onMount(() => {
    document.body.style.overflowY = 'hidden';
    overlay = document.querySelector('.overlay');
    return () => {
      document.body.style.overflowY = 'auto';
    };
  });
</script>

<Router>
  <nav class="navbar">
    <div class="navbar-links">
        <Link to="/"><p class=logo>AniMatch</p></Link>
        <Link to="about"><p class="navbar-link">About</p></Link>
        <Link to="about"><p class="navbar-link">Credits</p></Link>
        <Link to="about"><p class="navbar-link">FAQ</p></Link>
        <p class="navbar-link inactive">Stats</p>
    </div>
</nav>
</Router>

<main>
  <div class="overlay">
    <div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
    <p class="loading-text">Scrapping User</p>
  </div>
  <div class="background-image image1"></div>
  <div class="background-image image2"></div>
  <div class="background-image image3"></div>
  <div class="background-image image4"></div>
  <div class="background-image image5"></div>
  <div class="background-image image6"></div>
  <body>
      <div class="container">
          <h1 class="lato-bold">ANIME</h1>
          <h1 class="lato">MATCH</h1>
          <hr class="white-line">
          <p class="lato-light">Discover personalized anime recommendations tailored to your preferences through your MAL profile or manually. Let us be your guide to a world of captivating new anime experiences.</p>
          <div class="input-wrapper">
            <div class="input-container">
              <input type="text" class="lato-light rounded-left" placeholder={selectedModel === 'model2' ? 'Enter Anime Name' : 'Enter MyAnimeList Username'} bind:value={inputValueValue}>
            </div>            
            <button class="search-button" type="submit" style="height: 40px" {disabled} on:click={findMethod}>
              <i class="fa fa-search"></i>
            </button>
          </div>
          <div class="options">
            <div id="model1" 
            class="item late-light"
            class:selected={selectedModel === 'model1'}
            on:click={() => selectModel('model1')}
            on:keydown={(event) => {
              if (event.key === 'Enter' || event.key === 'Space') {
                selectModel('model1');
              }
            }}>Collab</div>
            <div id="model2" class="item late-light"
            class:selected={selectedModel === 'model2'}
            on:click={() => selectModel('model2')}
            on:keydown={(event) => {
              if (event.key === 'Enter' || event.key === 'Space') {
                selectModel('model2');
              }
            }}>Content</div>
            <div id="model3" class="item late-light"
            class:selected={selectedModel === 'model3'}
            on:click={() => selectModel('model3')}
            on:keydown={(event) => {
              if (event.key === 'Enter' || event.key === 'Space') {
                selectModel('model3');
              }
            }}>Collab V2</div>
            <div id="model4" class="item late-light"
            class:selected={selectedModel === 'model4'}
            on:click={() => selectModel('model4')}
            on:keydown={(event) => {
              if (event.key === 'Enter' || event.key === 'Space') {
                selectModel('model4');
              }
            }}>Hybrid</div>
            <div id="model5" class="item late-light"
            class:selected={selectedModel === 'model5'}
            on:click={() => selectModel('model5')}
            on:keydown={(event) => {
              if (event.key === 'Enter' || event.key === 'Space') {
                selectModel('model5');
              }
            }}>Network</div>
          </div>
      </div>
  </body>
</main>

<style>
.options{
  width: 450px;
  display: flex;
  height: 45px;
  background-color: rgba(0,0,0,0.4);
  border: 1px solid rgba(255,255,255, 0.7);
  border-radius: 5px;
  margin-top: 10px;
  vertical-align: baseline;
}

.item{
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-left: 1px solid rgba(255, 255, 255, 0.2);
}
.item:hover {
  background-color: rgba(0, 128, 0, 0.4);
}

.selected {
  background-color: green; /* Add the green background for the selected model */
}
.selected:hover {
  background-color: green; /* Add the green background for the selected model */
}

nav{
  position: absolute;
  z-index: 5;
  font-family: 'LatoLight', sans-serif;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
  padding: 10px;
}
  
.navbar-links {
  text-decoration: none;
  flex: 2;
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}
  
.navbar-link {
  color: #fff;
  font-size: 12px;
  margin: 0 60px;
}

.inactive{
  color: grey;
}
  
.logo {
  width: 30px;
  height: 30px;
  margin: 0 145px;
  color: white;
}

body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-size: cover;
    height: 100vh;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    text-decoration: none;
}

main {
    position: relative;
    padding: 0px;
    margin: 0;
    padding: 0;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  animation-duration: 15s;
  animation-timing-function: ease;
  background-size: cover;
  opacity: 0;
  animation-iteration-count: infinite;
}

.image1 {
  background-image: url('/images/chain.png');
  animation: zoomAndFade1 50s infinite linear;
  opacity: 1;
}

.image2 {
  background-image: url('/images/gilga.jpg');
  animation: zoomAndFade2 50s infinite linear;
}

.image3 {
  background-image: url('/images/fgo.jpg');
  animation: zoomAndFade3 50s infinite linear;
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
}

.image4 {
  background-image: url('/images/chill.jpg');
  animation: zoomAndFade4 50s infinite linear;
}

.image5 {
  background-image: url('/images/soldier.png');
  animation: zoomAndFade5 50s infinite linear;
}

.image6 {
  background-image: url('/images/city.png');
  animation: zoomAndFade6 50s infinite linear;
}

@keyframes zoomAndFade1 {
  0% {
      transform: scale(1.2);
  }
  12%{
      opacity: 1;
  }
  16% {
      transform: scale(1);
  }
  96%{
      transform: scale(1.22);
      opacity: 0;
  }
  100%{
      transform: scale(1.2);
      opacity: 1;
  }
}

@keyframes zoomAndFade2 {
  0%, 12%{
      opacity: 0;
      transform: scale(1.2);
  }
  16%{
      opacity: 1;
  }
  28%{
      opacity: 1;
  }
  32%{
      transform: scale(1);
      opacity: 0;
  }
  100%{
      opacity: 0;
  }
}

@keyframes zoomAndFade3 {
  0%, 28%{
      opacity: 0;
      transform: scale(1.2);
  }
  32%{
      opacity: 1;
  }
  44%{
      opacity: 1;
  }
  48%{
      transform: scale(1);
      opacity: 0;
  }
  100%{
      opacity: 0;
  }
}

@keyframes zoomAndFade4 {
  0%, 44%{
      opacity: 0;
      transform: scale(1.2);
  }
  48%{
      opacity: 1;
  }
  60%{
      opacity: 1;
  }
  64%{
      transform: scale(1);
      opacity: 0;
  }
  100%{
      opacity: 0;
  }
}

@keyframes zoomAndFade5 {
  0%, 60%{
      opacity: 0;
      transform: scale(1.2);
  }
  64%{
      opacity: 1;
  }
  76%{
      opacity: 1;
  }
  80%{
      transform: scale(1);
      opacity: 0;
  }
  100%{
      opacity: 0;
  }
}

@keyframes zoomAndFade6 {
  0%, 76%{
      opacity: 0;
      transform: scale(1.2);
  }
  80%{
      opacity: 1;
  }
  96%{
      opacity: 1;
  }
  100%{
      transform: scale(1);
      opacity: 0;
  }
}

@font-face {
  font-family: 'Lato';
  src: url('/fonts/Lato-Black.ttf') format('truetype');
}

@font-face {
  font-family: 'LatoBold';
  src: url('/fonts/Lato-Bold.ttf') format('truetype');
}

@font-face {
  font-family: 'LatoLight';
  src: url('/fonts/Lato-Light.ttf') format('truetype');
}

body::before {
  content: "";
  background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6685267857142857) 25%, rgba(0,0,0,0) 50%);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.container {
  position: relative;
  z-index: 2;
  background: transparent;
  padding: 20px;
  text-align: left; /* Left-align all content */
  border-radius: 10px;
  color: white;
  margin-left: 130px; /* Add a left margin of 300px */
  margin-top: 100px;
}

.lato {
  font-family: 'Lato', sans-serif;
  font-size: 4rem;
  margin: 0;
}

.lato-bold {
  font-family: 'LatoBold', sans-serif;
  font-size: 4rem;
  margin: 0;
}

.lato-light {
  font-family: 'LatoLight', sans-serif;
  color: white;
}

.white-line {
  border-top: 1px solid white;
  max-width: 250px;
  margin: 7px 0;
}

p {
  max-width: 500px;
  margin: 0 auto;
}

input[type="text"] {
  flex: 1;
  width: calc(100% - 45px);
  padding: 10px;
  margin: 20px 0;
  border: none;
  height: 100%;
  border-radius: 5px 5px 0 0 0;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.7);
  font-size: 20px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  height: 50px; 
  margin-top: 30px;
}

.input-container {
  flex: 1;
  display: flex;
}

.search-button {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.7);
  height: 93%;
  width: 50px;
  margin-right: 6px;
  border-radius: 0 10px 10px 0;
  cursor: pointer;
  outline: none;
}

.search-button:not([disabled]){
  background: rgba(255, 255, 255, 0.5);
}

.search-button:hover:not([disabled]) {
  font-size: 1.25rem;
  background: rgb(255, 255, 255, 0.8);
  color: white; 
}

.search-button i {
  color: white; 
  -webkit-transition: font-size .2s;
  -moz-transition: font-size .2s;
  -o-transition: font-size .2s;
  transition: font-size .2s;
}

.search-button:hover[disabled] {
  font-size: 1;
  background: rgba(0, 0, 0, 0.4); 
  border: 1px solid rgba(255, 255, 255, 0.7);
}

.overlay{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Adjust the last value for transparency */
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 5;
  display: none;
}

.overlay p{
  color: white;
  font-size: 20px;
  font-family: 'LatoLight', sans-serif;
  animation: lds-spinner 1.5s alternate ease-in infinite;
}

.lds-spinner {
  color: official;
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}
.lds-spinner div {
  transform-origin: 40px 40px;
  animation: lds-spinner 1.2s linear infinite;
}
.lds-spinner div:after {
  content: " ";
  display: block;
  position: absolute;
  top: 3px;
  left: 37px;
  width: 6px;
  height: 18px;
  border-radius: 20%;
  background: #fff;
}
.lds-spinner div:nth-child(1) {
  transform: rotate(0deg);
  animation-delay: -1.1s;
}
.lds-spinner div:nth-child(2) {
  transform: rotate(30deg);
  animation-delay: -1s;
}
.lds-spinner div:nth-child(3) {
  transform: rotate(60deg);
  animation-delay: -0.9s;
}
.lds-spinner div:nth-child(4) {
  transform: rotate(90deg);
  animation-delay: -0.8s;
}
.lds-spinner div:nth-child(5) {
  transform: rotate(120deg);
  animation-delay: -0.7s;
}
.lds-spinner div:nth-child(6) {
  transform: rotate(150deg);
  animation-delay: -0.6s;
}
.lds-spinner div:nth-child(7) {
  transform: rotate(180deg);
  animation-delay: -0.5s;
}
.lds-spinner div:nth-child(8) {
  transform: rotate(210deg);
  animation-delay: -0.4s;
}
.lds-spinner div:nth-child(9) {
  transform: rotate(240deg);
  animation-delay: -0.3s;
}
.lds-spinner div:nth-child(10) {
  transform: rotate(270deg);
  animation-delay: -0.2s;
}
.lds-spinner div:nth-child(11) {
  transform: rotate(300deg);
  animation-delay: -0.1s;
}
.lds-spinner div:nth-child(12) {
  transform: rotate(330deg);
  animation-delay: 0s;
}
@keyframes lds-spinner {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
