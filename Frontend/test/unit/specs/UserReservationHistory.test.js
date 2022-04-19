import {mount, createLocalVue} from '@vue/test-utils'
import ElementUI from 'element-ui'
import UserReservationHistory from '@/views/UserReservationHistory'
import VueRouter from 'vue-router'
import {tokenData, userReservationData} from './test_data'
import {setCookie} from '@/utils/cookies'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('UserReservationHistory buttons and computed', () => {
  it('should link to funcs', async () => {
    setCookie('api_token', 'test', 1)
    window.fetch = jest.fn()
    window.fetch.mockResolvedValueOnce({// CheckToken
      json: async () => (tokenData)
    })
    window.fetch.mockResolvedValueOnce({// GetRoomInfo
      json: async () => (userReservationData)
    })

    let wrapper = mount(UserReservationHistory, {
      localVue,
      router
    })
    // expect(wrapper.vm.allReservationList).toEqual(userReservationData.data)

    const mock = jest.fn()
    await wrapper.setMethods({
      goToHome: mock,
      handleAsideSelect: mock,
      // handleCurrentChange: mock,
      // getStartTime: mock,
      // getEndTime: mock,
      // isArriveLate: mock,
      // isLeaveLate: mock,
      // isCancelable: mock,
      // isUpcoming: mock,
      // isFulfilled: mock,
      // isRejected: mock,
      // isCancelled: mock,
      // cancelReservation: mock,
      updateResList: mock
    })

    // expect(mock).toHaveBeenCalledTimes(1) // created后调用updateResList
    await wrapper.findAll('li').at(8).trigger('click') // 返回首页
    // expect(mock).toHaveBeenCalledTimes(1)
    expect(wrapper.vm.$route.fullPath).toEqual('/')

    // wrapper.setData(
    //   {
    //     allReservationList: userReservationData['data'],
    //     dishonestReservationList: userReservationData['data'].slice(0, 3),
    //     fulfilledReservationList: userReservationData['data'].slice(0, 3),
    //     upcomingReservationList: userReservationData['data'].slice(0, 3),
    //     cancelledReservationList: userReservationData['data'].slice(0, 3),
    //     rejectedReservationList: userReservationData['data'].slice(0, 3)
    //   }
    // )
    /* let menus = wrapper.findAll('.el-menu-item')
    let allMenu = menus.at(0)
    await allMenu.trigger('click') // 显示全部预约记录
    expect(allMenu.text()).toEqual('全部预约')
    expect(wrapper.vm.activeListIndex).toEqual(0)
    expect(wrapper.vm.activePageNum).toEqual(1)
    expect(wrapper.vm.activeList).toEqual(wrapper.vm.allReservationList)
    expect(mock).toHaveBeenCalledTimes(2)
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(10)

    let fulfilledMenu = menus.at(1)
    await fulfilledMenu.trigger('click') // 显示已使用预约记录
    expect(fulfilledMenu.text()).toEqual('已使用预约')
    expect(wrapper.vm.activeList).toEqual(wrapper.vm.fulfilledReservationList)
    // expect(wrapper.vm.activeListIndex).toEqual(1)
    expect(wrapper.vm.activePageNum).toEqual(1)
    expect(mock).toHaveBeenCalledTimes(3)
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(4)

    // expect(wrapper.vm.activeListIndex).toEqual(2)
    let upcomingMenu = menus.at(2)
    await upcomingMenu.trigger('click') // 显示未使用预约记录
    expect(upcomingMenu.text()).toEqual('未使用预约')
    expect(wrapper.vm.activePageNum).toEqual(1)
    expect(wrapper.vm.activeList).toEqual(wrapper.vm.upcomingReservationList)
    expect(mock).toHaveBeenCalledTimes(4)
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(4)

    // expect(wrapper.vm.activeListIndex).toEqual(3)
    let cancelMenu = menus.at(3)
    await cancelMenu.trigger('click') // 显示取消记录
    expect(cancelMenu.text()).toEqual('预约取消记录')
    expect(wrapper.vm.activePageNum).toEqual(1)
    // expect(wrapper.vm.activeList).toEqual(wrapper.vm.cancelledReservationList)
    expect(mock).toHaveBeenCalledTimes(6) // 为什么到这里会调用updateList?神奇的Jest
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(4)

    // expect(wrapper.vm.activeListIndex).toEqual(4)
    let failMenu = menus.at(4)
    await failMenu.trigger('click') // 显示预约失败记录
    expect(failMenu.text()).toEqual('预约失败记录')
    expect(wrapper.vm.activePageNum).toEqual(1)
    expect(wrapper.vm.activeList).toEqual(wrapper.vm.rejectedReservationList)
    expect(mock).toHaveBeenCalledTimes(7)
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(4)

    // expect(wrapper.vm.activeListIndex).toEqual(5)
    let dishonestMenu = menus.at(5)
    await dishonestMenu.trigger('click') // 显示违约记录
    expect(dishonestMenu.text()).toEqual('违约记录')
    expect(wrapper.vm.activePageNum).toEqual(1)
    expect(wrapper.vm.activeList).toEqual(wrapper.vm.dishonestReservationList)
    expect(mock).toHaveBeenCalledTimes(8)
    // expect(wrapper.vm.activeListSliceStart).toEqual(0)
    // expect(wrapper.vm.activeListSliceStart).toEqual(4) */
  })
})
