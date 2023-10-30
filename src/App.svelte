<script>
	import { Router, Route, Link } from 'svelte-routing';
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

</main>

<style>
    main{
        overflow-y: hidden;
        overflow-x: hidden;
        padding: 0px;
    }
    nav{
        position: absolute;
    }
</style>