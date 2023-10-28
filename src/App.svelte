<script>
	import { Router, Route, Link } from 'svelte-routing';
    export let name;
    import About from './routes/About.svelte';
	import Home from './routes/Home.svelte';
</script>

<Router>
    <nav>
        <Link to="/">Home</Link>
        <Link to="about">About</Link>
    </nav>
    <div>
		<Route path="/" component={Home}/>
        <Route path="about" component={About} />
    </div>
</Router>

<main>
    <h1>Hello {name}!</h1>
    <p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>