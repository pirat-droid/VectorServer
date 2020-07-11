<!--suppress ES6ShorthandObjectProperty -->
<template>
    <div class="home">
        <h3>Список хостов</h3>
        <ul>
            <li><router-link to="/list-vm">Список виртуальных машин</router-link></li>
            <li><router-link to="/list-storage">Список носителей</router-link></li>
            <li><router-link to="/list-os">Список операционных систем</router-link></li>
        </ul>
        <div v-for="host in listHost">
        <ul>
            <li><a href="#" @click="goTo(host.id)"><h3>{{ host.name }}</h3></a> <p v-html="host.ip"></p><p v-html="host.os"></p></li>
        </ul>
        </div>
    </div>
</template>

<!--suppress JSUnresolvedVariable -->
<script>
    // @ is an alias to /src
    import HelloWorld from '@/components/HelloWorld.vue'
    // import Host from "./Host";

    export default {
        name: 'Home',
        data() {
            return {
                listHost: []
            }
        },
        components: {
            HelloWorld
        },
        created() {
            this.loadListHost()
        },
        methods: {
            async loadListHost() {
                this.listHost = await fetch(
                    `${this.$store.getters.getServerUrl}/list-host/`
                ).then(response => response.json())
                console.log(this.listHost)
            },
            goTo(id){
                this.$router.push({
                    name: 'Host',
                    params: {id: id}
                })
            },
        },
    }
</script>
