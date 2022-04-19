// RoomCalendarBlock测试
import {mount, createLocalVue} from '@vue/test-utils'
import RoomCalendarBlock from '@/components/RoomCalendarBlock.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('RoomCalendarBlock', () => {
  it('should act properly', async () => {
    let wrapper = mount(RoomCalendarBlock, {
      propsData: {
        list: [{
          id: 1,
          name: '111',
          string: '000000000000000000000000000000000000000000000000',
          time_span:
             [ '000000000000000000000000000000000000000000000000',
               '000000000000000000000011000000000000000000000000',
               '000011000000000000000000000000000000000000000000',
               '000000000000000000000000000000000000000000000000',
               '000000023000000000000000000000000000000000000000',
               '000000000000000000000000000000000000000000000000',
               '000000000022000000000000000000000000000000000000'
             ]
        }],
        today: '2021-04-01',
        dayRange: 7
      },
      localVue,
      router
    })
    // 日期按钮
    for (let i = 0; i < 7; i++) {
      await wrapper.findAll('li').at(i).trigger('click')
      expect(wrapper.vm.DateId).toEqual(i)
      expect(wrapper.vm.DateColumn[i].style.backgroundColor).toEqual('#46B8DA')
    }
    await wrapper.findAll('button').at(0).trigger('click')// room跳转
    expect(wrapper.vm.Active).toEqual(true)
    // expect(wrapper.vm.$route.name).toEqual('RoomInfo')
  })
})
