// CollapsePanel测试
import {mount, createLocalVue} from '@vue/test-utils'
import ElementUI from 'element-ui'
import CollapsePanel from '@/components/CollapsePanel'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('CollapsePanel buttons and computed', () => {
  it('should link to funcs', async () => {
    const mock = jest.fn()
    let wrapper = mount(CollapsePanel, {
      localVue,
      router
    })
    await wrapper.setMethods({
      handleCollapse: mock,
      cancelReservation: mock
    })
    await wrapper.findAll('.el-button').at(0).trigger('click') // 打开面板
    expect(mock).toHaveBeenCalledTimes(1)
    expect(wrapper.vm.isCollapsed).toEqual(true)
    await wrapper.setData({
      isCollapsed: false
    })
    await wrapper.findAll('.el-button').at(0).trigger('click') // 如果上边一条指令还起作用，则为关闭面板
    expect(mock).toHaveBeenCalledTimes(2)
    expect(wrapper.vm.isCollapsed).toEqual(false)

    let curDate = new Date()
    let nextDate = new Date(curDate.getTime() + 48 * 60 * 60 * 1000) // 后天
    await wrapper.setProps({
      resInfo: {
        submitTime: curDate.getTime() - 48 * 60 * 60 * 1000,
        room: {
          name: '301',
          building: 'New Building',
          floor: ''
        },
        applicant: '王小帅',
        date: nextDate.toLocaleDateString(),
        approvalTime: curDate.getTime() - 24 * 60 * 60 * 1000,
        approvalResult: true,
        approvalPerson: 'XXX',
        arrivalTime: '',
        leaveTime: '',
        reason: '这是一段理由',
        cancelTime: null,
        id: '',
        timeSpan: '001111'.padEnd(48, '0')
      }
    })
    expect(wrapper.vm.stepActiveIndex).toEqual(2) // 待使用状态
    // expect(wrapper.vm.finalStepStatus).toEqual('wait')
    expect(wrapper.vm.hasBeenApproved).toEqual(true)
    // expect(wrapper.vm.approvalResultString).toEqual('通过审批')
    expect(wrapper.vm.startTime).toEqual(new Date(nextDate.toLocaleDateString()).getTime() + (2 - 16) * 30 * 60 * 1000)
    expect(wrapper.vm.endTime).toEqual(new Date(nextDate.toLocaleDateString()).getTime() + (6 - 16) * 30 * 60 * 1000)
    expect(wrapper.vm.approvalResultBgColor).toEqual('#1abc9c')
    expect(wrapper.vm.cancelable).toEqual(true)

    let startTimeString = new Date(new Date(nextDate.toLocaleDateString()).getTime() + (2 - 16) * 30 * 60 * 1000).toLocaleTimeString()
    let endTimeString = new Date(new Date(nextDate.toLocaleDateString()).getTime() + (6 - 16) * 30 * 60 * 1000).toLocaleTimeString()
    expect(wrapper.vm.timeSpanString).toEqual(startTimeString + ' - ' + endTimeString)

    await wrapper.findAll('.el-button').at(1).trigger('click') // 取消预约
    expect(mock).toHaveBeenCalledTimes(3)

    await wrapper.setProps({
      resInfo: {
        submitTime: curDate.getTime() - 48 * 60 * 60 * 1000,
        room: {
          name: '301',
          building: 'New Building',
          floor: ''
        },
        applicant: '王小帅',
        date: nextDate.toLocaleDateString(),
        approvalTime: curDate.getTime() - 24 * 60 * 60 * 1000,
        approvalResult: true,
        approvalPerson: 'XXX',
        arrivalTime: new Date(nextDate.toLocaleDateString()).getTime() + 3 * 30 * 60 * 1000,
        leaveTime: new Date(nextDate.toLocaleDateString()).getTime() + 6 * 30 * 60 * 1000,
        reason: '这是一段理由',
        cancelTime: '',
        id: '',
        timeSpan: '001111'.padEnd(48, '0')
      }
    })
    expect(wrapper.vm.arriveLate).toEqual(true)
    expect(wrapper.vm.leaveLate).toEqual(true)
    expect(wrapper.vm.stepActiveIndex).toEqual(3) // 使用完毕
    // expect(wrapper.vm.finalStepStatus).toEqual('error')
  })
})
