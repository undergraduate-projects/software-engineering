// Terminal测试
import {mount, createLocalVue} from '@vue/test-utils'
import Terminal from '@/views/Terminal.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {setCookie} from '@/utils/cookies.js'
import {terminalData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('Terminal test', () => {
  it('should act properly', async () => {
    // 打开时保存信息
    setCookie('terminal_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// TerminalRoomInfo
      json: async () => (terminalData)
    })
    let wrapper = mount(Terminal, {
      localVue,
      router
    })

    // select
    await wrapper.findAll('li').at(12).trigger('click')// 正常
    expect(wrapper.vm.ShowArrive).toEqual(false)
    expect(wrapper.vm.ShowLeave).toEqual(false)
    await wrapper.findAll('li').at(14).trigger('click')// 签退选择
    expect(wrapper.vm.ShowArrive).toEqual(false)
    expect(wrapper.vm.ShowLeave).toEqual(true)
    await wrapper.findAll('li').at(13).trigger('click')// 签到选择
    expect(wrapper.vm.ShowArrive).toEqual(true)
    expect(wrapper.vm.ShowLeave).toEqual(false)

    // button
    // 不进行输入
    await wrapper.findAll('button').at(0).trigger('click')// 签到
    await wrapper.findAll('li').at(14).trigger('click')
    await wrapper.findAll('button').at(0).trigger('click')// 签退
    await wrapper.findAll('li').at(13).trigger('click')

    wrapper.setData({// 输入token
      ArriveToken: '123',
      LeaveToken: '456'
    })
    window.fetch.mockResolvedValueOnce({// TerminalArrive,fail
      json: async () => ({
        code: 400
      })
    })
    await wrapper.findAll('button').at(0).trigger('click')// 签到失败
    window.fetch.mockResolvedValueOnce({// TerminalArrive,success
      json: async () => ({
        code: 200
      })
    })
    await wrapper.findAll('button').at(0).trigger('click')// 签到成功

    await wrapper.findAll('li').at(14).trigger('click')
    window.fetch.mockResolvedValueOnce({// TerminalLeave,fail
      json: async () => ({
        code: 400
      })
    })
    await wrapper.findAll('button').at(1).trigger('click')// 签退失败
    window.fetch.mockResolvedValueOnce({// TerminalLeave,success
      json: async () => ({
        code: 200
      })
    })
    await wrapper.findAll('button').at(1).trigger('click')// 签退成功
  })
})
