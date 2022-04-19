// Info测试
import {mount, createLocalVue} from '@vue/test-utils'
import Info from '@/views/Info.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {setCookie} from '@/utils/cookies.js'
import {userInfoData, tokenData, saveData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('Info test', () => {
  it('should act properly', async () => {
    // 打开时保存信息
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetUserInfo
      json: async () => (userInfoData)
    })
    let wrapper = mount(Info, {
      localVue,
      router
    })

    // 跳转url
    await wrapper.findAll('button').at(0).trigger('click')// 返回主页
    expect(wrapper.vm.$route.fullPath).toEqual('/')

    // 保存信息
    window.fetch.mockResolvedValueOnce({// Save
      json: async () => (saveData)
    })
    await wrapper.findAll('button').at(1).trigger('click')// 保存信息
    // TODO
  })
})
