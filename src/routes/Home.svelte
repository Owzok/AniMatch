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
          <p class="lato-light">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Risus commodo viverra maecenas accumsan lacus vel facilisis.</p>
          <input type="text" class="lato-light" placeholder="Enter MyAnimeList Username">
      </div>
  </body>
</main>

<style>


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
  background-image: url('/images/asuka.png');
  animation: zoomAndFade1 50s infinite linear;
  opacity: 1;
}

.image2 {
  background-image: url('/images/rei.png');
  animation: zoomAndFade2 50s infinite linear;
}

.image3 {
  background-image: url('/images/city.png');
  animation: zoomAndFade3 50s infinite linear;
}

.image4 {
  background-image: url('/images/rin.png');
  animation: zoomAndFade4 50s infinite linear;
}

.image5 {
  background-image: url('/images/goku.jpeg');
  animation: zoomAndFade5 50s infinite linear;
}

.image6 {
  background-image: url('/images/chill.jpg');
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

.header {
  display: flex;
  align-items: flex-start; /* Align items to the top */
  justify-content: flex-start; /* Align content to the top */
  margin: 0;
  padding: 0;
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
}

.lato-match {
  margin-left: 20px; 
}

.white-line {
  border-top: 1px solid white;
  max-width: 250px;
  margin: 7px 0;
}

.content {
  text-align: left; /* Left-align the content below */
}

p {
  max-width: 500px;
  margin: 0 auto;
}

input[type="text"] {
  width: 300px;
  padding: 10px;
  margin: 20px 0;
  height: 25px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  background: rgba(0, 0, 0, 0.4); /* Black background with 40% opacity */
  border: 1px solid rgba(255, 255, 255, 0.7); /* White border with 70% opacity */
  margin-top: 40px;
  font-size: 20px;
}
</style>