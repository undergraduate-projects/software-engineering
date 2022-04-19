// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import CSOrder from './CSOrder'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import { deleteCookie } from '@/utils/cookies.js'

Vue.use(ElementUI)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#CSOrder',
  router,
  components: {
    CSOrder
  },
  template: '<CSOrder/>'
})

window.onbeforeunload = function () {
  deleteCookie('api_token')
}
