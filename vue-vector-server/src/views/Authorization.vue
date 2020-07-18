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
                        <li><a href="#" class="button button-strart" @click="goTo">Get Started</a></li>
                    </ul>
                </form>
                <hr/>

            </section>
        </div>
    </section>
</template>

<script>
    export default {
        name: "Authorization",
        methods: {
            goTo() {
                this.$router.push({
                    name: 'Host',
                })
            },
        }
    }
</script>

<style scoped>
    /*.col-sm-10 {*/
    /*    max-width: 100%;*/
    /*}*/

    /*.container {*/
    /*    max-width: 100%;*/
    /*}*/

    /*.row {*/
    /*    margin-left: 7%;*/
    /*}*/
    /*.ma*/
    .input-text, .input-password {
        width: auto;
        margin-left: 40%;
    }
    .button-strart{
        margin-left: 40px;
        font-size: 0.75em;
    }
    .sign{
        margin-bottom: 3.5rem;
        margin-left: 45%;
    }
</style>