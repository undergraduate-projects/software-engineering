<!--基本按钮-->
<template>
  <button @click="click" :style="TextButtonStyle">{{ Content }}</button>
</template>

<script>
export default {
  name: 'TextButton',
  props: {// 主要是可变的css属性
    fontSize: {
      type: String,
      default: () => '25px'
    },
    fontFamily: {
      type: String,
      default: () => 'Arial'
    },
    backgroundColor: {
      type: String,
      default: () => 'transparent'
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
    },
    content: {// 内容
      type: String,
      default: () => ''
    }
  },
  data () {
    return {
      Content: this.content,
      TextButtonStyle: {// 按钮样式
        width: this.width,
        height: this.height,
        color: this.color,
        backgroundColor: this.backgroundColor,
        fontSize: this.fontSize,
        fontFamily: this.fontFamily,
        display: this.display,
        margin: '10px',
        padding: '10px',
        textAlign: 'center',
        borderWidth: '2px',
        borderRadius: '10px',
        borderColor: 'black'
      }
    }
  },
  watch: {// 动态监听
    content: {
      handler (val) {
        this.Content = val
      }
    },
    width: {
      handler (val) {
        this.TextButtonStyle.width = val
      }
    },
    height: {
      handler (val) {
        this.TextButtonStyle.height = val
      }
    },
    color: {
      handler (val) {
        this.TextButtonStyle.color = val
      }
    },
    backgroundColor: {
      handler (val) {
        this.TextButtonStyle.backgroundColor = val
      }
    },
    fontSize: {
      handler (val) {
        this.TextButtonStyle.fontSize = val
      }
    },
    fontFamily: {
      handler (val) {
        this.TextButtonStyle.fontFamily = val
      }
    },
    display: {
      handler (val) {
        this.TextButtonStyle.display = val
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
.TextBlock {
  color: aquamarine;
}
</style>
