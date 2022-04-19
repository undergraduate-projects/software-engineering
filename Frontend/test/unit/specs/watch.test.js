// 该单元测试文件对组件中的属性进行修改，并确认监听器能够正常检测其变化
import TextBlock from '@/components/TextBlock.vue'
import TextInput from '@/components/TextInput.vue'
import TextButton from '@/components/TextButton.vue'
import RadioInput from '@/components/RadioInput.vue'
import RoomCalendarBlock from '@/components/RoomCalendarBlock.vue'
import RoomCalendarLine from '@/components/RoomCalendarLine.vue'
import {mount, createLocalVue} from '@vue/test-utils'

import ElementUI from 'element-ui'
import VueRouter from 'vue-router'
const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('watch TextBlock', () => { // TextBlock的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(TextBlock, {
      propsData: {
        content: '111',
        width: '50px',
        height: '50px',
        color: 'transparent',
        backgroundColor: 'transparent',
        fontSize: '20px',
        fontFamily: 'Arial',
        display: 'inline-block'
      }
    })
    let newprop = {
      content: '222',
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex'
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.Content).toEqual('222')// Content变化
    expect(wrapper.vm.TextBlockStyle).toEqual({// style变化
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex',
      marginLeft: '10px',
      padding: '0px',
      textAlign: 'left'
    })
  })
})

describe('watch TextInput', () => { // TextInput的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(TextInput, {
      propsData: {
        id: '1',
        placeholder: '111',
        width: '50px',
        height: '50px',
        color: 'transparent',
        backgroundColor: 'transparent',
        fontSize: '20px',
        fontFamily: 'Arial',
        display: 'inline-block'
      }
    })
    let newprop = {
      id: '2',
      placeholder: '222',
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex'
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.Id).toEqual('2')// Id变化
    expect(wrapper.vm.Placeholder).toEqual('222')// Placeholder变化
    expect(wrapper.vm.TextInputStyle).toEqual({// style变化
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex',
      margin: '10px',
      padding: '10px',
      textAlign: 'center'
    })
  })
})

describe('watch TextButton', () => { // TextButton的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(TextButton, {
      propsData: {
        content: '111',
        width: '50px',
        height: '50px',
        color: 'transparent',
        backgroundColor: 'transparent',
        fontSize: '20px',
        fontFamily: 'Arial',
        display: 'inline-block'
      }
    })
    let newprop = {
      content: '222',
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex'
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.Content).toEqual('222')// Content变化
    expect(wrapper.vm.TextButtonStyle).toEqual({// style变化
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex',
      margin: '10px',
      padding: '10px',
      textAlign: 'center',
      borderWidth: '2px',
      borderRadius: '10px',
      borderColor: 'black'
    })
  })
})

describe('watch RadioInput', () => { // RadioInput的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(RadioInput, {
      propsData: {
        name: '1',
        content: '111',
        width: '50px',
        height: '50px',
        color: 'transparent',
        backgroundColor: 'transparent',
        fontSize: '20px',
        fontFamily: 'Arial',
        display: 'inline-block'
      }
    })
    let newprop = {
      name: '2',
      content: '222',
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex'
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.Name).toEqual('2')// Name变化
    expect(wrapper.vm.Content).toEqual('222')// Content变化
    expect(wrapper.vm.RadioInputStyle).toEqual({// style变化
      width: '60px',
      height: '60px',
      color: 'blue',
      backgroundColor: 'blue',
      fontSize: '30px',
      fontFamily: 'Helvetica',
      display: 'flex',
      margin: '10px',
      padding: '10px',
      textAlign: 'center'
    })
  })
})

describe('watch RoomCalendarBlock', () => { // RoomCalendarBlock的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(RoomCalendarBlock, {
      propsData: {
        list: [{
          id: 1,
          name: '111',
          string: '000000000000000000000000000000000000000000000000'
        }],
        today: '2020-04-01',
        dayRange: 7,
        active: false
      }
    })
    let newprop = {
      list: [{
        id: 2,
        name: '222',
        string: '111100000000000000000000000000000000000000000000'
      }],
      today: '2020-02-28', // 闰年二月
      dayRange: 14, // 14天,
      active: true// 激活
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.List).toEqual([{// List变化
      id: 2,
      name: '222',
      string: '111100000000000000000000000000000000000000000000'
    }])
    expect(wrapper.vm.Today).toEqual('2020-02-28')// 日期变化
    expect(wrapper.vm.dayRange).toEqual(14)// 时间段变化
    expect(wrapper.vm.Active).toEqual(true)// 时间段变化
    // 日期变化
    expect(wrapper.vm.DateColumn[0].content).toEqual('2月28日')
    expect(wrapper.vm.DateColumn[1].content).toEqual('3月1日')
    expect(wrapper.vm.DateColumn[2].content).toEqual('3月2日')
    expect(wrapper.vm.DateColumn[3].content).toEqual('3月3日')
    expect(wrapper.vm.DateColumn[4].content).toEqual('3月4日')
    expect(wrapper.vm.DateColumn[5].content).toEqual('3月5日')
    expect(wrapper.vm.DateColumn[6].content).toEqual('3月6日')
    expect(wrapper.vm.DateColumn[7].content).toEqual('3月7日')
    expect(wrapper.vm.DateColumn[8].content).toEqual('3月8日')
    expect(wrapper.vm.DateColumn[9].content).toEqual('3月9日')
    expect(wrapper.vm.DateColumn[10].content).toEqual('3月10日')
    expect(wrapper.vm.DateColumn[11].content).toEqual('3月11日')
    expect(wrapper.vm.DateColumn[12].content).toEqual('3月12日')
    expect(wrapper.vm.DateColumn[13].content).toEqual('3月13日')
    expect(wrapper.vm.DateColumn[0].style.backgroundColor).toEqual('#46B8DA')// 颜色

    // 以下覆盖各种日期
    await wrapper.setData({
      DateId: 1
    })
    await wrapper.setProps({today: '2021-02-28'})// 非闰年二月
    expect(wrapper.vm.DateColumn[0].style.backgroundColor).toEqual('#eeeeee')// 颜色变化
    expect(wrapper.vm.DateColumn[1].content).toEqual('2月29日')
    expect(wrapper.vm.DateColumn[2].content).toEqual('3月1日')

    await wrapper.setProps({today: '2021-04-30'})// 小月
    expect(wrapper.vm.DateColumn[1].content).toEqual('5月1日')

    await wrapper.setProps({today: '2021-12-31'})// 跨年
    expect(wrapper.vm.DateColumn[1].content).toEqual('1月1日')
  })
})

describe('watch RoomCalendarLine', () => { // RoomCalendarLine的监听测试
  it('Data should render according to the props', async () => {
    // 加载
    let wrapper = mount(RoomCalendarLine, {
      router,
      localVue,
      propsData: {
        name: '111',
        string: '000000000000000000000000000000000000000000000000'
      }
    })

    let newprop = {
      name: '222',
      string: '000000000000000001231000000000000000000000000000'
    }
    await wrapper.setProps(newprop)// prop变化
    // 检测Data变化
    expect(wrapper.vm.Name).toEqual('222')// Name变化
    // String变化而导致的颜色变化
    expect(wrapper.vm.Column[0].style.backgroundColor).toEqual('#ffffff')
    expect(wrapper.vm.Column[1].style.backgroundColor).toEqual('#eeeeee')
    expect(wrapper.vm.Column[3].style.backgroundColor).toEqual('#F8C471')
    expect(wrapper.vm.Column[2].style.backgroundColor).toEqual('#94DC5A')
  })
})
