<template>
    <div class="list-storage">
        <h3>Список накопителей</h3>
        <div v-for="storage in listStorage">
            <ul>
                <li><a href="#"><h3>{{ storage.model }}</h3></a>
                    <p v-html="storage.type_storage"></p>
                    <p v-html="storage.inv"></p>
                    <p v-html="storage.size_storage"></p>
                    <p v-html="storage.date_install"></p></li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListStorage",
        data() {
            return {
                listStorage: []
            }
        },
        created() {
            this.loadListStorage()
        },
        methods: {
            async loadListStorage() {
                this.listStorage = await fetch(
                    `${this.$store.getters.getServerUrl}/list-storage`
                ).then(response => response.json())
                console.log(this.listStorage)
            }
        },
    }
</script>

<style scoped>

</style>