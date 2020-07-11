import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store( {
    mutations: {},
    state: {
        backendUrl: "http://127.0.0.1:8000/api"
    },
    actions: {},
    modules: {},
    getters: {
        getServerUrl: state => {
             return state.backendUrl
        }
    },
})

export default store