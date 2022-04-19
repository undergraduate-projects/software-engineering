// Index测试
import {mount, createLocalVue} from '@vue/test-utils'
import Index from '@/views/Index.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {setCookie} from '@/utils/cookies.js'
import {userInfoData, tokenData, userReservationData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()
describe('Index test', () => {
  it('should act properly', async () => {
    // 打开
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetUserInfo
      json: async () => (userInfoData)
    })
    window.fetch.mockResolvedValueOnce({// GetUserReservation
      json: async () => (userReservationData)
    })

    let wrapper = mount(Index, {
      localVue,
      router
    })

    // url跳转及内容变化
    await wrapper.findAll('li').at(2).trigger('click')// 登录
    await wrapper.findAll('li').at(3).trigger('click')// 会议室公共终端
    expect(wrapper.vm.DialogVisible).toEqual(true)
    await wrapper.findAll('li').at(4).trigger('click')// 会议室列表
    // expect(wrapper.vm.$route.fullPath).toEqual('/RoomReserve')
    await wrapper.findAll('li').at(5).trigger('click')// 预约列表
    expect(wrapper.vm.$route.fullPath).toEqual('/UserReservationHistory')
    await wrapper.findAll('li').at(6).trigger('click')// 个人信息管理
    expect(wrapper.vm.$route.fullPath).toEqual('/Info')

    await wrapper.findAll('li').at(7).trigger('click')// 预约审批
    expect(wrapper.vm.$route.fullPath).toEqual('/RoomExamine')
    await wrapper.findAll('li').at(8).trigger('click')// 用户权限管理
    expect(wrapper.vm.$route.fullPath).toEqual('/UserPermissionManage')
    await wrapper.findAll('li').at(9).trigger('click')// 房间信息管理
    expect(wrapper.vm.$route.fullPath).toEqual('/RoomInfoManage')

    window.fetch.mockResolvedValueOnce({// Logout
      json: async () => (tokenData)
    })
    await wrapper.findAll('li').at(10).trigger('click')// 退出登录
    // expect(readCookie('api_token')).toEqual('')
    // await wrapper.findAll('li').at(8).trigger('click')// 返回主页
  })
})
