<template>
    <div class="list-vm">
        <h3>Список виртуальных машин</h3>
        <div v-for="vm in listVM">
            <ul>
                <li><a href="#"><h3>{{ vm.name }}</h3></a>
                    <p v-html="vm.ip"></p>
                    <p v-html="vm.os"></p></li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "listVM",
        data() {
            return {
                listVM: []
            }
        },
        created() {
            this.loadListVM()
        },
        methods: {
            async loadListVM() {
                this.listVM = await fetch(
                    `${this.$store.getters.getServerUrl}/list-vm`
                ).then(response => response.json())
                console.log(this.listVM)
            }
        },
    }

</script>

<style scoped>

</style>