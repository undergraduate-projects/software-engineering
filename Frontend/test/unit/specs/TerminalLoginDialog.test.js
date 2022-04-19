// TerminalLoginDialog测试
import {mount, createLocalVue} from '@vue/test-utils'
import TerminalLoginDialog from '@/components/TerminalLoginDialog.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
// import {readCookie} from '@/utils/cookies.js'
import {terminalData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('Terminal test', () => {
  it('should act properly', async () => {
    // 打开
    let wrapper = mount(TerminalLoginDialog, {
      localVue,
      router
    })

    // watch
    await wrapper.setProps({
      dialogVisible: true
    })
    expect(wrapper.vm.DialogVisible).toEqual(true)

    // Login
    await wrapper.findAll('button').at(2).trigger('click')// 不合法的Login
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// TerminalLogin
      json: async () => (terminalData)
    })
    await wrapper.setData({
      RoomId: '11',
      Token: 't11'
    })
    await wrapper.findAll('button').at(2).trigger('click')// Login
    // expect(wrapper.vm.$route.name).toEqual('Terminal')
    // expect(readCookie('api_token').length).toEqual(3)

    // Cancel
    await wrapper.findAll('button').at(1).trigger('click')// Cancel
    expect(wrapper.vm.RoomId).toEqual('')
    expect(wrapper.vm.Token).toEqual('')
  })
})
