<script>
	import { Router, Route } from 'svelte-routing';
    import About from './routes/About.svelte';
	import Credits from './routes/Credits.svelte';
	import FAQ from './routes/FAQ.svelte';
	import Home from './routes/Home.svelte';
</script>

<Router>
    <div>
		<Route path="/" component={Home}/>
        <Route path="/about" component={About} />
        <Route path="/credits" component={Credits} />
        <Route path="/faq" component={FAQ} />
        <!--<Route path="stats" component={Stats} />-->
    </div>
</Router>

<style>
    @font-face {
    font-family: 'LatoLight';
    src: url('/fonts/Lato-Light.ttf') format('truetype');
    }
</style>  