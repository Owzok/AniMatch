<script>
  import { inputValue } from '../store';

  let todos = null;
  let title_val = ""

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

  // Call the fetchTodos function when the component is mounted
  import { onMount } from 'svelte';
  onMount(fetchTodos);
</script>

<main>
  <h1>About Page</h1>
  <div>
    <h2>Recommendations:</h2>
    <pre>{JSON.stringify(todos, null, 2)}</pre>
  </div>
</main>