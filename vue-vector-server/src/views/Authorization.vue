<template>
  <section id="intro" class="wrapper style1 fullscreen fade-up">
    <div class="inner">
      <section id="main" class="main">
        <header>
          <!-- <span class="avatar"><img src="images/avatar.jpg" alt="" /></span> -->
          <h1>Server inventory</h1>
          <!-- <p>Senior Psychonautics Engineer</p> -->
        </header>

        <hr/>
        <h2 class="sign">Sign in!</h2>
        <form method="post" action="#">
          <div class="fields">
            <div class="field">
              <input class="input-text" type="text" name="name" id="name" placeholder="Name"/>
            </div>
            <div class="field">
              <input class="input-password" type="password" name="password" id="email" placeholder="Password"/>
            </div>
          </div>
          <ul class="actions special">
            <li><a href="#" class="button button-strart" @click="getLogin">Get Started</a></li>
          </ul>
        </form>
        <hr/>

      </section>
    </div>
  </section>
</template>

<script>
import $ from 'jquery'

export default {
  name: "Authorization",
  data() {
    return {
      login: '',
      passwrd: '',
    }
  },
  methods: {
    goTo() {
      this.$router.push({
        name: 'Host',
      })
    },
    getLogin() {
      $.ajax({
        url: `${this.$store.getters.getServerUrl}/list-vm/`,
        type: 'POST',
        data: {
          username: this.login,
          password: this.passwrd
        },
        success: (response) => {
          sessionStorage.setItem('auth/_token', response.data.attributes.auth_token)
        },
        error: (response) => {
          if (response.status === 400) {
            alert('Логин или пароль не верен')
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.input-text, .input-password {
  width: auto;
  margin-left: 40%;
}

.button-strart {
  margin-left: 40px;
  font-size: 0.75em;
}

.sign {
  margin-bottom: 3.5rem;
  margin-left: 45%;
}
</style>