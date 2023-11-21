<script>
  import { inputValue, user } from '../store';

  let todos = null;
  let title_val = "";
  let imageExists = false;
  let imageSrc = null;
  let mal_images = [];

  //const unsubscribe = inputValue.subscribe(value => {
  //  title_val = value
  //});

  let title = "";
  let episodes = "";
  let type = "";
  let premiere = "";
  let studio = "";
  let rating = "";
  let desc = "";

  async function fetchTodos() {
  try {
    const response = await fetch('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: title_val, k: 10 }),
    });

    if (response.ok) {
      // Await the response.json() method to get the actual JSON data
      const json = await response.json();

      // Check if the 'results' property exists in the response
      if ('results' in json) {
        const parsedResults = JSON.parse(json.results);

        const firstAnimeId = parsedResults[0].anime_id;
        const restOfUrls = parsedResults.slice(1).map(entry => entry.anime_image_url);

        title_val = firstAnimeId;
        mal_images = restOfUrls;

        console.log("First anime_id:", firstAnimeId);
        console.log("Rest of the anime_image_urls:", restOfUrls);
        console.log('mal_images:', mal_images);
        retrieveInfo();
        checkImageExists();
        //generateImage();
      } else {
        console.error('Results property not found in the response:', json);
      }
      } else {
        console.error('Failed to fetch data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  async function checkImageExists() {
  try {
    const response = await fetch(`/download/${title_val}.jpg`);
    imageExists = response.ok;

    if (imageExists) {
      imageSrc = `/download/${title_val}.jpg`;
    }
  } catch (error) {
      console.error('Error:', error);
    }
  }

  async function retrieveInfo() {
  try {
    const response = await fetch('http://127.0.0.1:5000/get_info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: title_val }),
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

async function generateImage() {
  const api_url = 'http://localhost:5000/scrape_image';

  try {
    const response = await fetch(`/download/${title_val}.jpg`);
    imageExists = response.ok;

    if (imageExists) {
      imageSrc = `/download/${title_val}.jpg`;
    } else {
      const response = await fetch(api_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: title_val }),
      });

      if (response.ok) {
        console.log("Answered!");
        const responseData = await response.json();

        if (responseData.success) {
          imageExists = true;
          imageSrc = `/download/${title_val}.jpg`;
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
    // In the main page the scrollbar was desactivated
    document.body.style.overflowY = 'visible';


    fetchTodos();


    return () => {
      // Desactivate scrollbar
      document.body.style.overflowY = 'auto';
    };
  })

</script>

<main>
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
  <div class="image-container">
      {#if imageExists}
        <img src="/download/{title_val}.jpg" alt="" />
      {:else}
      <img src="/download/1.jpg" alt="" />
      {/if}
  </div>
  <div>
    <h2>Best recommendations for you:</h2>
    <!--<pre>{JSON.stringify(todos, null, 2)}</pre>-->
  </div>
        <div class="number_Recs">
            <div class="number-row">
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
            {#each mal_images.slice(0, 4) as url (url)}
              <img src={url} alt="">
            {/each}
          </div>
          <div class="image-row-s">
            {#each mal_images.slice(4) as url (url)}
              <img src={url} alt="">
            {/each}
          </div>
        </div>
</main>

<style>
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
      position: absolute;
      z-index: 4;
      width: 550px;
      margin-left: 80px;
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

  .image-container {
    position: relative;
    overflow: hidden;
  }

  .image-container img {
    width: 70%; /* Adjust the image width as needed */
    float: right;
    margin-top: -60px;
  }

  .image-container::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(0,0,0,1) 30%, rgba(0,0,0,0.6685267857142857) 50%, rgba(0,0,0,0) 70%);
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

  pre{
    color: white;
  }

  .recs {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.image-row {
    display: flex;
    justify-content: center;
    margin-bottom: 20px; /* Adjust the margin as needed */
}

.image-row-s {
    display: flex;
    justify-content: center;
    margin-bottom: 20px; /* Adjust the margin as needed */
}

.image-row img {
    height: 250px;
    margin-left: 130px;
    margin-bottom: 70px;
    z-index: 3;
    transition: .3s;
}

.image-row img:hover {
    height: 275px;
    margin-bottom: 20px;
}

.image-row-s img {
    height: 200px;
    margin-left: 130px;
    z-index: 3;
    transition: .3s;
}

.image-row-s img:hover{
    height: 225px;
}

.number_Recs {
    display: flex;
    justify-content: center;
    position: absolute;
    margin-top: 25px;
}

.number-row{
    margin-left: 58px;
}

.number-row img{
    height: 225px;
    margin-left: 53px;
    z-index: 0;
}

h2{
    color: white;
    margin-left: 80px;
    margin-bottom: 40px;
}

.number-row-s img{
    height: 200px;
    margin-top: 320px;
    z-index: 0;
    margin-left: 58px;
}

</style>