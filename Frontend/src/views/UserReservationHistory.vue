<template>
  <el-container style="border: 1px solid #eee">
    <NaviBar ref="NaviBar" />

    <el-container>
      <el-aside>
        <el-menu
          default-active="0"
          @select="handleAsideSelect"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="0"
            ><i class="el-icon-house"></i>全部预约
          </el-menu-item>
          <el-menu-item index="1"
            ><i class="el-icon-finished"></i>已使用预约
          </el-menu-item>
          <el-menu-item index="6"
            ><i class="el-icon-refresh"></i>待审批预约
          </el-menu-item>
          <el-menu-item index="2"
            ><i class="el-icon-key"></i>待使用预约
          </el-menu-item>
          <el-menu-item index="3"
            ><i class="el-icon-remove-outline"></i>已取消预约
          </el-menu-item>
          <el-menu-item index="4"
            ><i class="el-icon-circle-close"></i>未通过预约
          </el-menu-item>
          <el-menu-item index="7"
            ><i class="el-icon-alarm-clock"></i>已失效预约
          </el-menu-item>
          <el-menu-item index="5"
            ><i class="el-icon-warning-outline"></i>违约记录
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main v-loading="loading">
        <div class="panel-header" v-if="activeList.length !== 0">
          <!--      用于填写面板的标题-->
          <el-row :gutter="20">
            <el-col :span="9">
              <p>申请提交时间</p>
            </el-col>
            <el-col :span="8">
              <p>申请使用会议室</p>
            </el-col>
            <el-col :span="5">
              <p>预约进度</p>
            </el-col>
            <el-col :span="2"> </el-col>
          </el-row>
        </div>

        <div class="active-list">
          <div
            v-if="activeList.length !== 0"
            v-for="res in activeList.slice(
              activeListSliceStart,
              activeListSliceEnd
            )"
            :key="res.id"
          >
            <CollapsePanel :res-info.camel="res" @cancel="cancelReservation" />
          </div>
          <div v-if="activeList.length === 0">
            <div><h2>暂无记录</h2></div>
          </div>
        </div>
        <div class="pager" v-if="activeList.length !== 0">
          <el-pagination
            background
            @current-change="handleCurrentChange"
            layout="prev, pager, next, total, jumper"
            :total="activeList.length"
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
import CollapsePanel from '@/components/CollapsePanel.vue'
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import { GetUserReservation, CancelUserReservation, CheckToken } from '@/utils/communication.js'
import { readCookie } from '@/utils/cookies.js'

