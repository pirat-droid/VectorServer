<template>
    <div id="app">
        <Nav />
        <router-view/>
        <Footer />
    </div>
</template>

<style>
@import "assets/css/bootstrap/bootstrap.css";
@import "assets/css/jquery-ui.css";
@import "assets/css/owl.carousel.min.css";
@import "assets/css/owl.theme.default.min.css";
@import "assets/css/owl.theme.default.min.css";
@import "assets/css/jquery.fancybox.min.css";
@import "assets/css/bootstrap-datepicker.css";
@import "assets/fonts/flaticon/font/flaticon.css";
@import "assets/css/aos.css";
@import "assets/css/style.css";
</style>
<script src="assets/js/jquery-3.3.1.min.js"></script>
<script src="assets/js/jquery-ui.js"></script>
<script src="assets/js/popper.min.js"></script>
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/owl.carousel.min.js"></script>
<script src="assets/js/jquery.easing.1.3.js"></script>
<script src="assets/js/aos.js"></script>
<script src="assets/js/jquery.fancybox.min.js"></script>
<script src="assets/js/jquery.sticky.js"></script>
<script src="assets/js/isotope.pkgd.min.js"></script>
<script>
    import Nav from "./components/Nav";
    import Footer from "./components/Footer";
    export default {
        components: {Footer, Nav}
    }
</script>