// 该单元测试文件生成各种组件的快照，并在下一刻将得到的html与之比对，以确认组件渲染正确
import {mount, createLocalVue} from '@vue/test-utils'
import Index from '@/views/Index.vue'
import LoginRedirect from '@/views/LoginRedirect.vue'
import Info from '@/views/Info.vue'
import Manager from '@/views/Manager.vue'
import NaviBar from '@/components/NaviBar.vue'
import InfoBlock from '@/components/InfoBlock.vue'
import RadioInput from '@/components/RadioInput.vue'
import TextInput from '@/components/TextInput.vue'
import TextButton from '@/components/TextButton.vue'
import TextBlock from '@/components/TextBlock.vue'
import RoomReserve from '@/views/RoomReserve.vue'
import RoomInfo from '@/views/RoomInfo.vue'
import RoomCalendarBlock from '@/components/RoomCalendarBlock.vue'
import RoomCalendarLine from '@/components/RoomCalendarLine.vue'
import UserPermissionManage from '@/views/UserPermissionManage.vue'
import UserReservationHistory from '@/views/UserReservationHistory.vue'
import CollapsePanel from '@/components/CollapsePanel.vue'

import ElementUI from 'element-ui'
import VueRouter from 'vue-router'
const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('Index.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(Index, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})

describe('LoginRedirect.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(LoginRedirect, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})

describe('Info.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(Info, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('Manager.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(Manager, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('NaviBar.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(NaviBar, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('InfoBlock.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(InfoBlock, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})

describe('RadioInput.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(RadioInput, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})

describe('TextInput.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(TextInput, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('TextButton.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(TextButton, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('TextBlock.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(TextBlock, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('RoomReserve.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(RoomReserve, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('RoomCalendarBlock.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(RoomCalendarBlock, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('RoomCalendarLine.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(RoomCalendarLine, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('UserPermissionManage.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(UserPermissionManage, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('RoomInfo.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(RoomInfo, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('UserReservationHistory.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(UserReservationHistory, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
describe('CollapsePanel.vue', () => {
  it('should match snapshot', async () => {
    const wrapper = mount(CollapsePanel, {
      localVue,
      router
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toMatchSnapshot()
  })
})