export default {
  name: 'UserReservationHistory',
  components: {
    CollapsePanel,
    FooterBar,
    NaviBar
  },
  data () {
    return {
      loading: true,
      allReservationList: [],
      dishonestReservationList: [],
      fulfilledReservationList: [],
      upcomingReservationList: [],
      cancelledReservationList: [],
      rejectedReservationList: [],
      unexaminedReservationList: [],
      expiredReservationList: [],
      activeList: [],
      activeListIndex: 0, // 0:全部记录， 1：已使用记录， 2：未使用记录， 3：取消记录， 4：失败记录， 5：违约记录
      activePageNum: 1,
      itemPerPage: 10
    }
  },
  methods: {
    goToHome () {
      this.$router.push('/')
    },
    handleAsideSelect (key, keyPath) {
      // console.log(key, keyPath)
      this.activeListIndex = parseInt(key)
      this.activePageNum = 1 // 每次切换新的记录类型时，从第一页开始
      if (key === '0') { // 展示全部预约记录
        this.activeList = this.allReservationList
      } else if (key === '1') { // 展示已使用预约记录
        this.activeList = this.fulfilledReservationList
      } else if (key === '2') { // 展示未使用预约
        this.activeList = this.upcomingReservationList
      } else if (key === '3') { // 展示取消记录
        this.activeList = this.cancelledReservationList
      } else if (key === '4') { // 展示预约失败记录
        this.activeList = this.rejectedReservationList
      } else if (key === '5') { // 展示违约记录
        this.activeList = this.dishonestReservationList
      } else if (key === '6') { // 展示待审批记录
        this.activeList = this.unexaminedReservationList
      } else if (key === '7') { // 展示失效记录
        this.activeList = this.expiredReservationList
      }
    },
    handleCurrentChange (val) {
      // console.log('当前页: ' + val)
      this.activePageNum = parseInt(val)
    },
    getStartTime (resInfo) { // 从timeSpan中获取会议室开始使用时间的毫秒级时间戳
      let offset = 0 // 设置最早的使用时间为 8:00 am， 时间间隔为半个小时
      for (let i = 0; i < 48; i++) {
        if (resInfo.timeSpan[i] === '1') {
          offset += i * 30 * 60
          break
        }
      }
      // 以日期初始化Date，默认时间为早上8:00
      return new Date(resInfo.date).getTime() + offset * 1000
    },
    // getEndTime (resInfo) { // 从timeSpan中获取会议室开始使用时间的毫秒级时间戳
    //   let offset = 0 // 设置最早的使用时间为 8:00 am， 时间间隔为半个小时
    //   for (let i = 0; i < 48; i++) {
    //     if (resInfo.timeSpan[i] === '1') {
    //       offset = i * 30 * 60
    //     }
    //   }
    //   return new Date(resInfo.date).getTime() + offset * 1000
    // },
    isArriveLate (resInfo) {
      return resInfo.state === '签到超时'
      // if (!resInfo.arrivalTime) {
      //   return false
      // } else {
      //   let expectedStartTime = new Date(resInfo.date).getTime() + this.getStartTime(resInfo) - 8 * 60 * 60 * 1000
      //   return new Date(resInfo.arrivalTime).getTime() > expectedStartTime
      // }
    },
    isLeaveLate (resInfo) {
      return resInfo.state === '已完成（晚退）'
      // if (!resInfo.leaveTime) {
      //   return false
      // } else {
      //   let expectedEndTime = new Date(resInfo.date).getTime() + this.getEndTime(resInfo) - 8 * 60 * 60 * 1000
      //   return new Date(resInfo.leaveTime).getTime() > expectedEndTime
      // }
    },
    isUpcoming (resInfo) { // 不包括等待审批的预约
      return resInfo.state === '审批通过'
      // if (!resInfo.approvalTime) {
      //   return true
      // } else {
      //   let currentTime = new Date().getTime() // 获取毫秒级时间戳
      //   return new Date(resInfo.startTime).getTime() > currentTime
      // }
    },
    isFulfilled (resInfo) {
      return resInfo.state === '已完成'
      // if (!resInfo.approvalTime) {
      //   return false
      // }
      // return resInfo.leaveTime
    },
    isRejected (resInfo) {
      return resInfo.state === '已被拒绝'
      // return resInfo.approvalTime && !resInfo.approvalResult
    },
    isCancelled (resInfo) {
      return resInfo.state === '已撤销'
      // return resInfo.cancelTime
    },
    isUnexamined (resInfo) {
      return resInfo.state === '等待审批'
    },
    isExpired (resInfo) {
      return resInfo.state === '已过期'
    },
    cancelReservation (resInfo) {
      console.log('receive cancel-res')
      this.$confirm('此操作将取消本次会议室预约, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        CancelUserReservation(resInfo.id).then((res) => {
          if (res['data'] === 'Success') {
            this.$message({
              type: 'success',
              message: '取消成功!'
            })
            // 刷新页面
            let curListNum = 0 // 默认为this.allReservationList
            if (this.activeList === this.upcomingReservationList) {
              curListNum = 1
            } else if (this.activeList === this.unexaminedReservationList) {
              curListNum = 2
            }

            GetUserReservation().then((r) => {
              this.updateResList(r)
              if (curListNum === 0) {
                this.activeList = this.allReservationList
              } else if (curListNum === 1) {
                this.activeList = this.upcomingReservationList
              } else if (curListNum === 2) {
                this.activeList = this.unexaminedReservationList
              }
            })
          } else {
            this.$message({
              type: 'error',
              message: '取消失败!'
            })
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已放弃取消预约'
        })
      })
    },
    updateResList (res) {
      this.loading = true
      this.allReservationList = []
      this.dishonestReservationList = []
      this.fulfilledReservationList = []
      this.upcomingReservationList = []
      this.cancelledReservationList = []
      this.rejectedReservationList = []
      this.unexaminedReservationList = []
      this.expiredReservationList = []

      res.data.list.forEach((elem) => {
        let renameData = {}
        renameData['id'] = elem['id']
        renameData['applicant'] = elem['applicant']
        renameData['room'] = elem['room']
        renameData['date'] = elem['date']
        renameData['timeSpan'] = elem['time_span']
        renameData['applyReason'] = elem['apply_reason']
        renameData['submitTime'] = elem['submit_time']
        renameData['approvalResult'] = elem['approval_result']
        renameData['approvalPerson'] = elem['approval_person']
        renameData['approvalTime'] = elem['approval_time']
        renameData['token'] = elem['token']
        renameData['arrivalTime'] = elem['arrival_time']
        renameData['leaveTime'] = elem['leave_time']
        renameData['cancelTime'] = elem['cancel_time']
        renameData['state'] = elem['state']
        renameData['refuseReason'] = elem['refuse_reason']
        this.allReservationList.push(renameData)
      })

      console.log(this.allReservationList)
      this.allReservationList.forEach((elem) => {
        if (this.isCancelled(elem)) {
          this.cancelledReservationList.push(elem)
        }
        if (this.isArriveLate(elem) || this.isLeaveLate(elem)) {
          this.dishonestReservationList.push(elem)
        }
        if (this.isUpcoming(elem)) {
          this.upcomingReservationList.push(elem)
        }
        if (this.isFulfilled(elem)) {
          this.fulfilledReservationList.push(elem)
        }
        if (this.isRejected(elem)) {
          this.rejectedReservationList.push(elem)
        }
        if (this.isUnexamined(elem)) {
          this.unexaminedReservationList.push(elem)
        }
        if (this.isExpired(elem)) {
          this.expiredReservationList.push(elem)
        }
      })
      this.loading = false
    }
  },
  computed: {
    activeListSliceStart () {
      return (this.activePageNum - 1) * this.itemPerPage
    },
    activeListSliceEnd () {
      return Math.min(this.activePageNum * this.itemPerPage, this.activeList.length)
    }
  },
  mounted () {
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('4')
          GetUserReservation().then((res) => {
            this.updateResList(res)
            this.activeList = this.allReservationList
            // console.log('created' + this.activeList)
          })
        } else {
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style scoped>
.nav-block {
  list-style-type: none;
  margin: 0;
  display: block;
}

.nav-block li {
  padding-top: 2.5%;
  float: left;
}

.nav-block li button {
  display: block;
  margin: 8px;
  color: white;
  border: none;
  background: none;
  font-size: 1em;
}

.nav-block li button:hover {
  color: #ffd04b;
}

.el-aside {
  background-color: white;
  height: auto;
  width: 20% !important;
}

.el-main {
  height: auto;
  border-left: 1px solid #e6e6e6;
}

.panel-header {
  /*box-sizing: border-box;*/
  width: 100%;
  text-align: center;
  border: 1px solid #e3e6f0;
  border-radius: 0.35rem;
  margin-left: 5px;
  border-left: 0.25rem solid #e3e6f0 !important;
}

.pager {
  text-align: center;
}
</style>
