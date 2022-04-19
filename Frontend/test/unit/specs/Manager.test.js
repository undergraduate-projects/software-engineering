// Manager测试
import {mount, createLocalVue} from '@vue/test-utils'
import Manager from '@/views/Manager.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import { setCookie } from '@/utils/cookies.js'
import {tokenData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('Manager test', () => {
  it('should act properly', async () => {
    // 测试打开时接受用户信息
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    let wrapper = mount(Manager, {
      localVue,
      router
    })
    await wrapper.findAll('button').at(0).trigger('click')// ‘用户权限管理’按钮
    expect(wrapper.vm.$route.fullPath).toEqual('/UserPermissionManage')
    await wrapper.findAll('button').at(1).trigger('click')// ‘房间信息管理’按钮
    expect(wrapper.vm.$route.fullPath).toEqual('/RoomInfoManage')
  })
})
