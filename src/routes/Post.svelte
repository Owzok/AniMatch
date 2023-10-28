<script>
    import { onMount } from 'svelte';
    import { params } from 'svelte-routing';
  
    let id;
    onMount(() => {
      id = $params.id;
      // Fetch and display the post based on the id
    });
  </script>
  
  <h2>Post {id}</h2>