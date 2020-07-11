import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ListVM from "../views/ListVM";
import ListStorage from "../views/ListStorage";
import ListOS from "../views/ListOS";
import Host from "../views/Host";
import VM from "../views/VM";
import Storage from "../views/Storage";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/list-vm',
        name: 'ListVM',
        component: ListVM,
    },
    {
        path: '/storage/:id',
        name: 'Storage',
        component: Storage,
        props: true,
    },
    {
        path: '/vm/:id',
        name: 'VM',
        component: VM,
        props: true,
    },
    {
        path: '/host/:id',
        name: 'Host',
        component: Host,
        props: true,
    },
    {
        path: '/list-storage',
        name: 'ListStorage',
        component: ListStorage,
    },
    {
        path: '/list-os',
        name: 'ListOS',
        component: ListOS,
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router
