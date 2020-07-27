<template>
    <section id="sidebar">
        <div class="inner">
            <nav>
                <ul>
                    <li>
                        <router-link to="/list-host">Hosts</router-link>
                    </li>
                    <li>
                        <router-link to="/list-vm">Virtual machines</router-link>
                    </li>
                    <li>
                        <router-link to="/list-storage">Storages</router-link>
                    </li>
                    <li>
                        <router-link to="/list-operating-system">Operating systems</router-link>
                    </li>
                    <li><a href="http://127.0.0.1:8000/api/script-xls-create/">Uploading a report to .xls</a></li>
                </ul>
            </nav>
        </div>
    </section>
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