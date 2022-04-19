<template>
  <el-container>
    <div id="Manager" class="Manager">
      <NaviBar ref="NaviBar"></NaviBar>
      <div class="room_picture" v-show="notlogin">
        <img src="@/assets/room.jpg" height="600" width="1520px" />
      </div>
      <el-main v-show="islogin">
        <div>
          <el-button type="manage" @click="UserManage">
            用户权限管理
            <el-col style="margin-top: 20px"> (仅超级管理员可进) </el-col>
          </el-button>
          <el-button type="room" @click="RoomManage">
            房间信息管理
            <el-col class="el-icon-s-home" style="margin-top: 20px"></el-col>
          </el-button>
        </div>
      </el-main>
    </div>
    <el-footer><FooterBar /></el-footer>
  </el-container>
</template>

<script>
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import { readCookie } from '@/utils/cookies.js'
import { CheckToken } from '@/utils/communication.js'

export default {
  name: 'Manager',
  components: {
    NaviBar,
    FooterBar
  },
  props: {
    Manager_content: {
      type: String,
      default: () => '管理员界面'
    }
  },
  data () {
    return {
      ManagerBlockStyle: {
        backgroundColor: 'rgb(245, 245, 230)',
        display: 'flex'
      },
      manager: 'none',
      islogin: 0,
      notlogin: 1
    }
  },
  watch: {
  },
  methods: {
    logout: function () {
      this.islogin = 0
      this.notlogin = 1
      this.$router.push('/')
    },
    UserManage: function () { // 跳转到用户信息管理页面
      this.$router.push('/UserPermissionManage')
    },
    RoomManage: function () { // 跳转到房间信息管理页面
      this.$router.push('/RoomInfoManage')
    }
  },
  mounted () { // 通过cookie检测登录状态
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.islogin = 0
      this.notlogin = 1
      this.$router.push('/')
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('6')
          this.islogin = 1
          this.notlogin = 0
        } else { // 登录无效 返回主页
          this.islogin = 0
          this.notlogin = 1
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style scoped>
.Manager {
  font-size: 0px;
  background-color: rgb(210, 238, 214);
}

.el-button--manage {
  color: rgb(254, 204, 168);
  background-color: #9020b2;
  border-color: #20b2aa;
  height: 300px;
  width: 500px;
  font-size: 40px;
  margin-top: 80px;
  margin-right: 80px;
}

.el-button--room {
  color: rgb(255, 255, 255);
  background-color: #20b25d;
  border-color: #20b2aa;
  height: 300px;
  width: 500px;
  font-size: 40px;
}
.el-main {
  text-align: center;
  min-height: 600px;
}
.room_picture {
  display: flex;
  max-height: 600px;
  max-width: 1520px;
  overflow: hidden;
}
</style>
