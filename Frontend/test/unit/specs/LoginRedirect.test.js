// LoginRedirect测试
import {mount, createLocalVue} from '@vue/test-utils'
import LoginRedirect from '@/views/LoginRedirect.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {loginRedirectData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('LoginRedirect test', () => {
  it('should act properly', async () => {
    // 打开
    Object.defineProperty(window, 'location', {// 模拟跳转页的url
      value: new URL('http://localhost:8081/loginredirect/?code=efe0w3chn4t&state=a_try')
    })
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// Login
      json: async () => (loginRedirectData)
    })
    let wrapper = mount(LoginRedirect, {
      localVue,
      router
    })

    // 检查信息
    expect(wrapper.vm.$route.fullPath).toEqual('/')
    // expect(readCookie('api_token')).toEqual('test')
  })
})
