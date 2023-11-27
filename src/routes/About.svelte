<script>
  import { anime_links, anime_ids } from '../store';

  let imageExists = false;
  let imageSrc = null;
  let mal_images = [];
  let mal_ids = [];

  // Sliders Set 1
  let fromSlider1;
  let toSlider1;
  let fromInput1;
  let toInput1;
  let from_val1 = 1;
  let to_val1 = 100;

  // Sliders Set 2
  let fromSlider2;
  let toSlider2;
  let fromInput2;
  let toInput2;
  let from_val2 = 1;
  let to_val2 = 10;

  // Sliders Set 3
  let fromSlider3;
  let toSlider3;
  let fromInput3;
  let toInput3;
  let from_val3 = 1970;
  let to_val3 = 2023;

  const unsubscribe2 = anime_links.subscribe(value => {
    mal_images = value
  });

  const sus3 = anime_ids.subscribe(value => {
    mal_ids = value
  })

  function zipArrays(arr1, arr2) {
    return arr1.map((url, index) => ({ url, id: arr2[index] }));
  }

  let mal_data = zipArrays(mal_images, mal_ids);

  function handleClick(id) {
    current_id = id;
    change_banner();
  }
  
  function handleKeyDown(event, id) {
    if (event.key === 'Enter' || event.key === ' ') {
      handleClick(id);
    }
  }

  let current_id = mal_ids.slice(0, 1)[0];

  let title = "";
  let episodes = "";
  let type = "";
  let premiere = "";
  let studio = "";
  let rating = "";
  let desc = "";

  async function updateImage() {
  try {
    const response = await fetch(`/download/${current_id}.jpg`);
    imageExists = response.ok;

    if (imageExists) {
      imageSrc = `/download/${current_id}.jpg`;
    } else {
      generateImage();
    }
  } catch (error) {
      console.error('Error:', error);
    }
  }

  async function updateInfo() {
  try {

    const response = await fetch('http://127.0.0.1:5000/get_info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: current_id }),
    });

    if (response.ok) {
      const data = await response.json();
      title = data.Name;
      episodes = data.Episodes;
      premiere = data.Premiered;
      studio = data.Studios;
      type = data.Type;
      desc = data.synopsis;
      rating = data.Rating;
    } else {
      console.error('Failed to fetch data');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function change_banner(){
  updateInfo();
  updateImage();
}

async function generateImage() {
  const api_url = 'http://127.0.0.1:5000/scrape_image';

  try {
    const response = await fetch(`/download/${current_id}.jpg`);
    imageExists = response.ok;

    if (imageExists) {
      imageSrc = `/download/${current_id}.jpg`;
    } else {
      const response = await fetch(api_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: current_id }),
      });

      if (response.ok) {
        console.log("Answered!");
        const responseData = await response.json();

        if (responseData.success) {
          imageExists = true;
          imageSrc = `/download/${current_id}.jpg`;
          console.log(imageExists);
        } else {
          console.error('API request was not successful:', responseData.error);
        }
      } else {
        console.error('API request failed with status code:', response.status);
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

  import { onMount } from 'svelte';
  onMount(() => {
    document.body.style.backgroundColor = 'black';
    document.body.style.overflowY = 'visible';     // In the main page the scrollbar was desactivated

    updateInfo();
    updateImage();

    fromSlider1 = document.querySelector('#fromSlider1');
    toSlider1 = document.querySelector('#toSlider1');
    fromInput1 = document.querySelector('#fromInput1');
    toInput1 = document.querySelector('#toInput1');

    // Initialize the slider appearance for Set 1
    fillSlider(fromSlider1, toSlider1, '#C6C6C6', '#25daa5', toSlider1);
    setToggleAccessible(toSlider1, toInput1);

    // Event listeners for Set 1
    fromSlider1.oninput = () => controlFromSlider(fromSlider1, toSlider1, fromInput1);
    toSlider1.oninput = () => controlToSlider(fromSlider1, toSlider1, fromInput1);

    // Assign the elements for Set 2
    fromSlider2 = document.querySelector('#fromSlider2');
    toSlider2 = document.querySelector('#toSlider2');
    fromInput2 = document.querySelector('#fromInput2');
    toInput2 = document.querySelector('#toInput2');

    // Initialize the slider appearance for Set 2
    fillSlider(fromSlider2, toSlider2, '#C6C6C6', '#25daa5', toSlider2);
    setToggleAccessible(toSlider2, toInput2);

    // Event listeners for Set 2
    fromSlider2.oninput = () => controlFromSlider2(fromSlider2, toSlider2, fromInput2);
    toSlider2.oninput = () => controlFromSlider2(fromSlider2, toSlider2, fromInput2);

    // Assign the elements for Set 3
    fromSlider3 = document.querySelector('#fromSlider3');
    toSlider3 = document.querySelector('#toSlider3');
    fromInput3 = document.querySelector('#fromInput3');
    toInput3 = document.querySelector('#toInput3');

    // Initialize the slider appearance for Set 3
    fillSlider(fromSlider3, toSlider3, '#C6C6C6', '#25daa5', toSlider3);
    setToggleAccessible(toSlider3, toInput3);

    // Event listeners for Set 3
    fromSlider3.oninput = () => controlFromSlider3(fromSlider3, toSlider3, fromInput3);
    toSlider3.oninput = () => controlFromSlider3(fromSlider3, toSlider3, fromInput3);


    return () => {
      document.body.style.backgroundColor = ''; // or you can set it to the original color
      document.body.style.overflowY = 'auto'; // Desactivate scrollbar
    };
  })

  // Slider

  function controlFromSlider(fromSlider, toSlider, fromInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    if (from > to) {
      fromSlider.value = to;
      fromInput.value = to;
    } else {
      fromInput.value = from;
    }
    from_val1 = from;
    to_val1 = to;
  }

  function controlToSlider(fromSlider, toSlider, toInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    setToggleAccessible(toSlider, toInput); // Pass toInput to setToggleAccessible
    if (from <= to) {
      toSlider.value = to;
      toInput.value = to;
    } else {
      toInput.value = from;
      toSlider.value = from;
    }
    from_val1 = from;
    to_val1 = to;
  }

  function controlFromSlider2(fromSlider, toSlider, fromInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    if (from > to) {
      fromSlider.value = to;
      fromInput.value = to;
    } else {
      fromInput.value = from;
    }
    from_val2 = from;
    to_val2 = to;
  }

  function controlToSlider2(fromSlider, toSlider, toInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    setToggleAccessible(toSlider, toInput); // Pass toInput to setToggleAccessible
    if (from <= to) {
      toSlider.value = to;
      toInput.value = to;
    } else {
      toInput.value = from;
      toSlider.value = from;
    }
    from_val2 = from;
    to_val2 = to;
  }

  function controlFromSlider3(fromSlider, toSlider, fromInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    if (from > to) {
      fromSlider.value = to;
      fromInput.value = to;
    } else {
      fromInput.value = from;
    }
    from_val3 = from;
    to_val3 = to;
  }

  function controlToSlider3(fromSlider, toSlider, toInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    setToggleAccessible(toSlider, toInput); // Pass toInput to setToggleAccessible
    if (from <= to) {
      toSlider.value = to;
      toInput.value = to;
    } else {
      toInput.value = from;
      toSlider.value = from;
    }
    from_val3 = from;
    to_val3 = to;
  }
  

  function getParsed(currentFrom, currentTo) {
    const from = parseInt(currentFrom.value, 10);
    const to = parseInt(currentTo.value, 10);
    return [from, to];
  }

  function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = to.max-to.min;
    const fromPosition = from.value - to.min;
    const toPosition = to.value - to.min;
    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
      ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
      ${rangeColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} ${(toPosition)/(rangeDistance)*100}%, 
      ${sliderColor} 100%)`;
  }

  function setToggleAccessible(currentTarget, toInput) {
    if (Number(toInput.value) <= 0) {
      currentTarget.style.zIndex = 2;
    } else {
      currentTarget.style.zIndex = 0;
    }
  }
</script>

<main>
  <div class="image-container">
    {#if imageExists}
      <img src="/download/{current_id}.jpg" alt="" />
    {:else}
    <img src="/download/1.jpg" alt="" />
    {/if}
</div>
  <div class="info">
    <p class="best">Best Recommendation</p>
    <h1>{title}</h1>
    <ul>
        <li>{episodes} Episodes</li>
        <li>{type}</li>
        <li>{premiere}</li>
        <li>{studio}</li>
        <!--<li>{rating}</li>-->
    </ul>
    <p class="desc">
        {desc}
    </p>
    <p class="Genres">Avant Garde, Comedy, Drama, Mystery, Supernatural, Psychological</p>
    <button>MyAnimeList</button>
  </div>
  <h2>Best recommendations for you</h2>
  <div class="main-recs">
        <div class="number_Recs">
            <div class="number-row">
              <img src="./icons/1.png" alt="1">
                <img src="./icons/2.png" alt="2">
                <img src="./icons/3.png" alt="3">
                <img src="./icons/4.png" alt="4">
                <img src="./icons/5.png" alt="5">
            </div>
        </div>
        <div class="number_Recs">
            <div class="number-row-s">
                <img src="./icons/6.png" alt="6">
                <img src="./icons/7.png" alt="7">
                <img src="./icons/8.png" alt="8">
                <img src="./icons/9.png" alt="9">
                <img src="./icons/10.png" alt="10">
            </div>
        </div>
        <div class="recs">
          <div class="image-row">
            {#each mal_data.slice(0, 5) as { url, id } (url)}
            <img
              src={url}
              alt=""
              on:click={() => handleClick(id)}
              on:keydown={(event) => handleKeyDown(event, id)}
              />
            {/each}
          </div>
          <div class="image-row-s">
            {#each mal_data.slice(5) as { url, id } (url)}
            <img
              src={url}
              alt=""
              on:click={() => handleClick(id)}
              on:keydown={(event) => handleKeyDown(event, id)}
              />
            {/each}
          </div>
        </div>
    </div>
    <div>

    <div class="sliders">
      <div class="range_container">
        <div class="sliders_control">
          <input id="fromSlider1" type="range" value="1" min="1" max="99"/>
          <input id="toSlider1" type="range" value="100" min="2" max="100"/>
        </div>
        <div class="form_control">
          <p class="test" id="fromInput1">Episodes:</p>
          <div class="sections">
            <div class="form_control_container">
              <p class="test" id="fromInput1">{ from_val1 }&nbsp;-</p>
            </div>
            <div class="form_control_container">
            <p class="test" id="toInput1">&nbsp;{ to_val1 }</p>
            </div>
          </div>
        </div>
      </div>

      <div class="range_container">
        <div class="sliders_control">
          <input id="fromSlider2" type="range" value="1" min="1" max="9"/>
          <input id="toSlider2" type="range" value="10" min="2" max="10"/>
        </div>
        <div class="form_control">
          <p class="test" id="fromInput2">Score:</p>
          <div class="sections">
            <div class="form_control_container">
              <p class="test" id="fromInput2">{ from_val2 }&nbsp;-</p>
            </div>
            <div class="form_control_container">
            <p class="test" id="toInput2">&nbsp;{ to_val2 }</p>
            </div>
          </div>
        </div>
      </div>

      <div class="range_container">
        <div class="sliders_control">
          <input id="fromSlider3" type="range" value="1970" min="1970" max="2022"/>
          <input id="toSlider3" type="range" value="2022" min="1971" max="2023"/>
        </div>
        <div class="form_control">
          <p class="test" id="fromInput3">Year:</p>
          <div class="sections">
            <div class="form_control_container">
              <p class="test" id="fromInput3">{ from_val3 }&nbsp;-</p>
            </div>
            <div class="form_control_container">
            <p class="test" id="toInput3">&nbsp;{ to_val3 }</p>
            </div>
          </div>
        </div>
      </div>
    </div>


    </div>
    <h2>Best <b>MOVIE</b> recommendations for you</h2>
    <div class="image-row-l">
      {#each mal_images.slice(0, 6) as url (url)}
        <img src={url} alt="">
      {/each}
    </div>
    <h2>Anime with less than <b>13</b> episodes</h2>
    <div class="image-row-l">
      {#each mal_images.slice(3, 9) as url (url)}
        <img src={url} alt="">
      {/each}
    </div>
</main>

<style>

.sliders{
  display: flex;
  justify-content: space-between;
}

.test{
  color: white;
  font-family: 'LatoLight', sans-serif;
  font-size: 18px;
}

.range_container {
  display: flex;
  flex-direction: column;
  width: 20%;
  margin: 100px auto;
}

.sliders_control {
  position: relative;
  min-height: 20px;
}

.sections{
  position: relative;
  display: flex;
  font-size: 24px;
  color: #635a5a;
}

.form_control {
  position: relative;
  display: flex;
  justify-content: space-between;
  font-size: 24px;
  color: #635a5a;
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  pointer-events: all;
  width: 24px;
  height: 24px;
  background-color: #fff;
  border-radius: 50%;
  box-shadow: 0 0 0 1px #C6C6C6;
  cursor: pointer;
}

input[type=range]::-moz-range-thumb {
  pointer-events: all;
  width: 24px;
  height: 24px;
  background-color: #fff;
  border-radius: 50%;
  box-shadow: 0 0 0 1px #C6C6C6;
  cursor: pointer;  
}

input[type=range]::-webkit-slider-thumb:hover {
  background: #f7f7f7;
}

input[type=range]::-webkit-slider-thumb:active {
  box-shadow: inset 0 0 3px #387bbe, 0 0 9px #387bbe;
  -webkit-box-shadow: inset 0 0 3px #387bbe, 0 0 9px #387bbe;
}


input[type="range"] {
  -webkit-appearance: none; 
  appearance: none;
  height: 10px;
  width: 100%;
  position: absolute;
  background-color: #C6C6C6;
  pointer-events: none;
}

#fromSlider3, #fromSlider2, #fromSlider1 {
  height: 0;
  z-index: 1;
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

  @font-face {
    font-family: 'LatoThin';
    src: url('/fonts/Lato-Thin.ttf') format('truetype');
  }

  main{
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      background-color: black;
  }

  .info{
      color: white;
      position: relative;
      z-index: 4;
      width: 500px;
      height: 480px;
      margin-left: 140px;
      margin-top: 130px;
  }

  .best{
      text-transform: uppercase;
      font-size: 12px;
      font-family: 'LatoBold', sans-serif;
      color: rgb(233, 208, 97);
  }

  .desc{
      font-weight: 100;
      font-size: 18px;
      font-family: 'LatoLight', sans-serif;
      opacity: 0.7;
  }

  button{
      margin-top: 5px;
      width: 100px;
      height: 35px;
  }

  p{
      margin: 0;
  }

  .Genres{
    margin: 20px 0 20px 0;
    font-size: 14px;
    letter-spacing: 1px;
  }

  h1{
      font-size: 50px;
      margin: 0;
      margin-top: 10px;
      line-height: 50px;
      max-width: 500px;
      text-transform: uppercase;
  }

  ul{
      list-style: none;
      width: 100%;
      padding: 0;
      margin: 25px 0 25px 0;
  }

  li{
      display: inline-block;
      font-size: 18px;
      margin-right: 30px;
  }

  .main-recs{
    height: 570px;
  }

  .image-container {
    position: absolute;
    overflow: hidden;
  }

  .image-container img {
    width: 80%; /* Adjust the image width as needed */
    float: right;
    /*margin-top: -60px;*/
  }

  .image-container::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(0,0,0,1) 20%, rgba(0,0,0,0.6685267857142857) 30%, rgba(0,0,0,0) 50%);
    pointer-events: none;
  }

  .image-container::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent 80%, black);
    pointer-events: none;
  }

  .recs {
    display: flex;
    flex-direction: column;
    align-items:flex-start;
}

.image-row {
    display: flex;
    justify-content: center;
    margin-bottom: 20px; /* Adjust the margin as needed */
    margin-left: 170px;
}

.image-row-s {
    display: flex;
    justify-content: center;
    margin-left: 170px;
}

.image-row-l {
    display: flex;
    justify-content: flex-start;
    margin-left: 130px;
    margin-top: 30px;
    margin-bottom: 70px;
}

.image-row-l img{
    margin-right: 20px;
    width: 500px;
}

.image-row img {
    height: 200px;
    width: 141px;
    margin-top: 45px;
    margin-bottom: 70px;
    z-index: 3;
    transition: .3s;
    margin-right: 128px;
}

.image-row img:hover {
    height: 225px;
    width: 160px;
    margin-bottom: 20px;
    margin-right: 108px;
}

.image-row-s img {
    height: 200px;
    width: 141px;
    z-index: 3;
    transition: .3s;
    margin-right: 128px;
}

.image-row-s img:hover{
    height: 225px;
    width: 160px;
    margin-right: 108px;
}

.number_Recs {
    display: flex;
    justify-content: center;
    position: absolute;
    align-items: flex-start;
    margin-top: 40px;
}

.number-row{
  margin-left: 60px;
}

.number-row-s{
    margin-left: 60px;
    margin-top: 290px;
}

.number-row img{
    height: 220px;;
    z-index: 0;
    margin-right: 155px;
}

b{
  font-family: 'LatoBold', sans-serif;
  letter-spacing: 1px;
}

h2{
    color: white;
    margin: 10px;
    margin-left: 150px;
    font-size: 18px;
    font-family: 'LatoLight', sans-serif;
    font-weight: bold;
    margin-bottom: 20px;
}

.number-row-s img{
    height: 220px;
    margin-right: 155px;
    z-index: 0;
}

</style>