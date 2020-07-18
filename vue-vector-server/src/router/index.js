import Vue from 'vue'
import VueRouter from 'vue-router'
import Host from "../components/Host";
import Virtual from "../components/Virtual";
import Storage from "../components/Storage";
import OperatingSystem from "../components/OperatingSystem";
import DetailHost from "../components/DetailHost";
import Authorization from "../views/Authorization";


Vue.use(VueRouter)

const routes = [
    {
        path: '/list-host',
        name: 'Host',
        component: Host,
    },
    {
        path: '/list-vm',
        name: 'Virtual',
        component: Virtual,
    },
    {
        path: '/list-storage',
        name: 'Storage',
        component: Storage,
    },
    {
        path: '/list-operating-system',
        name: 'OperatingSystem',
        component: OperatingSystem,
    },
    {
        path: '/:id',
        name: 'DetailHost',
        component: DetailHost,
        props: true,
    },
    {
        path: '/',
        name: 'Authorization',
        component: Authorization,
        props: true,
    },
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router
