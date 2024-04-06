<script>
  import { anime_links, anime_ids, all_data } from '../store';
  import { onMount } from 'svelte';
  // mal_ids is anime_ids
  // mal_images is anime_links
  // fetched_data is all_data

  let selectedChoice = null, choiceElements = null, selectedChoice2 = null, choiceElements2 = null;
  let toggleContainers = null, togglerStates = null;

  let imageExists = false, imageSrc = null;
  let mal_images = [], mal_ids = [], fetched_data = [];
  let menuItem = null, menuSlided = false, menu_active = false,menu = null;

  // Sliders Set 1
  let fromSlider1, toSlider1, fromInput1, toInput1;
  let from_val1 = 1, to_val1 = 100;
  // Sliders Set 2
  let fromSlider2, toSlider2, fromInput2, toInput2;
  let from_val2 = 1, to_val2 = 10;
  // Sliders Set 3
  let fromSlider3, toSlider3, fromInput3, toInput3;
  let from_val3 = 1970, to_val3 = 2023;

  let title = "", episodes = "", members = "", score = "", ranked = "", desc = "", genres = "", genresArray = [];

  // this variable isnt used, but is required to do a "suscribe"
  const unsubscribe2 = anime_links.subscribe(value => { mal_images = value });
  const sus3 = anime_ids.subscribe(value => { mal_ids = value })
  const sus_alldata = all_data.subscribe(value => { fetched_data = value })

  // FILTER IDS
  let filtered_ids = [], movie_ids = [], short_ids = [], long_ids = [], old_ids = [], newer_ids = [];

  // Utils
  function zipArrays(arr1, arr2) { return arr1.map((url, index) => ({ url, id: arr2[index] })); }
  function handleKeyDown(event, id) { if (event.key === 'Enter' || event.key === ' ') { handleClick(id); } }

  let mal_data = zipArrays(mal_images, mal_ids);

  // Updates the top banner and the current id info
  function handleClick(id) {
    current_id = id;
    change_banner();
  }
  
  // Initial current id is recommendations first element (best recommendation)
  let current_id = mal_ids.slice(0, 1)[0];

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

    // if the members is 1.2M, it will
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
        console.log(data);
        title = data.Name;
        episodes = data.Episodes;
        if (episodes === '1'){
          episodes = 'Movie';
        }
        score = data.Score;
        members = data.Members;
        members = formatScore(data.Members);
        desc = data.synopsis;
        ranked = data.Ranked;
        genres = data.Genres;
        genresArray = genres.split(',').map(genre => genre.trim());
        console.log(genresArray);
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
    scrollToTop();
  }

  async function movieFilter(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ min_episodes: 1, max_episodes: 1, fetched_data: fetched_data }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        movie_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
      } else { console.error('Failed to fetch data'); }
  }

  async function shortFilter(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ min_episodes: 6, max_episodes: 13, fetched_data: fetched_data
        }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        short_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
      } else {
        console.error('Failed to fetch data');
      }
  }

  async function longFilter(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ min_episodes: 50, fetched_data: fetched_data }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        long_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
      } else {
        console.error('Failed to fetch data');
      }
  }

  async function oldFilter(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ max_year: 2003, fetched_data: fetched_data }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        old_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
      } else {
        console.error('Failed to fetch data');
      }
  }

  async function newerFilter(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ min_year: 2018, fetched_data: fetched_data }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        newer_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
      } else {
        console.error('Failed to fetch data');
      }
  }

  async function applyFilters(){
      const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({
          min_score: from_val2,
          max_score: to_val2,
          min_episodes: from_val1,
          max_episodes: to_val1,
          min_year: from_val3,
          max_year: to_val3,
          mature: togglerStates[0],
          prequel: togglerStates[2],
          fetched_data: fetched_data
        }),
      });

      if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        filtered_ids = filteredData;
        
        await fetch('http://127.0.0.1:5000/profile_pics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', },
          body: JSON.stringify({ ids: filteredData }),
        });
        //sendToRecommendRoute(filteredData);
      } else {
        console.error('Failed to fetch data');
      }
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

  onMount(() => {
    document.body.style.backgroundColor = 'black';
    document.body.style.overflowY = 'visible';     // In the main page the scrollbar was desactivated

    selectedChoice = document.querySelector('.selected-el').textContent;
    choiceElements = document.querySelectorAll('.choice-el');

    selectedChoice2 = document.querySelector('.selected-el2').textContent;
    choiceElements2 = document.querySelectorAll('.choice-el2');

    toggleContainers = document.querySelectorAll('.container-toggle');
    togglerStates = Array.from(toggleContainers, container => {
      return container.querySelector('.slider').classList.contains('sl-toggled');
    });
    choiceElements.forEach(element => {
      element.addEventListener('click', handleChoiceClick);
    });

    choiceElements2.forEach(element => {
      element.addEventListener('click', handleChoiceClick2);
    });

    toggleContainers.forEach((container, index) => {
      container.addEventListener('click', handleTogglerClick(index));
    });

    updateInfo();
    updateImage();
    movieFilter();
    shortFilter();
    newerFilter();
    longFilter();
    oldFilter();

    fromSlider1 = document.querySelector('#fromSlider1');
    toSlider1 = document.querySelector('#toSlider1');
    fromInput1 = document.querySelector('#fromInput1');
    toInput1 = document.querySelector('#toInput1');

    // Initialize the slider appearance for Set 1
    fillSlider(fromSlider1, toSlider1, '#C6C6C6', '#000000', toSlider1);
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
    fillSlider(fromSlider2, toSlider2, '#C6C6C6', '#000000', toSlider2);
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
    fillSlider(fromSlider3, toSlider3, '#C6C6C6', '#000000', toSlider3);
    setToggleAccessible(toSlider3, toInput3);

    // Event listeners for Set 3
    fromSlider3.oninput = () => controlFromSlider3(fromSlider3, toSlider3, fromInput3);
    toSlider3.oninput = () => controlFromSlider3(fromSlider3, toSlider3, fromInput3);

    toSlider1.value = 100; // Set the initial max value for Set 1
    toSlider2.value = 10;  // Set the initial max value for Set 2
    toSlider3.value = 2023; // Set the initial max value for Set 3
    fillSlider(fromSlider3, toSlider3, '#C6C6C6', '#000000', toSlider3);
    
    menu = document.querySelector(".burger");
    menuItem = document.querySelector(".menu-items")

    return () => {
      document.body.style.backgroundColor = ''; // or you can set it to the original color
      document.body.style.overflowY = 'auto'; // Desactivate scrollbar
    };
  })

  // Slider
  function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
    const rangeDistance = to.max - to.min;
    const fromPosition = (from.value - to.min) / rangeDistance * 100;
    const toPosition = (to.value - to.min) / rangeDistance * 100;

    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${fromPosition}%,
      ${rangeColor} ${fromPosition}%,
      ${rangeColor} ${toPosition}%, 
      ${sliderColor} ${toPosition}%,
      ${sliderColor} 100%)`;
  }

  function controlFromSlider(fromSlider, toSlider, fromInput) {
    const [from, to] = getParsed(fromSlider, toSlider);
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#000000', toSlider);
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

  let currentIndexCinematicGems = 0, currentIndexShortStories = 0;
  const moviesPerPageCinematicGems = 6, totalMoviesCinematicGems = 20;
  const moviesPerPageShortStories = 6, totalMoviesShortStories = 20;

  function updateImageDisplayCinematicGems() {
    const imageContainer = document.querySelector('.cinematic-gems');
    const translateXValue = -currentIndexCinematicGems * 93 / moviesPerPageCinematicGems + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonCG');
    const nextButton = document.querySelector('#nextButtonCG');
    prevButton.disabled = currentIndexCinematicGems === 0;
    nextButton.disabled = currentIndexCinematicGems + moviesPerPageCinematicGems >= totalMoviesCinematicGems;
  }

  function showNextCinematicGems() {
    currentIndexCinematicGems += moviesPerPageCinematicGems;
    console.log("NEXT");
    updateImageDisplayCinematicGems();
  }

  function showPrevCinematicGems() {
    currentIndexCinematicGems -= moviesPerPageCinematicGems;
    console.log("PREV");
    updateImageDisplayCinematicGems();
  }

  function updateImageDisplayShortStories() {
    const imageContainer = document.querySelector('.short-stories');
    const translateXValue = -currentIndexShortStories * 93 / moviesPerPageShortStories + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonSS');
    const nextButton = document.querySelector('#nextButtonSS');
    prevButton.disabled = currentIndexShortStories === 0;
    nextButton.disabled = currentIndexShortStories + moviesPerPageShortStories >= totalMoviesShortStories;
  }

  function showNextShortStories() {
    currentIndexShortStories += moviesPerPageShortStories;
    console.log("NEXT");
    updateImageDisplayShortStories();
  }

  function showPrevShortStories() {
    currentIndexShortStories -= moviesPerPageShortStories;
    console.log("PREV");
    updateImageDisplayShortStories();
  }

  let currentIndexEpicJourneys = 0;
  const moviesPerPageEpicJourneys = 6;  // Adjust as needed
  const totalMoviesEpicJourneys = 20;  // Adjust as needed

  function updateImageDisplayEpicJourneys() {
    const imageContainer = document.querySelector('.epic-journeys');
    const translateXValue = -currentIndexEpicJourneys * 93 / moviesPerPageEpicJourneys + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonEJ');
    const nextButton = document.querySelector('#nextButtonEJ');
    prevButton.disabled = currentIndexEpicJourneys === 0;
    nextButton.disabled = currentIndexEpicJourneys + moviesPerPageEpicJourneys >= totalMoviesEpicJourneys;
  }

  function showNextEpicJourneys() {
    currentIndexEpicJourneys += moviesPerPageEpicJourneys;
    updateImageDisplayEpicJourneys();
  }

  function showPrevEpicJourneys() {
    currentIndexEpicJourneys -= moviesPerPageEpicJourneys;
    updateImageDisplayEpicJourneys();
  }

  let currentIndexVintageAnime = 0;
  const moviesPerPageVintageAnime = 6;  // Adjust as needed
  const totalMoviesVintageAnime = 20;  // Adjust as needed

  function updateImageDisplayVintageAnime() {
    const imageContainer = document.querySelector('.vintage-anime');
    const translateXValue = -currentIndexVintageAnime * 93 / moviesPerPageVintageAnime + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonVA');
    const nextButton = document.querySelector('#nextButtonVA');
    prevButton.disabled = currentIndexVintageAnime === 0;
    nextButton.disabled = currentIndexVintageAnime + moviesPerPageVintageAnime >= totalMoviesVintageAnime;
  }

  function showNextVintageAnime() {
    currentIndexVintageAnime += moviesPerPageVintageAnime;
    updateImageDisplayVintageAnime();
  }

  function showPrevVintageAnime() {
    currentIndexVintageAnime -= moviesPerPageVintageAnime;
    updateImageDisplayVintageAnime();
  }

  let currentIndexLatestAnime = 0;
  const moviesPerPageLatestAnime = 6;  // Adjust as needed
  const totalMoviesLatestAnime = 20;  // Adjust as needed

  function updateImageDisplayLatestAnime() {
    const imageContainer = document.querySelector('.latest-anime');
    const translateXValue = -currentIndexLatestAnime * 93 / moviesPerPageLatestAnime + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonLA');
    const nextButton = document.querySelector('#nextButtonLA');
    prevButton.disabled = currentIndexLatestAnime === 0;
    nextButton.disabled = currentIndexLatestAnime + moviesPerPageLatestAnime >= totalMoviesLatestAnime;
  }

  function showNextLatestAnime() {
    currentIndexLatestAnime += moviesPerPageLatestAnime;
    updateImageDisplayLatestAnime();
  }

  function showPrevLatestAnime() {
    currentIndexLatestAnime -= moviesPerPageLatestAnime;
    updateImageDisplayLatestAnime();
  }

  let currentIndexFiltered = 0;
  const moviesPerPageFiltered = 6;  // Adjust as needed
  const totalMoviesFiltered = 20;  // Adjust as needed

  function updateImageDisplayFiltered() {
    const imageContainer = document.querySelector('.filtered-anime');
    const translateXValue = -currentIndexFiltered * 93 / moviesPerPageFiltered + '%';
    imageContainer.style.transform = `translateX(${translateXValue})`;

    // Disable/enable buttons based on the current index
    const prevButton = document.querySelector('#prevButtonF');
    const nextButton = document.querySelector('#nextButtonF');
    prevButton.disabled = currentIndexFiltered === 0;
    nextButton.disabled = currentIndexFiltered + moviesPerPageFiltered >= totalMoviesFiltered;
  }

  function showNextFiltered() {
    currentIndexFiltered += moviesPerPageFiltered;
    updateImageDisplayFiltered();
  }

  function showPrevFiltered() {
    currentIndexFiltered -= moviesPerPageFiltered;
    updateImageDisplayFiltered();
  }

  function scrollToTop() {
    // Scroll to the top of the page with smooth behavior
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }


  let selectedOption = null;
  
  function toggleDropdown() {
    const dropdown = document.getElementById("myDropdown");
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
  }

  let menu_on = false;

  function updateBool(){
      const bodyOverflow = document.body.style.overflowY;
      document.body.style.overflowY = bodyOverflow === 'visible' ? 'hidden' : 'visible';

      menu_on = !menu_on;
      const panel = document.getElementById("menu");
      const overlay = document.getElementById("overlay");

      overlay.style.display = (overlay.style.display === "block") ? "none" : "block";

      if (menu_on){
          panel.classList.add("on");
          panel.classList.remove("off");

          overlay.classList.add("activated")
      } else {
          panel.classList.remove("on");
          panel.classList.add("off");

          overlay.classList.remove("activated")
      }
  };

  function handleChoiceClick(event) {
      // Remove the selected class from all choice elements
      choiceElements.forEach(element => {
          element.classList.remove('selected-el');
      });
      // Add the selected class to the clicked choice element
      event.target.classList.add('selected-el');
      // Update the selectedChoice variable
      selectedChoice = event.target.textContent;
  }

  function handleChoiceClick2(event) {
      // Remove the selected class from all choice elements
      choiceElements2.forEach(element => {
          element.classList.remove('selected-el2');
      });
      // Add the selected class to the clicked choice element
      event.target.classList.add('selected-el2');
      // Update the selectedChoice variable
      selectedChoice2 = event.target.textContent;
  }

  function setToggleAccessible(currentTarget, toInput) {
    if (Number(toInput.value) <= 0) {
      currentTarget.style.zIndex = 2;
    } else {
      currentTarget.style.zIndex = 0;
    }
  }

  function handleTogglerClick(index) {
      return function () {
          const slider = toggleContainers[index].querySelector('.slider');
          const toggle = toggleContainers[index].querySelector('.toggle');
          slider.classList.toggle('sl-toggled');
          toggle.classList.toggle('t-toggled');
          togglerStates[index] = slider.classList.contains('sl-toggled');
          console.log(togglerStates);
      };
  }
</script>

<main>
  <div class="menu-btn">
    <div class:burger={menu_active} on:click={updateBool} on:keydown={updateBool}>
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>

  <!-- TRUE MENU -->
  <div class="overlay" class:activated={menu_on} id="overlay"></div>

  <div class="menu" class:on={menu_on} class:off={!menu_on} id="menu">
    <div class="top">
      <button class="cross" on:click={updateBool} on:keydown={updateBool}>X</button>
      <h3>Filters</h3>
    </div>
    <div class="menu-container">
      <div class="sec1">
          <h2>Model Selection</h2>
          <p>Each model has its own strengths and weaknesses, for more info click <a href="/">here</a></p>

          <div class="mult-choice">
              <div class="choice-el selected-el">Auto-Encoder</div>
              <div class="choice-el">Perceptron</div>
              <div class="choice-el">Collab. Filtering</div>
          </div>
      </div>

      <div class="sec2">
          <h2>Filters</h2>
          <p>Move the handlers below to filter and make your anime search more precise</p>
          
          <div class="sliders" style="margin-bottom: 70px;">
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
                <input id="toSlider3" type="range" value="2023" min="1971" max="2023"/>
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

      <div class="sec3">
          <h2>Advanced Parameters</h2>  
          <div class="container-toggle">
              <div class="side-text">
                  <h4>Extra Seasons</h4>
                  <p>If turned on, it will include second and further seasons of shows.</p>
              </div>
              <div class="slider">
                  <div class="toggle"></div>
              </div>
          </div>

          <div class="container-toggle">
              <div class="side-text">
                  <h4>Include your already plan to watch shows</h4>
                  <p>By default, the shows you've marked already as PTW are excluded from the recommendations.</p>
              </div>
              <div class="slider">
                  <div class="toggle"></div>
              </div>
          </div>

          <div class="container-toggle">
              <div class="side-text">
                  <h4>Include mature content</h4>
                  <p>With this you agree to be 18 years old or older and giving your consent to watch explicit content.</p>
              </div>
              <div class="slider sl-toggled">
                  <div class="toggle t-toggled"></div>
              </div>
          </div>
      </div>

      <div class="sec4">
        <h2>Popularity Attenuation Factor</h2>
        <p>A higher value result in less-popular anime being weighted higher in recommendations.</p>

        <div class="mult-choice2">
          <div class="choice-el2 selected-el2">High</div>
          <div class="choice-el2">Medium</div>
          <div class="choice-el2">None</div>
        </div>
      </div>
    </div>
    <button class="filter-btn" on:click={applyFilters} on:click={updateBool}>Show results</button>
  </div>

  <!-- Main Panel -->

  <div class="image-container">
    {#if imageExists}
      <img src="/download/{current_id}.jpg" alt="" />
    {:else}
    <img src="/download/1.jpg" alt="" />
    {/if}
</div>
  <div class="info">
    <p class="p best">Ranked #<b style="font-size:18px;">{ranked}</b> on MAL</p>
    <h1>{title}</h1>
    <ul>
        <li class='li' style="font-size:22px;"><p class='p' style="font-size:14px;">SCORE</p>{score}</li>
        <li class='li' style="font-size:20px;"><p class='p' style="font-size:14px;">Members</p>{members}</li>
        <li class='li' style="font-size:20px;"><p class='p' style="font-size:14px;">Episodes</p>{episodes}</li>
        <li class='li'><a href="https://myanimelist.net/anime/{current_id}" target="_blank"><img style="width: 30px; height: 30px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);" src="/icons/mal.png" alt=""></a></li>
        <li class='li'><a href="https://anilist.co/anime/{current_id}" target="_blank"><img style="width: 30px; height: 30px; margin-left:-15px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);" src="/icons/anilist.png" alt=""></a></li>
    </ul>
    <p class="p desc">
      {desc}
    </p>
    <p class="Genres">
      {#each genresArray as genre (genre)}
        <span class="genre">{genre}</span>
      {/each}
    </p>
    <div class="thumbs">
      <p class='p'>Do you find the recommendations useful? </p>
      <img src="/icons/ThumbsUp.png" alt="thumbsup">
      <img src="/icons/ThumbsDown.png" alt="thumbsdown">
    </div>
  </div>


  <!-- Top 10 Recommendations -->


  <h2 class="h2">Best recommendations for you</h2>
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
            {#each mal_data.slice(5, 10) as { url, id } (url)}
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

    <!-- Actual Content -->

    </div>
    {#if filtered_ids.length > 0}
    <div>
      <div class="image-row-l filtered-anime" style="margin-top: 40px">
        {#each filtered_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonF" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevFiltered} disabled><i class="arrow left"></i></button>
        <button id="nextButtonF" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextFiltered}><i class="arrow right"></i></button>
      </div>
    </div>
    {/if}

    <h2 class="h2"><b>Cinematic Gems</b> Tailored Just for You</h2>
    <div>
      <div class="image-row-l cinematic-gems">
        {#each movie_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonCG" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevCinematicGems} disabled><i class="arrow left"></i></button>
        <button id="nextButtonCG" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextCinematicGems}><i class="arrow right"></i></button>
      </div>
    </div>
    
    <h2 class="h2"><b>Binge-Worthy Short Stories:</b> Anime Under 13 Episodes</h2>
    <div>
      <div class="image-row-l short-stories">
        {#each short_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonSS" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevShortStories} disabled><i class="arrow left"></i></button>
        <button id="nextButtonSS" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextShortStories}><i class="arrow right"></i></button>
      </div>
    </div>
    
    <h2 class="h2"><b>Epic Journeys Unfold:</b> Anime with 50+ Episodes</h2>
    <div>
      <div class="image-row-l epic-journeys">
        {#each long_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonEJ" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevEpicJourneys} disabled><i class="arrow left"></i></button>
        <button id="nextButtonEJ" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextEpicJourneys}><i class="arrow right"></i></button>
      </div>
    </div>
    
    <h2 class="h2"><b>Timeless Classics:</b> Dive into the World of Vintage Anime</h2>
    <div>
      <div class="image-row-l vintage-anime">
        {#each old_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonVA" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevVintageAnime} disabled><i class="arrow left"></i></button>
        <button id="nextButtonVA" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextVintageAnime}><i class="arrow right"></i></button>
      </div>
    </div>
    
    <h2 class="h2"><b>Fresh and Exciting:</b> Discover the Latest Anime Adventures</h2>
    <div>
      <div class="image-row-l latest-anime">
        {#each newer_ids.slice(0, 21) as id (id)}
          <img src={`../download/profiles/${id}.jpg`} alt="" on:click={() => handleClick(id)} on:keydown={(event) => handleKeyDown(event, id)}>
        {/each}
      </div>
      <div class="button-container">
        <button id="prevButtonLA" style="margin-top: -490px;" class="coolPrevbtn" on:click={showPrevLatestAnime} disabled><i class="arrow left"></i></button>
        <button id="nextButtonLA" style="margin-top: -490px;" class="coolNextbtn" on:click={showNextLatestAnime}><i class="arrow right"></i></button>
      </div>
    </div>
</main>

<style>
.overlay{
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    position: absolute;
    background-color: black;
    opacity: 0;
    transition: .5s ease-in-out;
    display: none;
}

.activated{
    opacity: 0.6;
    z-index: 11;
}

.filter-btn{
  background-color: #353535;
  color: white;
  height: 50px;
  width: 170px;
  border-radius: 8px;
  float: right;
  position: relative;
  margin-right: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.menu-container{
  width: 700px;
  height: 580px;
  overflow-x: hidden;
  overflow-y: auto;
  border-bottom: 1px solid #ccc;
}

.menu{
    background-color: white;
    width: 700px;
    position: fixed;
    margin-left: 30%;
    height: 720px;
    margin-top: 1000px;
    box-shadow: 5px 5px 20px 10px rgba(0,0,0,0.2);
    border-radius: 20px;
    opacity: 0;
    justify-content: center;
    z-index: 12;
}

.menu .top{
    position: relative;
    display: inline-flex;
    height: 60px;
    width: 100%;
    border-bottom: 1px solid #ccc;
}

.top h3{
    margin-left: 250px;
}

.cross{
    width: 60px;
    background-color: white;
    border: 0px;
    border-radius: 40px;
    margin-left: 5px;
    margin-top: 15px;
}

.cross:hover{
    background-color: rgb(235, 235, 235);
}

.sec1{
    padding: 24px;
    border-bottom: 1px solid #ccc;
}

.sec1 h2, .sec2 h2, .sec3 h2, .sec4 h2{
  font-family: 'LatoBold', sans-serif;
  font-size: 24px;
}

.sec1 p, .sec2 p, .sec3 p, .sec4 p{
  font-family: 'LatoLight', sans-serif;
  font-size: 14px;
}

.on{
    transform: translateY(-910px);
    transition: .5s ease-out;
    opacity: 1;
}

.off{
    transform: translateY(910px);
    transition: .5s ease-in;
}

/*

*/

.sec2{
    padding: 24px;
    height: 350px;
    border-bottom: 1px solid #ccc;
}

/*

*/

.sec3{
    padding: 24px;
    border-bottom: 1px solid #ccc;
}

.sec4{
  padding: 24px;
  border-bottom: 1px solid #ccc;
  height: 200px;
}

.container-toggle{
    display: block;
    height: 50px;
    margin: 20px 0px 20px 0px;
}

.side-text h4 {
  margin-top: 0;
  margin-bottom: 5px;
  font-family: 'LatoLight', sans-serif;
}

.side-text p {
    margin-top: 0;
    margin-bottom: 0;
    font-family: 'LatoLight', sans-serif;
}



.slider{
    margin-top: -30px;
    width: 50px;
    height: 32px;
    background-color: rgb(170,170,170);
    border-radius: 20px;
    float: right;
    transition: .1s;
    cursor: pointer;
}

.slider:hover{
    background-color: #353535;
}

.sl-toggled{
    background-color: #353535;
}

.t-toggled{
    transform: translateX(18px);
}

.toggle{
    width: 28px;
    height: 28px;
    margin: 2px;
    background-color: white;
    border-radius: 35px;
    transition: .1s ease-in-out;
}

/* 
        Multiple choice
*/

.mult-choice{
    display: inline-flex;
    margin-left: 30px;
}

.choice-el{
    border: 1px solid lightgrey;
    padding: 20px;
    width: 150px;
    cursor: pointer;
    background-color: white;
    display: flex;
    justify-content: center;
}

.choice-el:first-child{
    border-radius: 10px 0px 0px 10px;
}

.choice-el:last-child{
    border-radius: 0px 10px 10px 0px;
}

.choice-el:hover{
    border: 1px solid #353535;
}

.selected-el{
    border: 1px solid #353535;
    padding: 20px;
    cursor: pointer;
    background-color: #353535;
    color: white;
}

.mult-choice2{
    display: inline-flex;
    margin-left: 30px;
}

.choice-el2{
    border: 1px solid lightgrey;
    padding: 20px;
    width: 150px;
    cursor: pointer;
    background-color: white;
    display: flex;
    justify-content: center;
}

.choice-el2:first-child{
    border-radius: 10px 0px 0px 10px;
}

.choice-el2:last-child{
    border-radius: 0px 10px 10px 0px;
}

.choice-el2:hover{
    border: 1px solid #353535;
}

.selected-el2{
    border: 1px solid #353535;
    padding: 20px;
    cursor: pointer;
    background-color: #353535;
    color: white;
}

/* --- --- --- */

.menu-items ul li {
  margin-bottom: 0px;
}

.menu-btn{
  position: absolute;
  z-index: 12;
}

.menu-btn div{
  z-index: 5;
  margin-top: 50px;
  margin-left: 50px;
  width: 20px;
  height: 14px;
  cursor: pointer;
  position: relative;
}

.menu-btn div span {
  background-color: white;
  height: 2px;
  position: absolute;
  width: 100%;
  left: 0;
  transition: all 0.3s ease;
}

.menu-btn div span:first-child {
  top: 0;
}
.menu-btn div span:nth-child(2) {
  top: 6px;
}
.menu-btn div span:last-child {
  top: 12px;
}

.burger span:nth-child(2) {
  opacity: 0;
}
.burger span:first-child,
.burger span:last-child {
  top: 6px;
  background-color: red;
}
.burger span:first-child {
  transform: rotate(45deg);
}
.burger span:last-child {
  transform: rotate(-45deg);
}

  .button-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px; /* Adjust the margin as needed */
  }

  .coolNextbtn{
    background: linear-gradient(to right, #ffffff00, rgb(15,15,15));
    border: none;
    color: white;
    height: 350px;
    width: 150px;
  }

  .coolNextbtn:disabled .arrow{
    border: solid black;
  }

  .coolPrevbtn:disabled .arrow{
    border: solid black;
  }

  .coolPrevbtn{
    background: linear-gradient(to left, #ffffff00, rgb(15,15,15));
    border: none;
    color: white;
    height: 350px;
    width: 150px;
  }

  .arrow {
    border: solid white;
    border-width: 0 3px 3px 0;
    display: inline-block;
    padding: 3px;
  }

.right {
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}

.left {
  transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
}

.genre {
  margin-right: 5px;
  background-color: rgba(255,255,255,0.35);
  border-radius: 5px;
  padding: 5px 10px 5px 10px;
}

.thumbs{
  display: flex;
}

.thumbs p{
  margin: 10px 0 10px 0;
}

.thumbs img{
  width: 50px;
  height: 50px;
  margin-left: 20px;
  opacity: 0.3;
  transition: .3s;
  cursor:pointer;
}

.thumbs img:hover{
  opacity: 1;
  rotate: 360deg;
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
      background-color: rgb(15,15,15);
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

  .p{
      margin: 0;
  }

  .Genres{
    margin: 20px 0 20px 0;
    font-size: 14px;
    letter-spacing: 1px;
    width: 600px;
  }

  .info h1 {
      font-size: 50px;
      margin: 0;
      margin-top: 10px;
      line-height: 50px;
      width: 700px;
      text-transform: uppercase;
  }

  .info ul {
      list-style: none;
      width: 100%;
      padding: 0;
  }

  .info li, .li{
      display: inline-block;
      font-size: 18px;
      margin-right: 30px;
      font-family: 'Lato', sans-serif;
  }

  .info ul li p, .li p{
    font-size: 14px;
    font-family: 'LatoLight', sans-serif;
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
    background: linear-gradient(90deg, rgba(15,15,15,1) 20%, rgba(15,15,15,0.6685267857142857) 30%, rgba(0,0,0,0) 50%);
    pointer-events: none;
  }

  .image-container::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent 80%, rgb(15,15,15));
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
    z-index: 1;
}

.image-row-s {
    display: flex;
    justify-content: center;
    margin-left: 170px;
    z-index: 1;
}

.image-row-l {
    display: flex;
    justify-content: flex-start;
    margin-left: 130px;
    transition: transform 0.5s ease-in-out;
    z-index: 1;
}

.image-row-l img{
  height: 330px;
  width: 225px;
  margin-right: 10px;
  transition: .3s;
  margin-bottom: 70px;
}

.image-row-l img:hover{
  height: 350px;
  width: 235px;
  margin-bottom: 10px;
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
    z-index: 1;
    margin-right: 155px;
}

b{
  font-family: 'LatoBold', sans-serif;
  letter-spacing: 2px;
}

.h2{
    color: white;
    margin: 10px;
    margin-left: 150px;
    font-size: 22px;
    font-family: 'LatoLight', sans-serif;
    font-weight: bold;
}

.number-row-s img{
    height: 220px;
    margin-right: 155px;
    z-index: 1;
}

.range_container {
  display: flex;
  flex-direction: column;
  margin: 20px;
}

.sliders_control {
  position: relative;
  margin: 10px;
}

.sections{
  position: relative;
  display: flex;
  font-size: 14px;
  color: #635a5a;
}

.form_control {
  position: relative;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
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
  width: 30px;
  height: 30px;
}

input[type="range"] {
  -webkit-appearance: none; 
  appearance: none;
  height: 2px;
  width: 100%;
  position: absolute;
  background-color: #C6C6C6;
  pointer-events: none;
}

#fromSlider3, #fromSlider2, #fromSlider1 {
  height: 0;
  z-index: 1;
}

</style>