<template>
  <el-container>
    <NaviBar ref="NaviBar"></NaviBar>
    <el-container class="container">
      <el-dialog
        style="text-align: center"
        title="用户权限修改"
        :visible.sync="ShowRoleChangeDialog"
        :close-on-click-modal="false"
        width="50%"
      >
        <el-form label-width="200px">
          <el-form-item label="姓名">
            <el-form-item :label="UserName" label-width="300px"></el-form-item>
          </el-form-item>
          <el-Form-item label="权限">
            <el-select
              v-model="UserRole"
              placeholder="请设置该用户的权限"
              style="width: 300px"
            >
              <el-option label="超级管理员" value="R"></el-option>
              <el-option label="管理员" value="A"></el-option>
              <el-option label="普通用户" value="U"></el-option>
            </el-select>
          </el-Form-item>
          <el-Form-item label="教师">
            <el-select
              v-model="UserIsTeacher"
              placeholder="请设置该用户是否是教师"
              style="width: 300px"
            >
              <el-option label="是" :value="true"></el-option>
              <el-option label="否" :value="false"></el-option>
            </el-select>
          </el-Form-item>
          <el-Form-item label="研究所">
            <el-select
              v-model="UserInstitute"
              placeholder="请设置该用户所属研究所"
              style="width: 300px"
            >
              <el-option label="无" :value="null"></el-option>
              <el-option
                label="智能技术与系统国家重点实验室"
                value="1"
              ></el-option>
              <el-option label="人机交互与媒体集成研究所" value="2"></el-option>
              <el-option label="计算机网络技术研究所" value="3"></el-option>
              <el-option label="高性能计算研究所" value="4"></el-option>
              <el-option label="计算机软件研究所" value="5"></el-option>
              <el-option label="基础与实验教学部" value="6"></el-option>
            </el-select>
          </el-Form-item>
          <el-form-item label="当前状态">
            <el-form-item
              :label="UserStatus"
              label-width="300px"
            ></el-form-item>
          </el-form-item>
          <el-form-item label="限制该用户不可预约的天数">
            <el-input v-model="UserBanDays" style="width: 300px"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="RoleChange()" type="primary">确定</el-button>
        </span>
      </el-dialog>
      <el-main class="main_manage">
        <div id="UPM" class="UPM">
          <el-row class="UPMLine" type="flex" align="middle">
            <el-col :span="10">
              <el-input
                v-model="search_content"
                placeholder="搜索学工号或姓名"
                :clearable="true"
              >
                <el-select
                  v-model="search_select"
                  slot="prepend"
                  placeholder="请选择"
                >
                  <el-option label="姓名" value="fullname"></el-option>
                  <el-option label="学工号" value="uid"></el-option>
                </el-select>
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  @click="Search"
                ></el-button>
              </el-input>
            </el-col>
          </el-row>

          <el-table
            :data="userlist"
            :row-style="{ height: '50px' }"
            v-loading="loading"
            :default-sort="{ prop: 'uid', order: 'ascending' }"
            @sort-change="sortName"
            @filter-change="filterChange"
          >
            <el-table-column
              prop="fullname"
              label="姓名"
              width="110"
              align="center"
              sortable="custom"
            />

            <el-table-column
              label="学工号"
              prop="uid"
              width="150"
              align="center"
              sortable="custom"
            />

            <el-table-column
              prop="jobname"
              label="身份"
              width="100"
              align="center"
            />

            <el-table-column
              prop="role"
              label="权限"
              width="100"
              align="center"
              :formatter="roleFormatter"
              :filters="role_filters"
            />

            <el-table-column
              prop="institute"
              label="研究所"
              width="220"
              align="center"
              :formatter="instituteFormatter"
              :filters="institute_filters"
            />
            <el-table-column
              prop="role"
              label="修改权限"
              width="150"
              align="center"
            >
              <template slot-scope="scope">
                <el-button
                  v-if="scope.row.role !== 'R'"
                  size="medium"
                  type="primary"
                  @click="OpenRoleChange(scope.row.uid)"
                  >修改权限</el-button
                >

                <div v-if="scope.row.role == 'R'">不可操作</div>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            layout="total, prev, pager, next, jumper"
            :current-page="pagenumber"
            background
            :total="Math.max(1, this.usernumber)"
          >
          </el-pagination>
        </div>
      </el-main>
    </el-container>
    <el-footer>
      <FooterBar />
    </el-footer>
  </el-container>
