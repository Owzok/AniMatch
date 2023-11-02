<script>
  import { inputValue } from '../store';

  let todos = null;
  let title_val = ""
  let imageExists = false;
  let imageSrc = null;

  const unsubscribe = inputValue.subscribe(value => {
    title_val = value
  });

  async function fetchTodos() {
    try {
      const response = await fetch('http://127.0.0.1:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title_val, k: 10 }), // Replace with your API request payload
      });

      if (response.ok) {
        const json = await response.json();
        todos = json;
      } else {
        console.error('Failed to fetch data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  async function checkImageExists() {
    try {
      const response = await fetch(`/download/1.jpg`);
      imageExists = response.ok;

      if (imageExists) {
        imageSrc = `/download/1.jpg`;
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  async function generateImage() {
    const api_url = 'http://localhost:5000/scrape_image';  // Update with your actual API endpoint

    try {
      const response = await fetch(api_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search_query: title_val, id: '1' }),
      });

      if (response.ok) {
        console.log("Answered!")
        const responseData = await response.json();
        if (responseData.success) {
          // Image was generated successfully
          imageExists = true;
          imageSrc = `/download/1.jpg`;
          console.log(imageExists);
        } else {
          // Image generation failed
          console.error('API request was not successful:', responseData.error);
        }
      } else {
        console.error('API request failed with status code:', response.status);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  // Call the fetchTodos function when the component is mounted
  import { onMount } from 'svelte';
  onMount(() => {
    fetchTodos();
    checkImageExists();
    generateImage();
  })
</script>

<main>
  <h1>About Page</h1>
  <div>
    <h2>Recommendations:</h2>
    <pre>{JSON.stringify(todos, null, 2)}</pre>
  </div>
  <div>
    <h2>Image:</h2>
    {#if imageExists}
      <img src="/download/1.jpg" alt="" />
    {:else}
      <p>Image not found</p>
    {/if}
  </div>
</main>