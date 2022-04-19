<template>
  <div id="CSOrder">
    <router-view v-if="Show" />
  </div>
</template>

<script>

export default {
  name: 'CSOrder',
  data () {
    return {
      Show: true
    }
  },
  provide () { // 父组件中通过provide来提供变量，在子组件中通过inject来注入变量。
    return {
      PageReload: this.Reload
    }
  },
  methods: {
    Reload () {
      this.Show = false // 关闭
      this.$nextTick(function () {
        this.Show = true // 打开
      })
    }
  },
  mounted () {
    document.onkeydown = function (event) {
      if (event.keyCode === 116 || (event.ctrlKey && event.keyCode === 82)) { // 禁用刷新
        event.preventDefault()
        event.keyCode = 0
        event.returnValue = false
        return false
      }
    }
    document.oncontextmenu = function () { // 禁用右键菜单
      return false
    }
  }
}
</script>

<style>
body {
  margin: 0;
}
</style>
