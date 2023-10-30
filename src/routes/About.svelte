<script>
  let todos = [];

  async function fetchTodos() {
    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/todos/1');
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
    <h2>Todos:</h2>
    <pre>{JSON.stringify(todos, null, 2)}</pre>
  </div>
</main>