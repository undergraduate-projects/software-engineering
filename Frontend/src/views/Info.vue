<template>
  <el-container>
    <NaviBar ref="NaviBar" />
    <div id="Info" class="Info">
      <div id="Infobody" class="Infobody">
        <!--个人信息展示栏-->
      </div>
      <div id="InfoBlock" :style="InfoBlockStyle">
        <InfoBlock ref="InfoBlock"></InfoBlock>
      </div>
    </div>
    <el-footer>
      <FooterBar />
    </el-footer>
  </el-container>
</template>

<script>
import InfoBlock from '@/components/InfoBlock.vue'
import NaviBar from '@/components/NaviBar.vue'
import { readCookie } from '@/utils/cookies.js'
import { CheckToken } from '@/utils/communication.js'
import FooterBar from '../components/FooterBar.vue'

export default {
  name: 'Info',
  components: {
    InfoBlock,
    NaviBar,
    FooterBar
  },
  props: {
  },
  data () {
    return {
      InfoBlockStyle: {
        backgroundColor: 'rgb(255,255,255)',
        display: 'flex'
      }
    }
  },
  methods: {
    Returnhome: function () { // 跳转到主页面
      this.$router.push('/')
    }
  },
  mounted () { // 打开时，通过cookie检测登陆状态
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('5')
          this.$refs.InfoBlock.SaveUserInfoAndJudge()
        } else { // 登录无效
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style scoped>
.Info {
  font-size: 0px;
}

.Infobody {
  display: flex;
}
.Info_header {
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #333; /* “个人信息管理 ” 字体颜色*/
  text-align: center;
  line-height: 60px;
  letter-spacing: 20px;
  font-size: 30px;
  /* font-family: Cursive; */
}
.Info_footer {
  height: 20% !important;
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #fff;
  justify-content: center;
  text-align: center;
}
.return_button_info {
  background-color: #daee22;
  border-color: #0eaf94;
}
.el-input.is-disabled .el-input__inner {
  background-color: #ffffff !important;
  color: #606266;
}
</style>
<style scoped>
.Info_pageheader {
  margin-top: 20px;
  font-weight: 600;
  color: azure;
}
</style>
