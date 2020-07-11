<template>
    <div class="list-storage">
        <h3>Список операционных систем</h3>
        <div v-for=" os in listOS">
            <p>{{ os.family }} {{ os.os }} {{ os.capacity}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListOS",
        data() {
            return {
                listOS: []
            }
        },
        created() {
            this.loadListOS()
        },
        methods: {
            async loadListOS() {
                this.listOS = await fetch(
                    `${this.$store.getters.getServerUrl}/list-os`
                ).then(response => response.json())
                console.log(this.listOS)
            }
        },
    }
</script>

<style scoped>

</style>