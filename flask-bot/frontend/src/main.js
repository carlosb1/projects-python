import Vue from 'vue'
import App from './App'
import router from './router'
import VueSocketio from 'vue-socket.io'

Vue.use(new VueSocketio({connection: 'http://0.0.0.0:5004'}))
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
