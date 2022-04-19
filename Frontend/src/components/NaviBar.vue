<!--统一导航栏，在页面的上方-->
<template>
  <div id="Navibar" class="Navibar" v-loading="Loading">
    <el-menu
      class="el-menu-index"
      mode="horizontal"
      background-color="#098ce4"
      text-color="#fff"
      active-text-color="#ffd04b"
      :default-active="MenuIndex"
    >
      <el-menu-item
        title="主页"
        @click="Index"
        class="el-icon-s-home"
        style="height: 70px"
        v-show="ShowLogout"
        index="8"
      ></el-menu-item>
      <el-menu-item
        title="刷新"
        @click="Refresh"
        class="el-icon-refresh"
        style="height: 70px; font-size: 25px"
        v-show="ShowLogout"
        index="11"
      ></el-menu-item>
      <el-menu-item
        @click="Login"
        v-show="ShowLogin"
        style="height: 70px"
        index="1"
        >用户登录</el-menu-item
      >
      <el-menu-item
        @click="TerminalLogin"
        v-show="ShowLogin"
        style="height: 70px"
        index="2"
        >会议室公共终端</el-menu-item
      >
      <el-menu-item
        @click="RoomReserve"
        v-show="ShowLogout"
        style="height: 70px"
        index="3"
        >预约</el-menu-item
      >
      <el-menu-item
        @click="UserReservationHistory"
        v-show="ShowLogout"
        style="height: 70px"
        index="4"
        >预约记录</el-menu-item
      >
      <el-menu-item
        @click="Info"
        v-show="ShowLogout"
        style="height: 70px"
        index="5"
        >个人信息</el-menu-item
      >
      <el-menu-item
        @click="RoomExamine"
        v-show="ShowManager"
        style="height: 70px"
        index="7"
        >审批
        <el-badge
          :value="ExamineTotal"
          v-if="ExamineTotal > 0"
          v-show="ShowManager"
        ></el-badge>
      </el-menu-item>
      <el-menu-item
        @click="UserPermissionManage"
        v-show="ShowRoot"
        style="height: 70px"
        index="6"
        >用户管理</el-menu-item
      >
      <el-menu-item
        @click="RoomInfoManage"
        v-show="ShowRoot"
        style="height: 70px"
        index="10"
        >房间管理</el-menu-item
      >

      <el-menu-item
        title="退出登录"
        @click="Logout"
        class="el-icon-switch-button"
        style="float: right; font-size: 25px; height: 70px"
        v-show="ShowLogout"
      ></el-menu-item>
      <div class="cs-logo">
        <img src="@/assets/cslogo-1-white.svg" alt="cs-logo" />
      </div>
      <el-menu-item
        style="float: right; height: 70px"
        v-show="ShowLogout"
        index="9"
        >{{ TextContent }}</el-menu-item
      >
    </el-menu>
  </div>
</template>

<script>
import { deleteCookie } from '@/utils/cookies.js'
import { GetUserInfo, Logout, GetReservationList } from '@/utils/communication.js'

export default {
  name: 'NaviBar',
  inject: ['PageReload'],
  props: {
  },
  data () {
    return {
      LOCALHOST: '', // 常量，用于通信
      Loading: false, // 加载
      // 以下用于各个组件的显示与隐藏
      MenuIndex: '0', // 当前导航栏index
      ShowLogin: false, // 在未登录状态时显示
      ShowManager: false, // 在是管理员时显示
      ShowRoot: false, // 在是超级管理员时显示
      ShowLogout: true, // 在登录状态时显示
      Authorized: false, // 是否真实登录
      TextContent: '', // 显示的用户信息
      ExamineTotal: 0 // 提示总的预约数量
    }
  },
  methods: {
    Refresh: function () {
      this.PageReload()
    },
    SetLoading: function (val) { // 设置加载状态
      this.Loading = val
    },
    LoginStatus: function (val) { // 转为登录状态
      if (val === '-1') { // 会议室终端专属
        this.ShowLogin = false
        this.ShowLogout = false
      } else {
        this.Authorized = true
        this.MenuIndex = val
        this.SaveUserInfoAndJudge()// 保存信息
      }
    },
    LogoutStatus: function () { // 转为登出状态
      this.ShowLogin = true
      this.ShowLogout = false
      this.ShowManager = false
      this.ShowRoot = false
      this.Authorized = false
    },
    SaveUserInfoAndJudge: function () { // 显示用户信息并判管理员
      GetUserInfo().then((res) => {
        let info = res['data']
        this.TextContent = '欢迎登录，' + info['fullname'] + '！'
        if (info['role'] !== 'U') { // 普通用户不能进入管理员页面
          this.ShowManager = true
          GetReservationList(1, 'state:W').then((r) => { // 获得预约信息
            this.ExamineTotal = r['data']['total']
            this.Loading = false
          })
          if (info['role'] === 'R') { // 是超级管理员
            this.ShowRoot = true
          }
        } else {
          this.Loading = false
        }
      })
    },
    Login: function () { // 登录，通过直接跳转url，实现发送GET请求
      window.location.href =
        'https://stu.cs.tsinghua.edu.cn/api/v2/authorize?response_type=code&client_id=N5SC-Ys13UYQ0hpEVP75L3p6VTg&redirect_uri=' + this.LOCALHOST + '/loginredirect/&scope=anything&state=a_try'
    },
    TerminalLogin: function () { // 终端登录
      this.$emit('TerminalLogin')
    },
    Info: function () { // 个人信息页
      if (this.MenuIndex !== '5' && this.Authorized) { this.$router.push('/Info') }
    },
    UserPermissionManage: function () { // 用户权限管理页
      if (this.MenuIndex !== '6' && this.Authorized) { this.$router.push('/UserPermissionManage') }
    },
    RoomInfoManage: function () { // 房间信息管理页
      if (this.MenuIndex !== '10' && this.Authorized) { this.$router.push('/RoomInfoManage') }
    },
    RoomReserve: function () { // 房间列表页
      if (this.MenuIndex !== '3' && this.Authorized) { this.$router.push('/RoomReserve') }
    },
    Index: function () { // 主页
      if (this.MenuIndex !== '8' && this.Authorized) { this.$router.push('/') }
    },
    RoomExamine: function () { // 预约审批页
      if (this.MenuIndex !== '7' && this.Authorized) { this.$router.push('/RoomExamine') }
    },
    Logout: function () { // 退出登录
      if (this.Authorized) {
        Logout().then((r) => {
          if (r['code'] === 200) { // 成功退出登录
            this.$message({
              type: 'success',
              message: '退出登录成功!',
              duration: 2000
            })
          } else { // 未登录或登录已过期
            this.$message({
              type: 'error',
              message: '未登录或登录已过期!',
              duration: 5000
            })
          }
        })
        this.LogoutStatus()
        deleteCookie('api_token') // 删除cookie
        this.$router.push('/')// 跳回主页
      }
    },
    UserReservationHistory: function () { // 个人预约列表页
      if (this.MenuIndex !== '4' && this.Authorized) { this.$router.push('/UserReservationHistory') }
    }
  },
  created () {
    this.LOCALHOST = process.env.NODE_ENV === 'development'
      ? 'http://localhost:8081' : 'https://frontend-antijuan.app.secoder.net'// 自动检测环境以配置LOCALHOST
  }
}
</script>
<style>
.Navibar {
  text-align: center;
}
.cs-logo img {
  float: right;
  display: block;
  width: 200px;
  height: 50px;
  padding: 10px 10px 5px 0px;
}
.el-icon-switch-button {
  font-size: 25px;
}
.el-icon-s-home {
  font-size: 25px;
}
</style>