</template>

<script>

import { readCookie } from '@/utils/cookies.js'
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import { CheckToken, GetUserInfo, GetUserList, SetRole } from '@/utils/communication.js'

export default {
  name: 'UserPermissonManage',
  components: {
    NaviBar,
    FooterBar
  },
  data () {
    return {
      pageinfo: '',
      pagenumber: 1,
      usernumber: 0,
      all_institutes: [
        { id: 1, name: '智能技术与系统国家重点实验室' },
        { id: 2, name: '人机交互与媒体集成研究所' },
        { id: 3, name: '计算机网络技术研究所' },
        { id: 4, name: '高性能计算研究所' },
        { id: 5, name: '计算机软件研究所' },
        { id: 6, name: '基础实验与教学部' }
      ],
      institute_filters: [],
      role_col: '',
      institute_col: '',
      all_roles: [
        { role: 'U', rolename: '普通用户' },
        { role: 'A', rolename: '管理员' },
        { role: 'R', rolename: '超级管理员' }
      ],
      role_filters: [],
      orderBy: 'uid',
      only: {
        role: [],
        institute: [],
        name_uid_contain: ''
      },
      search_content: '',
      search_select: '',
      form: '',
      num: '',
      uid: '',
      role: '',
      userlist: [],
      loading: false,
      pagesize: 10, // 每页的数据条数

      // 设置权限
      ShowRoleChangeDialog: false,
      UserName: '',
      UserStatus: '',
      UserId: '',
      UserRole: '',
      UserIsTeacher: '',
      UserInstitute: '',
      UserBanDays: '0'
    }
  },
  mounted () { // 打开时，通过cookie检测登陆状态
    this.loading = true
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
      this.$message({
        message: '请以超级管理员身份登录',
        type: 'error'
      })
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('6')
          this.Judge()
        } else { // 登录无效
          this.$router.push('/')
          this.$message({
            message: '请以超级管理员身份登录',
            type: 'error'
          })
        }
      })
      GetUserList('1', this.orderBy, this.only).then((r) => { // 刚开始必须获取用户列表，默认第1页
        if (r['code'] === 200) { // 有效信息
          this.Process(r['data'])
        }
      })
    }
    // set up role_filters
    let temRoleFilters = []
    for (let i in this.all_roles) {
      temRoleFilters.push({
        text: this.all_roles[i].rolename,
        value: this.all_roles[i].role
      })
    }
    this.role_filters = temRoleFilters
  },
  methods: {
    RoleChange () {
      if (isNaN(parseInt(this.UserBanDays))) {
        this.$message({
          type: 'error',
          message: '输入不合法!',
          duration: 3000
        })
        return
      }
      if (parseInt(this.UserBanDays) === 0 && this.UserStatus !== '正常') {
        this.$message({
          type: 'info',
          message: '您已解除对该用户的限制!',
          duration: 5000
        })
      }
      if (parseInt(this.UserBanDays) > 0) {
        this.$message({
          type: 'info',
          message: '您将该用户限制' + parseInt(this.UserBanDays).toString() + '天',
          duration: 5000
        })
      }
      SetRole(this.UserId, this.UserRole, this.UserIsTeacher, this.UserInstitute, this.UserBanDays).then((r) => {
        if (r['code'] === 200) { // 有效信息
          this.$message({
            type: 'success',
            message: '权限修改成功!',
            duration: 3000
          })
          this.loading = true
          GetUserList(this.pagenumber, this.orderBy, this.only).then((res) => { // 刚开始必须获取用户列表，默认第1页
            if (res['code'] === 200) { // 有效信息
              this.Process(res['data'])
            }
          })
        } else {
          this.$message({
            type: 'error',
            message: '权限修改失败!',
            duration: 3000
          })
        }
      })
    },
    OpenRoleChange (val) {
      let date = new Date()
      for (let i = 0; i < this.userlist.length; i++) {
        if (this.userlist[i].uid === val) {
          this.UserName = this.userlist[i].fullname
          this.UserId = this.userlist[i].id
          this.UserRole = this.userlist[i].role
          if (this.userlist[i].unban_time === null || this.userlist[i].unban_time < date.getTime()) {
            this.UserStatus = '正常'
          } else {
            let minutes = Math.floor((this.userlist[i].unban_time - date.getTime()) / 3600000)
            this.UserStatus = '封禁剩余' + minutes.toString() + '小时'
          }
          this.UserIsTeacher = this.userlist[i].is_teacher
          this.UserInstitute = this.userlist[i].institute === null ? null : this.userlist[i].institute.id.toString()
          this.UserBanDays = '0'
        }
      }
      this.ShowRoleChangeDialog = true
    },
    Returnhome: function () { // 跳转到主页面
      this.$router.push('/')
    },
    Process: function (data) { // 处理发来的data并更新信息
      // this.loading = true
      this.usernumber = parseInt(data['total'])
      let inituserlist = data['list']
      for (let i = 0; i <= inituserlist.length - 1; i++) { // 先增加列表的缺失成员，防止动态绑定问题
        inituserlist[i].jobname = ''
      }
      for (let i = 0; i <= inituserlist.length - 1; i++) {
        inituserlist[i].jobname = inituserlist[i].is_teacher === true ? '教师' : '学生'
      }
      this.userlist = inituserlist
      // set up institute_filters
      let temInstituteFilters = []
      for (let i in this.all_institutes) {
        temInstituteFilters.push({
          text: this.all_institutes[i].name,
          value: this.all_institutes[i].id
        })
      }
      this.institute_filters = temInstituteFilters
      // loaded
      this.loading = false
    },
    Search: function () {
      if (this.search_select === '') {
        this.$message({
          showClose: true,
          message: '请选择学工号或姓名',
          type: 'warning'
        })
        return
      }
      // 若为空
      if (this.search_content === '') {
        this.only.name_uid_contain = ''
      } else {
        // 输入学号筛选信息
        if (this.search_select === 'fullname') {
          this.only.name_uid_contain = `fullname__contains:${this.search_content}`
        }
        // 输入姓名筛选信息
        if (this.search_select === 'uid') {
          this.only.name_uid_contain = `uid__contains:${this.search_content}`
        }
      }

      this.loading = true
      this.pagenumber = 1
      GetUserList('1', this.orderBy, this.only).then((r) => {
        if (r['code'] === 200) {
          this.Process(r['data'])
        }
      })
    },
    handleSizeChange: function (val) {
      console.log(`每页 ${val} 条`)
    },

    // 跳转页面--操作
    handleCurrentChange: function (val) {
      this.loading = true
      this.pagenumber = val
      val = val.toString()
      this.changePage(val)
    },

    // 跳转页面--函数
    changePage: function (val) {
      let num = parseInt(val)
      GetUserList(val, this.orderBy, this.only).then((r) => {
        if (r['code'] === 200) { // 有效信息
          this.pagenumber = num
          this.Process(r['data'])
        }
      })
    },

    //  返回主页
    Return: function () {
      this.$router.push('/')
    },

    // 判管理员
    Judge: function () {
      GetUserInfo().then((res) => {
        let info = res['data']
        if (info.role !== 'R') { // 不是超级管理员则跳出
          this.$router.push('/')
          this.$message({
            message: '请以超级管理员身份登录',
            type: 'error'
          })
        }
      })
    },

    // 修改权限为‘普通用户’
    RoleChange_To_U: function (val) {
      for (let i = 0; i < this.userlist.length; i++) {
        if (this.userlist[i].uid === val) {
          let uid = this.userlist[i].uid
          let role = this.userlist[i].role
          if (role === 'A') {
            SetRole(uid, 'U').then((r) => {
              if (r['code'] === 200) { // 更换权限有效
                this.$message({
                  type: 'success',
                  message: '已修改为普通用户'
                })
                this.userlist[i].role = 'U'
                this.userlist[i].rolename = '普通用户'
              }
            })
          } else {
            this.$message({
              message: '无法修改该用户权限',
              type: 'error'
            })
          }
          break
        }
      }
    },

    // 修改权限为‘管理员’
    RoleChange_To_A: function (val) {
      for (let i = 0; i < this.userlist.length; i++) {
        if (this.userlist[i].uid === val) {
          let role = this.userlist[i].role
          let uid = this.userlist[i].uid
          if (role === 'U') {
            SetRole(uid, 'A').then((r) => {
              if (r['code'] === 200) { // 更换权限有效
                this.$message({
                  type: 'success',
                  message: '已修改为管理员'
                })
                this.userlist[i].rolename = '管理员'
                this.userlist[i].role = 'A'
              }
            })
          } else {
            this.$message({
              message: '无法修改该用户权限',
              type: 'error'
            })
          }
          break
        }
      }
    },

    // 限制预约函数，功能未实现
    Restrict: function (
    ) {
      // TODO
    },

    // 排序---fullname, uid
    sortName: function (obj) {
      if (obj.order === null) {
        return this.userlist
      }
      let prop = obj.prop
      if (obj.order === 'ascending') {
        this.orderBy = prop
      }
      if (obj.order === 'descending') {
        this.orderBy = '-' + prop
      }
      this.loading = true
      this.pagenumber = 1
      GetUserList('1', this.orderBy, this.only).then((r) => { // 刚开始必须获取用户列表，默认第1页
        if (r['code'] === 200) { // 有效信息
          this.Process(r['data'])
        }
      })
    },
    instituteFormatter: function (row) {
      return row.institute === null ? '' : row.institute.name
    },
    roleFormatter: function (row) {
      for (let r of this.all_roles) {
        if (r.role === row.role) {
          return r.rolename
        }
      }
    },
    filterChange: function (obj) {
      // 理论上只是一次循环
      for (const key in obj) {
        let array = obj[key]
        // 如果是重置
        if (array.length === 0) {
          // 如果是重置institute
          if (key === this.institute_col) {
            this.only.institute = []
          }
          if (key === this.role_col) {
            this.only.role = []
          }
        } else {
          // 如果是筛选institute
          if (typeof (array[0]) === 'number') {
            if (key !== this.institute_col) {
              this.institute_col = key
            }
            this.only.institute = array
          }
          // 如果是筛选role
          if (typeof (array[0]) === 'string') {
            if (key !== this.role_col) {
              this.role_col = key
            }
            this.only.role = array
          }
        }
        this.loading = true
        this.pagenumber = 1

        GetUserList('1', this.orderBy, this.only).then((r) => { // 刚开始必须获取用户列表，默认第1页
          if (r['code'] === 200) { // 有效信息
            this.Process(r['data'])
          }
        })
      }
    }
  }
}

</script>

<style scoped>
.header_manage {
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #333;
  text-align: center;
  line-height: 60px;
  letter-spacing: 20px;
  font-size: 30px;
}
.footer_manage {
  height: 20% !important;
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #fff;
  justify-content: center;
  text-align: center;
}
.main_manage {
  display: flex;
  justify-content: center;
}

.el-select {
  width: 90px;
}
.el-input-group__prepend {
  background-color: #fff;
}

.UPMbody {
  display: flex;
}

.UPMLine {
  margin-bottom: 10px;
}
.FormLine {
  display: flex;
  height: 65px;
}

.el-pagination {
  margin-top: 20px;
  text-align: center;
}
.el-table {
  /* margin-left: 10%; */
  color: #000;
}
.container {
  display: flex;
  min-height: 600px;
}
</style>
<style scoped>
.el-container {
  background-color: #fff;
}
</style>
