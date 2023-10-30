<script>
	import { Router, Route, Link } from 'svelte-routing';
    import About from './routes/About.svelte';
	import Credits from './routes/Credits.svelte';
	import FAQ from './routes/FAQ.svelte';
	import Home from './routes/Home.svelte';
    import Stats from './routes/Stats.svelte';
</script>

<Router>
    <nav class="navbar">
        <div class="navbar-links">
            <Link to="/"><p class=logo>AniMatch</p></Link>
            <Link to="about"><p class="navbar-link">About</p></Link>
            <Link to="about"><p class="navbar-link">Credits</p></Link>
            <Link to="about"><p class="navbar-link">FAQ</p></Link>
            <p class="navbar-link inactive">Stats</p>
        </div>
    </nav>
    <div>
		<Route path="/" component={Home}/>
        <Route path="about" component={About} />
        <Route path="credits" component={Credits} />
        <Route path="faq" component={FAQ} />
        <!--<Route path="stats" component={Stats} />-->
    </div>
</Router>

<style>
    @font-face {
    font-family: 'LatoLight';
    src: url('/fonts/Lato-Light.ttf') format('truetype');
    }

    nav{
        position: absolute;
        z-index: 5;
        font-family: 'LatoLight', sans-serif;
    }
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #fff;
      padding: 10px;
    }
  
    .navbar-links {
        text-decoration: none;
        flex: 2;
        display: flex;
        justify-content: space-around;
        margin-top: 30px;
    }
  
    .navbar-link {
        color: #fff;
        font-size: 12px;
        margin: 0 60px;
    }

    .inactive{
        color: grey;
    }
  
    .logo {
        width: 30px;
        height: 30px;
        margin: 0 145px;
        color: white;
    }
</style>  