<template>
  <body data-spy="scroll" data-target=".site-navbar-target" data-offset="300">

  <!--  <div id="overlayer"></div>-->
  <!--  <div class="loader">-->
  <!--    <div class="spinner-border text-primary" role="status">-->
  <!--      <span class="sr-only">Loading...</span>-->
  <!--    </div>-->
  <!--  </div>-->

  <div class="site-wrap">

    <div class="site-mobile-menu site-navbar-target">
      <div class="site-mobile-menu-header">
        <div class="site-mobile-menu-close mt-3">
          <span class="icon-close2 js-menu-toggle"></span>
        </div>
      </div>
      <div class="site-mobile-menu-body"></div>
    </div>

    <header class="site-navbar py-4 js-sticky-header site-navbar-target" role="banner">

      <div class="container">
        <div class="row align-items-center justify-content-center">

          <div class="col-2">
            <h1 class="m-0 site-logo">
              <router-link to="/list-host">Мониторинг</router-link>
            </h1>
          </div>

          <div class="col-10">
            <nav class="site-navigation position-relative text-right" role="navigation">
              <ul class="site-menu main-menu js-clone-nav mr-auto d-none d-lg-block">
                <li>
                  <router-link to="/list-host">Хосты</router-link>
                </li>
                <li>
                  <router-link to="/list-vm">Виртуальные машины</router-link>
                </li>
                <li>
                  <router-link to="/list-storage">Накопители</router-link>
                </li>
                <li>
                  <router-link to="/list-operating-system">Операционные системы</router-link>
                </li>
                <li><a href="http://192.168.19.132:8000/api/script-xls-create/">Выгрузка отчёта в .xls</a></li>
              </ul>
            </nav>
            <a href="#" class="d-inline-block d-lg-none site-menu-toggle js-menu-toggle float-right"><span
                class="icon-menu h3"></span></a>
          </div>
        </div>
      </div>

    </header>


    <!--    <div class="site-blocks-cover overlay bg-light" style="background-image: url('assets/images/hero_bg_1.jpg'); " id="home-section">-->

    <div class="container">
      <div class="row justify-content-center">

        <div class="col-12 text-center align-self-center text-intro">
          <div class="row justify-content-center">
            <div class="col-lg-8">
              <h1 class="text-white" data-aos="fade-up" data-aos-delay="">We Are Digital Services</h1>
              <p class="lead text-white" data-aos="fade-up" data-aos-delay="100">Lorem ipsum dolor sit amet, consectetur
                adipisicing elit. Dignissimos magnam maxime voluptates libero, nobis impedit aut corrupti sunt
                possimus.</p>
              <p data-aos="fade-up" data-aos-delay="200"><a href="#services-section"
                                                            class="btn smoothscroll btn-primary">Our Services</a></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </body>
</template>

<script>
export default {
  name: "Nav",
  methods: {
    async CreateReport() {
      this.host = await fetch(
          `${this.$store.getters.getServerUrl}/script-xls-create/`
      ).then(response => response.json())
    },
  }
}
</script>

<style scoped>

</style>