<script>
  import { first_anime_id, anime_links } from '../store';

  let todos = null;
  let title_val = "";
  let imageExists = false;
  let imageSrc = null;
  let mal_images = [];

  const unsubscribe = first_anime_id.subscribe(value => {
    title_val = value
  });

  const unsubscribe2 = anime_links.subscribe(value => {
    mal_images = value
  });

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
    } else {
      generateImage();
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
  const api_url = 'http://127.0.0.1:5000/scrape_image';

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
    document.body.style.backgroundColor = 'black';
    document.body.style.overflowY = 'visible';

    retrieveInfo();
    checkImageExists();

    //fetchTodos();

    return () => {
      // Desactivate scrollbar
      document.body.style.backgroundColor = ''; // or you can set it to the original color
      document.body.style.overflowY = 'auto';
    };
  })

</script>

<main>
  <div class="image-container">
    {#if imageExists}
      <img src="/download/{title_val}.jpg" alt="" />
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
      max-height: 450px;
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

  pre{
    color: white;
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
    margin-left: 245px;
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
    height: 250px;
    margin-bottom: 70px;
    z-index: 3;
    transition: .3s;
    margin-right: 130px;
}

.image-row img:hover {
    height: 275px;
    margin-bottom: 20px;
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
}

.number_Recs {
    display: flex;
    justify-content: center;
    position: absolute;
    align-items: flex-start;
    margin-top: 40px;
}

.number-row{
    margin-left: 130px;
}

.number-row-s{
    margin-left: 60px;
    margin-top: 290px;
}

.number-row img{
    height: 225px;;
    z-index: 0;
    margin-right: 190px;
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