// InfoBlock测试
import {mount, createLocalVue} from '@vue/test-utils'
import InfoBlock from '@/components/InfoBlock.vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueRouter)
const router = new VueRouter()

describe('InfoBlock test', () => {
  it('should act properly', async () => {
    let wrapper = mount(InfoBlock, {
      localVue,
      router
    })
    await wrapper.findAll('button').at(0).trigger('click')// ‘返回主页’按钮
    expect(wrapper.vm.$route.fullPath).toEqual('/')
    await wrapper.findAll('button').at(1).trigger('click')// ‘返回主页’按钮
    expect(wrapper.vm.$route.fullPath).toEqual('/')
  })
})
