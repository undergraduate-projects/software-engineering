<!--基本输入框-->
<template>
  <input :style="TextInputStyle" :placeholder="Placeholder" :id="Id" />
</template>

<script>
export default {
  name: 'TextInput',
  props: {// 主要是可变的css属性
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
    backgroundColor: {
      type: String,
      default: () => 'transparent'
    },
    fontSize: {
      type: String,
      default: () => '20px'
    },
    fontFamily: {
      type: String,
      default: () => 'Arial'
    },
    color: {
      type: String,
      default: () => 'black'
    },
    id: {// 通过id来获取内容
      type: String,
      default: () => ''
    },
    placeholder: {
      type: String,
      default: () => ''
    }
  },
  data () {
    return {
      TextInputStyle: {// 输入框样式
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
      Placeholder: this.placeholder,
      Id: this.id
    }
  },
  watch: {// 动态监听
    width: {
      handler (val) {
        this.TextInputStyle.width = val
      }
    },
    height: {
      handler (val) {
        this.TextInputStyle.height = val
      }
    },
    color: {
      handler (val) {
        this.TextInputStyle.color = val
      }
    },
    backgroundColor: {
      handler (val) {
        this.TextInputStyle.backgroundColor = val
      }
    },
    fontSize: {
      handler (val) {
        this.TextInputStyle.fontSize = val
      }
    },
    fontFamily: {
      handler (val) {
        this.TextInputStyle.fontFamily = val
      }
    },
    display: {
      handler (val) {
        this.TextInputStyle.display = val
      }
    },
    placeholder: {
      handler (val) {
        this.Placeholder = val
      }
    },
    id: {
      handler (val) {
        this.Id = val
      }
    }
  }
}
</script>

<style scoped>
</style>
