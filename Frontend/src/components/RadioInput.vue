<!--基本输入框-->
<template>
  <label
    ><input
      type="radio"
      :style="RadioInputStyle"
      :name="Name"
      @click="click"
    />{{ Content }}</label
  >
</template>

<script>
export default {
  name: 'RadioInput',
  props: {// 主要是可变的css属性
    name: {// 绑定一组单选框
      type: String,
      default: () => ''
    },
    content: {// 显示的文本内容
      type: String,
      default: () => ''
    },
    backgroundColor: {
      type: String,
      default: () => 'transparent'
    },
    fontSize: {
      type: String,
      default: () => '25px'
    },
    fontFamily: {
      type: String,
      default: () => 'Arial'
    },
    color: {
      type: String,
      default: () => 'black'
    },
    width: {
      type: String,
      default: () => 'auto'
    },
    height: {
      type: String,
      default: () => 'auto'
    },
    display: {
      type: String,
      default: () => 'inline-block'
    }
  },
  data () {
    return {
      RadioInputStyle: {// 输入框样式
        width: this.width,
        height: this.height,
        color: this.color,
        backgroundColor: this.backgroundColor,
        fontSize: this.fontSize,
        fontFamily: this.fontFamily,
        display: this.display,
        margin: '10px',
        padding: '10px',
        textAlign: 'center'
      },
      Name: this.name,
      Content: this.content
    }
  },
  watch: {// 动态监听
    width: {
      handler (val) {
        this.RadioInputStyle.width = val
      }
    },
    height: {
      handler (val) {
        this.RadioInputStyle.height = val
      }
    },
    color: {
      handler (val) {
        this.RadioInputStyle.color = val
      }
    },
    backgroundColor: {
      handler (val) {
        this.RadioInputStyle.backgroundColor = val
      }
    },
    fontSize: {
      handler (val) {
        this.RadioInputStyle.fontSize = val
      }
    },
    fontFamily: {
      handler (val) {
        this.RadioInputStyle.fontFamily = val
      }
    },
    display: {
      handler (val) {
        this.RadioInputStyle.display = val
      }
    },
    name: {
      handler (val) {
        this.Name = val
      }
    },
    content: {
      handler (val) {
        this.Content = val
      }
    }
  },
  methods: {
    click: function () {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
</style>
