// UserPermissionManage测试
import {mount, createLocalVue} from '@vue/test-utils'
import UserPermissionManage from '@/views/UserPermissionManage.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import { setCookie } from '@/utils/cookies.js'
import {tokenData, userInfoData} from './test_data.js'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('UserPermissionManage test', () => {
  it('should act properly', async () => {
    // 测试打开时接受用户信息
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetUserInfo
      json: async () => (userInfoData)
    })
    let wrapper = mount(UserPermissionManage, {
      localVue,
      router
    })

    await wrapper.findAll('button').at(0).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(1).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.only).toEqual({'institute': [], 'name_uid_contain': '', 'role': []})

    await wrapper.findAll('button').at(2).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.only).toEqual({'institute': [], 'name_uid_contain': '', 'role': []})

    await wrapper.findAll('button').at(3).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(4).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    /* await wrapper.findAll('button').at(5).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid') */

    /* await wrapper.findAll('button').at(7).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(8).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(9).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(10).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(11).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(12).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid')

    await wrapper.findAll('button').at(13).trigger('click')// 按 uid 排序按钮
    expect(wrapper.vm.orderBy).toEqual('uid') */

    // 筛选
    /* let radios = wrapper.findAll({ name: 'el-radio' })
    // 按姓名和学号排序
    radios.at(0).trigger('click')
    expect(wrapper.vm.orderBy).toEqual('uid')
    radios.at(1).trigger('click')
    expect(wrapper.vm.orderBy).toEqual('fullname')
    /*
    // 按角色分类
    radios.at(2).trigger('click')
    expect(wrapper.vm.only).toEqual('')
    radios.at(3).trigger('click')
    expect(wrapper.vm.only).toEqual('role:U;')
    radios.at(4).trigger('click')
    expect(wrapper.vm.only).toEqual('role:DA;')
    radios.at(5).trigger('click')
    expect(wrapper.vm.only).toEqual('role:IA;')
    radios.at(6).trigger('click')
    expect(wrapper.vm.only).toEqual('role:R;')

    // 按研究所分类
    radios.at(7).trigger('click')
    expect(wrapper.vm.i_only).toEqual('')
    radios.at(8).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:1')
    radios.at(9).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:2')
    radios.at(10).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:3')
    radios.at(11).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:4')
    radios.at(12).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:5')
    radios.at(13).trigger('click')
    expect(wrapper.vm.i_only).toEqual('institute:6') */
  })
})
