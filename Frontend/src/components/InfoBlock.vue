<!--，包含个人信息：姓名、学工号、邮箱或手机、身份、所在研究所 和'保存'、'返回主页'按钮-->
<template>
  <div id="InfoBlock" class="InfoBlock">
    <el-main class="main_info">
      <el-form :model="infoform" :rules="rules" ref="infoform" id="form_info">
        <el-form-item label="姓名" label-width="100px" v-model="username">
          <el-input
            v-model="username"
            :disabled="true"
            :style="{width: '100px'}"
          ></el-input>
        </el-form-item>
        <el-form-item label="学工号" label-width="100px" v-model="userid">
          <el-input
            v-model="userid"
            :disabled="true"
            :style="{width: '100px'}"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="身份"
          label-width="100px"
          v-model="student_or_teacher"
        >
          <el-input
            v-model="student_or_teacher"
            :disabled="true"
            :style="{width: '100px'}"
          ></el-input>
        </el-form-item>
        <el-form-item label="角色" label-width="100px" v-model="Role">
          <el-input
            v-model="Role"
            :disabled="true"
            :style="{width: '100px'}"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="input_phone" label-width="100px">
          <el-input
            v-model="infoform.input_phone"
            :style="{width: '100px'}"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="input_email" label-width="100px">
          <el-input
            v-model="infoform.input_email"
            :style="{width: '100px'}"
            clearable=""
          ></el-input>
        </el-form-item>
        <el-form-item label="所在研究所" label-width="100px">
          <el-select v-model="value">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <!--'保存'按钮-->
          <el-button
            size="medium"
            class="save_button"
            @click="save('infoform')"
          >
            保存
          </el-button>
          <!--'返回主页'按钮-->
          <el-button
           size="medium"
           class="return_button"
           @click="Return">
            返回主页
          </el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import TextBlock from '@/components/TextBlock.vue'
import { GetUserInfo, Save } from '@/utils/communication.js'

export default {
  name: 'InfoBlock',
  components: {
    TextBlock
  },
  props: {
  },
  data () {
    return {
      infoform: {
        input_email: '',
        input_phone: ''
      },
      username: '',
      userid: '',
      role: '',
      Role: '',
      phone_: '',
      email_: '',
      institute_: '',
      student_or_teacher: '',
      options: [
        {
          value: 1,
          label: '智能技术与系统国家重点实验室'
        },
        {
          value: 2,
          label: '人机交互与媒体集成研究所'
        },
        {
          value: 3,
          label: '计算机网络技术研究所'
        },
        {
          value: 4,
          label: '高性能计算研究所'
        },
        {
          value: 5,
          label: '计算机软件研究所'
        },
        {
          value: 6,
          label: '基础实验与教学'
        },
        {
          value: 0,
          label: '无'
        }
      ],
      value: ''
    }
  },
  computed: {
    rules () {
      var EmailRule = (rule, value, callback) => {
        let regEmail = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
        if (!regEmail.test(value)) {
          callback(new Error('请填写正确的邮箱'))
        } else {
          callback()
        }
      }
      var PhoneRule = (rule, value, callback) => {
        let regPhone = /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/
        if (!regPhone.test(value) && value !== '') {
          callback(new Error('请填写正确的电话号码！！'))
        } else {
          callback()
        }
      }; return {
        input_email: [
          { required: true, message: '请输入邮箱！', trigger: 'blur' },
          { validator: EmailRule, trigger: 'blur' }
        ],
        input_phone: [
          { validator: PhoneRule, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    save (formname) { //  保存信息
      if (this.value === 0) {
        this.institute_ = null
      } else {
        this.institute_ = this.value
      }
      this.$refs[formname].validate((valid) => {
        if (valid) {
          Save(this.infoform.input_email.trim(), this.infoform.input_phone.trim(), this.institute_).then((r) => {
            if (r['code'] === 200) {
              this.$message({
                message: '保存成功',
                type: 'success'
              })
            } else {
              this.$message({
                message: '数据传输失败！',
                type: 'error'
              })
            }
          })
        } else {
          this.$message({
            message: '保存失败！',
            type: 'error'
          })
        }
      })
    },
    Return: function () { //  返回主页
      this.$router.push('/')
    },
    SaveUserInfoAndJudge: function () { // 保存用户信息并判管理员
      GetUserInfo().then((res) => {
        let info = res['data']
        this.role = info['role']
        if (this.role === 'U') {
          this.Role = '普通用户'
        }
        if (this.role === 'A') {
          this.Role = '管理员'
        }
        if (this.role === 'R') {
          this.Role = '超级管理员'
        }
        this.username = info['fullname']
        this.userid = info['uid']
        this.email_ = info['email']
        this.phone_ = info['phone_number']
        this.infoform.input_phone = this.phone_
        this.infoform.input_email = this.email_
        if (info['is_teacher']) {
          this.student_or_teacher = '教师'
        } else {
          this.student_or_teacher = '学生'
        }
        if (res['data']['institute'] === null) {
          this.value = 0
        } else {
          this.value = res['data']['institute']['id']
        }
      })
    }
  }
}
</script>

<style scoped>
.InfoBlock {
  padding: 20px 0px 0px 0px;
  text-align: center;
  display: flex;
  margin: 0 auto;
  margin-bottom: 20px;
  margin-top: 20px;
  min-height: 578px;
}
.InfoLine {
  display: flex;
  height: 65px;
}
.el-input {
  width: 200px;
}
.main_info {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  margin: 0 auto;
  padding-left: 10px;
}
#form_info >>> .el-form-item__label {
  text-align: right;
  font-size: 17px;
  font-weight: 600;
}
.el-form-item {
  margin-bottom: 30px;
}
</style>
