<template>
    <div class="storage">
        <h3>Накопитель</h3>
    </div>
</template>

<script>
    export default {
        name: "Storage",
        props: ['id'],
        data() {
            return {
                storage: {}
            }
        },
        created() {
            this.LoadStorage()
        },
        methods: {
            async LoadStorage() {
                this.storage = await fetch(
                    `${this.$store.getters.getServerUrl}/storage/${this.id}`
                ).then(response => response.json())
                console.log(this.storage)
                console.log(this.id)
            },
        }
    }
</script>

<style scoped>

</style>