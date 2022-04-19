// RoomReserve测试
import {mount, createLocalVue} from '@vue/test-utils'
import RoomReserve from '@/views/RoomReserve.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import {setCookie} from '@/utils/cookies.js'
import {tokenData, roomListData} from './test_data.js'
import {triggerTextButton} from './utils.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('RoomReserve test', () => {
  it('should act properly', async () => {
    // 测试打开时接受用户信息
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetRoomList
      json: async () => (roomListData)
    })
    let wrapper = mount(RoomReserve, {
      localVue,
      router
    })

    // 测试查询教室
    await wrapper.setData({// 设置Data
      FullList: roomListData.data.room_list
    })
    window.alert = jest.fn()
    triggerTextButton(wrapper, '确 定')
    await wrapper.setData({
      Search: {
        method: 'name', // 按名字筛选
        name: 'test'// 错误的名字
      }
    })
    triggerTextButton(wrapper, '确 定')

    await wrapper.setData({
      Search: {
        method: 'name', // 按名字筛选
        name: '会议室211'// 正确的名字
      }
    })
    triggerTextButton(wrapper, '确 定')
    await wrapper.setData({
      Search: {
        method: 'id', // 按id筛选
        id: 'test'// 错误的id
      }
    })
    triggerTextButton(wrapper, '确 定')
    await wrapper.setData({
      Search: {
        method: 'id', // 按id筛选
        id: '11'// 正确的id
      }
    })
    triggerTextButton(wrapper, '确 定')

    // 测试筛选
    let menus = wrapper.findAll({name: 'el-menu-item'})
    let k = -1
    for (let i = 0; i < menus.length; i++) {
      if (menus.at(i).text() === '全部') {
        k = i
        break
      }
    }
    menus.at(k - 1).trigger('click')// do nothing
    menus.at(k).trigger('click')// 取消筛选
    expect(wrapper.vm.SizeType).toEqual('')
    expect(wrapper.vm.BuildingType).toEqual('')
    expect(wrapper.vm.FloorType).toEqual('')
    expect(wrapper.vm.InstituteType).toEqual('')
    // SizeType
    menus.at(k + 1).trigger('click')
    expect(wrapper.vm.SizeType).toEqual('s')
    menus.at(k + 2).trigger('click')
    expect(wrapper.vm.SizeType).toEqual('m')
    menus.at(k + 3).trigger('click')
    expect(wrapper.vm.SizeType).toEqual('l')
    menus.at(k).trigger('click')// 取消筛选
    // BuildingType
    menus.at(k + 4).trigger('click')
    expect(wrapper.vm.BuildingType).toEqual('newbuilding')
    menus.at(k + 5).trigger('click')
    expect(wrapper.vm.BuildingType).toEqual('eastprime')
    menus.at(k).trigger('click')// 取消筛选
    // FloorType
    menus.at(k + 6).trigger('click')
    expect(wrapper.vm.FloorType).toEqual('1')
    menus.at(k + 7).trigger('click')
    expect(wrapper.vm.FloorType).toEqual('2')
    menus.at(k + 8).trigger('click')
    expect(wrapper.vm.FloorType).toEqual('3')
    menus.at(k).trigger('click')// 取消筛选
    // InstituteType
    menus.at(k + 9).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('1')
    menus.at(k + 10).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('2')
    menus.at(k + 11).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('3')
    menus.at(k + 12).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('4')
    menus.at(k + 13).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('5')
    menus.at(k + 14).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('6')
    menus.at(k + 15).trigger('click')
    expect(wrapper.vm.InstituteType).toEqual('7')
    menus.at(k).trigger('click')// 取消筛选
  })
})
