<template>
    <section id="sidebar">
        <div class="inner">
            <nav>
                <ul>
                    <li><router-link to="/list-host">Hosts</router-link></li>
                    <li><router-link to="/list-vm">Virtual machines</router-link></li>
                    <li><router-link to="/list-storage">Storages</router-link></li>
                    <li><router-link to="/list-operating-system">Operating systems</router-link></li>
                </ul>
            </nav>
        </div>
    </section>
</template>

<script>
    export default {
        name: "Nav"
    }
</script>

<style scoped>

</style>