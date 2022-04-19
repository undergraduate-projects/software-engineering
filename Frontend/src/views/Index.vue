<!--网站主页-->
<template>
  <el-container>
    <div id="Index" class="Index">
      <div id="NaviBar" class="NaviBar">
        <NaviBar @TerminalLogin="TerminalLogin" ref="NaviBar"></NaviBar>
      </div>
      <div class="room_picture">
        <img src="@/assets/room.jpg" height="100%" width="100%" />
      </div>
    </div>
    <TerminalLoginDialog :dialogVisible="DialogVisible" @Cancel="Cancel" />
    <el-footer><FooterBar /></el-footer>
  </el-container>
</template>

<script>
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import TerminalLoginDialog from '@/components/TerminalLoginDialog.vue'
import { readCookie } from '@/utils/cookies.js'
import { CheckToken } from '@/utils/communication.js'

export default {
  name: 'Index',
  components: {
    NaviBar,
    FooterBar,
    TerminalLoginDialog
  },
  data () {
    return {
      DialogVisible: false, // 会议室终端登录框
      ShowString: ''// 导航栏使用
    }
  },
  methods: {
    TerminalLogin: function () { // 显示会议室终端登录框
      this.DialogVisible = true
    },
    Cancel: function () { // 隐藏会议室终端登录框
      this.DialogVisible = false
    }
  },
  mounted () { // 主页打开时，通过cookie检测登陆状态
    let apiToken = readCookie('api_token')
    if (apiToken.length !== 0) { // token存在
      // this.$refs.NaviBar.SetLoading(true)// 开始加载
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('8')
          // this.$refs.NaviBar.SetLoading(false)
        } else {
          this.$refs.NaviBar.LogoutStatus()
          // this.$refs.NaviBar.SetLoading(false)
        }
      })
    } else {
      this.$refs.NaviBar.LogoutStatus()
    }
  }
}
</script>

<style scoped>
.Index {
  font-size: 0px;
}
.room_picture {
  display: flex;
  overflow: hidden;
}
</style>
