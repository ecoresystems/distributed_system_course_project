import Vue from 'vue'
import ElementUI from 'element-ui'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'

Vue.use(ElementUI)
Vue.use(axios)
Vue.prototype.$axios = axios

new Vue({
  el: '#app',
  render: h => h(App)
})
