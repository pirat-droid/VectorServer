<template>
    <div class="vm">
        <h1>Имя виртуальной машины: {{ vm.name }}</h1>
        <p>Операционная система {{ vm.os }}, IP адрес {{ vm.ip }}, ядер {{ vm.cores }},
        потоков {{ vm.threads }}, памяти {{ vm.memory }}Гб., накопитель {{ vm.storage_size }} Гб.,
        размещен {{ vm.host }}</p>
        <h3>Описание:</h3>
        <p>{{ vm.description }}</p>
        <a href="#">Редактировать</a>
    </div>
</template>

<script>
    export default {
        name: "VM",
        props: ['id'],
        data() {
            return {
                vm: {}
            }
        },
        created() {
            this.LoadVM()
        },
        methods: {
            async LoadVM() {
                this.vm = await fetch(
                    `${this.$store.getters.getServerUrl}/vm/${this.id}`
                ).then(response => response.json())
                console.log(this.vm)
                console.log(this.id)
            }
        },
    }
</script>

<style scoped>

</style>