<!--基本文本框-->
<template>
  <label :style="TextBlockStyle">{{ Content }}</label>
</template>

<script>
export default {
  name: 'TextBlock',
  props: {// 主要是可变的css属性
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
    content: {// 内容
      type: String,
      default: () => ''
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
      TextBlockStyle: {// 文本框样式
        width: this.width,
        height: this.height,
        color: this.color,
        backgroundColor: this.backgroundColor,
        fontSize: this.fontSize,
        fontFamily: this.fontFamily,
        display: this.display,
        marginLeft: '10px',
        padding: '0px',
        textAlign: 'left'
      },
      Content: this.content
    }
  },
  watch: {// 动态监听
    width: {
      handler (val) {
        this.TextBlockStyle.width = val
      }
    },
    height: {
      handler (val) {
        this.TextBlockStyle.height = val
      }
    },
    color: {
      handler (val) {
        this.TextBlockStyle.color = val
      }
    },
    backgroundColor: {
      handler (val) {
        this.TextBlockStyle.backgroundColor = val
      }
    },
    fontSize: {
      handler (val) {
        this.TextBlockStyle.fontSize = val
      }
    },
    fontFamily: {
      handler (val) {
        this.TextBlockStyle.fontFamily = val
      }
    },
    display: {
      handler (val) {
        this.TextBlockStyle.display = val
      }
    },
    content: {
      handler (val) {
        this.Content = val
      }
    }
  }
}
</script>

<style scoped>
</style>
