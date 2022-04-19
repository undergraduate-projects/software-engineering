<!--会议室终端登录对话框-->
<template>
  <el-dialog
    style="text-align: center"
    title="会议室公共终端登录"
    :visible.sync="DialogVisible"
    :close-on-click-modal="false"
    :before-close="Cancel"
    width="50%"
  >
    <el-form label-width="80px">
      <el-form-item label="会议室id">
        <el-input v-model="RoomId"></el-input>
      </el-form-item>
      <el-form-item label="token">
        <el-input v-model="Token"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="Cancel">取消</el-button>
      <el-button @click="Login" type="primary">登录</el-button>
    </span>
  </el-dialog>
</template>

<script>

import { TerminalLogin } from '@/utils/communication.js'
import { setCookie } from '@/utils/cookies.js'

export default {
  name: 'PostDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => false
    }
  },
  data () {
    return {
      DialogVisible: this.dialogVisible, // 是否显示该组件
      RoomId: '', // 会议室id
      Token: ''// token
    }
  },
  watch: {// 监听
    dialogVisible: {
      handler (val) {
        this.DialogVisible = val
      }
    }
  },
  methods: {
    Login: function () { // 终端登录
      let reg = /^\d+$/
      if (reg.test(this.RoomId)) { // 输入的是纯数字
        TerminalLogin(this.RoomId, this.Token).then((r) => {
          if (r['code'] === 400) { // 无效的会议室id
            this.$message({
              type: 'info',
              message: '不存在该会议室！',
              duration: 3000
            })
          } else if (r['code'] === 420) { // token错误
            this.$message({
              type: 'error',
              message: 'token错误！',
              duration: 3000
            })
          } else { // 成功登录
            this.$message({
              type: 'success',
              message: '公共终端登录成功！',
              duration: 3000
            })
            setCookie('terminal_token', this.Token, 7 * 24 * 60)// 设置7天cookie
            this.$router.push({ name: 'Terminal', params: { RoomId: this.RoomId } })
          }
        })
      } else { // 输入不合法
        this.$message({
          type: 'error',
          message: '会议室id必须填写数字！',
          duration: 3000
        })
      }
    },
    Cancel: function () { // 取消，清空信息并隐藏对话框
      this.RoomId = ''
      this.Token = ''
      this.$emit('Cancel')
    }
  }
}
</script>
