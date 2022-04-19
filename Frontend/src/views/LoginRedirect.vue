<template>
  <!-- 本页面为用户在主页点击登陆后，进行酒井OAuth验证的重定向网页 -->
  <div>
    <h3 id="loginRedirect">正在登录...</h3>
  </div>
</template>

<script>

import { Login } from '@/utils/communication'

export default {
  name: 'LoginRedirect',
  created () {
    let LOCALHOST = process.env.NODE_ENV === 'development'
      ? 'http://localhost:8081' : 'https://frontend-antijuan.app.secoder.net'// 自动检测环境以配置LOCALHOST
    let reg = new RegExp('(code=)' + '([^&]*)' + '(&)')

    // 从url中获取auth code
    let authCode = location.href.match(reg)
    if (authCode && authCode.length >= 1) {
      Login(authCode[2], LOCALHOST + '/loginredirect/').then((res) => {
        if (res['result'] === 'success') {
          this.setCookie('api_token', res['api_token'])
          // OAuth验证成功后，重定向到主页
          this.$router.push('/')
          this.$message({
            type: 'success',
            message: '登录成功!',
            duration: 1000
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '登录失败，请重新登录!',
          duration: 3000
        })
        document.getElementById('loginRedirect').innerText = '登录失败，正在返回主页...'
        setInterval(() => {
          this.$router.push('/')
        }, 2000)
      })
    }
  },
  methods: {
    setCookie (name, value) {
      let exDate = new Date()
      exDate.setTime(exDate.getTime() + 1000 * 60 * 60) // 设置cookie的失效时间为60分钟
      document.cookie = name + '=' + escape(value) + ';expires=' + exDate.toGMTString() +
        ';path=/'
    }
  }
}
</script>
