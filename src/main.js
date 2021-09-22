import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import store from './store'
import Vant from 'vant'
import 'vant/lib/index.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

export const eventBus = new Vue()

Vue.use(Vant)
Vue.use(ElementUI, { size: 'small', zIndex: 3000 })
Vue.config.productionTip = false

new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app')
