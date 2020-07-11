<template>
    <div class="host">
        <div>
            <h1>Имя  хоста: {{ host.name }}</h1>
            <h3>Информация о хосте</h3>
            <p>Операционная система: {{ host.os}}, IP адрес: {{ host.ip }}, процессор {{ host.cpu }},
                объём оперативной памяти {{ host.memory }} Гб., инв. № {{ host.inv }}</p>
            <h3>Список накопителей:</h3>
            <span v-for="storage in host.storage" :key="storage.id">
                <p>Модель: {{ storage.model}} {{storage.type_storage}} {{storage.size_storage}}
                    Гб, инв. № {{ storage.inv }}, дата установки {{ storage.date_install }}</p>
            </span>
            <h3>Список виртуальных машин:</h3>
                        <ul v-for="vm in host.virtuals" >
                            <li><a @click="goTo(vm.id)">Имя {{ vm.name }}, операционная система {{ vm.os }}, IP адрес {{ vm.ip }} </a></li>
                        </ul>
            <h3>Описание хоста</h3>
            <p>{{ host.description}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Host",
        props: ['id'],
        data() {
            return {
                host: {}
            }
        },
        created() {
            this.LoadHost()
        },
        methods: {
            async LoadHost() {
                this.host = await fetch(
                    `${this.$store.getters.getServerUrl}/host/${this.id}`
                ).then(response => response.json())
                console.log(this.host)
                console.log(this.id)
            },
            goTo(id){
                this.$router.push({
                    name: 'VM',
                    params: {id: id}
                })
            }
        },
    }
</script>

<style scoped>

</style>