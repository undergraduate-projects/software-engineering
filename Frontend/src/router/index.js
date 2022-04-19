import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index.vue'
import Info from '@/views/Info.vue'
import Manager from '@/views/Manager.vue'
import RoomInfoManage from '@/views/RoomInfoManage.vue'
import UserPermissionManage from '@/views/UserPermissionManage.vue'
import LoginRedirect from '@/views/LoginRedirect.vue'
import RoomReserve from '@/views/RoomReserve.vue'
import RoomInfo from '@/views/RoomInfo.vue'
import UserReservationHistory from '@/views/UserReservationHistory.vue'
import RoomExamine from '@/views/RoomExamine.vue'
import Terminal from '@/views/Terminal.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/Info',
      name: 'Info',
      component: Info
    },
    {
      path: '/loginredirect',
      name: 'LoginRedirect',
      component: LoginRedirect
    },
    {
      path: '/Manager',
      name: 'Manager',
      component: Manager
    },
    {
      path: '/RoomInfoManage',
      name: 'RoomInfoManage',
      component: RoomInfoManage
    },
    {
      path: '/UserPermissionManage',
      name: 'UserPermissionManage',
      component: UserPermissionManage
    },
    {
      path: '/RoomReserve',
      name: 'RoomReserve',
      component: RoomReserve
    },
    {
      path: '/RoomInfo',
      name: 'RoomInfo',
      component: RoomInfo
    },
    {
      path: '/UserReservationHistory',
      name: 'UserReservationHistory',
      component: UserReservationHistory
    },
    {
      path: '/RoomExamine',
      name: 'RoomExamine',
      component: RoomExamine
    },
    {
      path: '/Terminal',
      name: 'Terminal',
      component: Terminal
    }
  ]
})
