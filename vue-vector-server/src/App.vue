<template>
    <div id="app">
        <Nav />
        <router-view/>
        <Footer />
    </div>
</template>

<style>
    @import "assets/css/main.css";
    @import "assets/css/noscript.css";
    @import "assets/css/fontawesome-all.min.css";
</style>
<script>
    import Nav from "./components/Nav";
    import Footer from "./components/Footer";
    export default {
        components: {Footer, Nav}
    }
</script>