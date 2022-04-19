// RoomInfo测试
import {mount, createLocalVue} from '@vue/test-utils'
import RoomInfo from '@/views/RoomInfo.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {setCookie} from '@/utils/cookies.js'
import {roomInfoData, tokenData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('RoomInfo test', () => {
  it('should act properly', async () => {
    // 打开时保存信息
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetRoomInfo
      json: async () => (roomInfoData)
    })
    let wrapper = mount(RoomInfo, {
      localVue,
      router
    })

    // 跳转url
    await wrapper.findAll('li').at(0).trigger('click')// 返回主页
  })
})
