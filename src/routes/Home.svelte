<script>
	import { Link, Router, navigate } from 'svelte-routing'; // Import the navigate function
	import { inputValue } from '../store';

	let inputValueValue = '';

	$: disabled = inputValueValue === '';

	async function search() {
		try {
			const response = await fetch('http://127.0.0.1:5000/get_malid', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ title: inputValueValue }), // Replace with your API request payload
			});

			if (response.ok) {
				const data = await response.json();
        const id = data.id
				// console.log(data.id);

				if (inputValueValue !== '') {
					inputValue.set(id); // Update the store with the inputValue
					console.log(`Searching for ${id} of ${inputValueValue}`);
				}
				
				// Navigate to the "/about" route after logging the result
				navigate('/about');
			}
		} catch (error) {
			console.error('Error:', error);
		}
	}
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
              <input type="text" class="lato-light rounded-left" placeholder="Enter MyAnimeList Username" bind:value={inputValueValue}>
            </div>
            <button class="search-button" type="submit" style="height: 40px" {disabled} on:click={search}>
              <i class="fa fa-search"></i>
            </button>
          </div>
        </div>
  </body>
</main>

<style>

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

</style>