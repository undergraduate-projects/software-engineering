<template>
  <div class="collapse-panel">
    <div class="panel-header">
      <!--      用于填写面板的标题-->
      <el-row :gutter="20">
        <el-col :span="9">
          <div class="submit-time">
            {{
              new Date(resInfo.submitTime).toLocaleDateString() +
              " " +
              new Date(resInfo.submitTime).toLocaleTimeString()
            }}
          </div>
        </el-col>
        <el-col :span="8">
          <div class="room-name">
            {{ resInfo.room.building.name + " " + resInfo.room.name }}
          </div>
        </el-col>
        <el-col :span="5">
          <div
            class="res-status"
            :style="{ backgroundColor: approvalResultBgColor }"
          >
            {{ useResultString }}
          </div>
        </el-col>
        <el-col :span="2">
          <div class="collapse-button">
            <!--      用于提示是否折叠面板-->
            <div v-if="isCollapsed">
              <el-button
                size="mini"
                icon="el-icon-caret-bottom"
                @click="handleCollapse"
                :style="{ border: 'none' }"
                round
              ></el-button>
            </div>
            <div v-else>
              <el-button
                size="mini"
                icon="el-icon-caret-top"
                @click="handleCollapse"
                :style="{ border: 'none' }"
                round
              ></el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="panel-body" v-if="isCollapsed === false">
      <!--      用于填写详细信息-->
      <div class="res-step">
        <el-steps
          :space="200"
          :active="stepActiveIndex"
          finish-status="success"
          align-center
        >
          <el-step title="递交申请" icon="el-icon-s-promotion"></el-step>
          <el-step
            :title="waitEaxmineTitle"
            icon="el-icon-s-check"
            :status="waitEaxmineStatus"
          ></el-step>
          <el-step
            :title="waitUseTitle"
            icon="el-icon-key"
            :status="waitUseStatus"
          ></el-step>
          <el-step
            :title="finishStepTitle"
            icon="el-icon-time"
            :status="finishStepStatus"
          ></el-step>
        </el-steps>
      </div>

      <el-row :gutter="20" type="flex">
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block"><strong>申请人： </strong></div>
            <div style="display: inline-block">
              {{ resInfo.applicant.fullname }}
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>申请提交时间： </strong>
            </div>
            <div style="display: inline-block">
              {{
                new Date(resInfo.submitTime).toLocaleDateString() +
                " " +
                new Date(resInfo.submitTime).toLocaleTimeString()
              }}
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>申请使用教室： </strong>
            </div>
            <div style="display: inline-block">
              {{ resInfo.room.building.name + " " + resInfo.room.name }}
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>申请使用时间： </strong>
            </div>
            <div style="display: inline-block">
              {{
                new Date(resInfo.date).toLocaleDateString() +
                " " +
                timeSpanString
              }}
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>申请理由： </strong>
            </div>
            <div style="display: inline-block">
              {{ resInfo.applyReason }}
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="res-item" v-if="hasBeenApproved">
            <div style="display: inline-block"><strong>审批人： </strong></div>
            <div style="display: inline-block">
              {{ resInfo.approvalPerson }}
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>审批结果： </strong>
            </div>
            <div style="display: inline-block">{{ approvalResultString }}</div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" v-if="hasBeenApproved">
        <el-col :span="12">
          <div class="res-item" v-if="hasBeenApproved">
            <div style="display: inline-block">
              <strong>审批时间： </strong>
            </div>
            <div style="display: inline-block">
              {{
                new Date(resInfo.approvalTime).toLocaleDateString() +
                " " +
                new Date(resInfo.approvalTime).toLocaleTimeString()
              }}
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="res-item" v-if="resInfo.approvalResult">
            <div style="display: inline-block">
              <strong>签到/签退口令： </strong>
            </div>
            <div class="token-text" v-if="showTokenText">
              {{ resInfo.token }}
            </div>
            <div class="token-text" v-else>******</div>
            <el-tooltip
              :content="switchValue"
              placement="top"
              effect="light"
              :style="{
                display: 'inline-block',
                position: 'absolute',
                right: '5%',
              }"
            >
              <el-switch
                v-model="switchValue"
                active-color="#3498db"
                inactive-color="#95a5a6"
                active-value="显示口令"
                inactive-value="隐藏口令"
                @change="tokenVisibleChange"
              >
              </el-switch>
            </el-tooltip>
          </div>
          <div class="res-item" v-else>
            <div style="display: inline-block">
              <strong>审批意见： </strong>
            </div>
            <div style="display: inline-block">{{ resInfo.refuseReason }}</div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="res-item">
            <div style="display: inline-block">
              <strong>使用状况： </strong>
            </div>
            <div style="display: inline-block">{{ useResultString }}</div>
          </div>
        </el-col>
        <el-col :span="12" v-if="cancelable">
          <div
            v-if="cancelable"
            :style="{
              display: 'inline-block',
              position: 'absolute',
              right: '5%',
            }"
          >
            <el-tooltip
              class="item"
              effect="light"
              content="点击取消本次预约"
              placement="left"
            >
              <el-button
                size="mini"
                class="cancel-button"
                @click="cancelReservation"
                round
              >
                取消预约</el-button
              >
            </el-tooltip>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CollapsePanel',
  props: {
    resInfo: {
      type: Object,
      default: () => ({
        submitTime: '2021.4.5 12:00',
        room: {
          name: '301',
          building: {
            name: 'New Building',
            id: '1'
          },
          floor: ''
        },
        applicant: {
          fullname: '王小帅'
        },
        date: '',
        approvalTime: '',
        approvalResult: true,
        approvalPerson: 'XXX',
        arrivalTime: '',
        leaveTime: '',
        applyReason: '这是一段申请理由',
        approveReason: '这是一段审批理由',
        cancelTime: '',
        id: '',
        timeSpan: '',
        token: ''
      })
    }
  },
  data () {
    return {
      isCollapsed: true, // true表示处于折叠状态，false表示处于展开状态
      showTokenText: false,
      switchValue: '隐藏口令'
    }
  },
  computed: {
    startTime () { // 从timeSpan中获取会议室开始使用时间的毫秒级时间戳
      let offset = 0 // 时间间隔为半个小时
      for (let i = 0; i < 48; i++) {
        if (this.resInfo.timeSpan[i] === '1') {
          offset = (i - 16) * 30 * 60
          break
        }
      }
      // 以日期初始化Date，默认时间为早上8:00
      return new Date(this.resInfo.date).getTime() + offset * 1000
    },
    endTime () { // 从timeSpan中获取会议室开始使用时间的毫秒级时间戳
      let offset = 0 // 时间间隔为半个小时
      for (let i = 0; i < 48; i++) {
        if (this.resInfo.timeSpan[i] === '1') {
          offset = (i - 15) * 30 * 60
        }
      }
      return new Date(this.resInfo.date).getTime() + offset * 1000
    },
    arriveLate () {
      if (!this.resInfo.arrivalTime) {
        return false
      } else {
        // let expectedStartTime = new Date(this.resInfo.date).getTime() + this.startTime - 8 * 60 * 60 * 1000
        return new Date(this.resInfo.arrivalTime).getTime() > this.startTime
      }
    },
    leaveLate () {
      if (!this.resInfo.leaveTime) {
        return false
      } else {
        // let expectedEndTime = new Date(this.resInfo.date).getTime() + this.endTime - 8 * 60 * 60 * 1000
        return new Date(this.resInfo.leaveTime).getTime() > this.endTime
      }
    },
    hasBeenApproved () {
      return this.resInfo.approvalTime !== null
    },
    approvalResultString () {
      if (this.resInfo.state === '已过期') {
        return '管理员未及时审批本次预约'
      }
      if (!this.resInfo.approvalTime) {
        return '管理员尚未审批本次预约'
      }
      if (this.resInfo.approvalResult) {
        return '本次预约已经通过审批'
      }
      return '本次预约未通过审批'
    },
    approvalResultBgColor () {
      if (this.resInfo.state === '已撤销' || this.resInfo.state === '已过期') {
        return '#95a5a6'
      }
      if (!this.resInfo.approvalTime) { // 等待审批
        return '#1abc9c'
      }
      if (this.resInfo.state === '已被拒绝' || this.resInfo.state === '签到超时') {
        return '#e74c3c'
      }
      if (this.resInfo.state === '审批通过') {
        return '#9b59b6'
      }
      if (this.resInfo.state === '已完成') {
        return '#2ecc71'
      }
      if (this.resInfo.state === '已完成（晚退）') {
        return '#f39c12'
      }
      return '#1abc9c'
    },
    cancelable () {
      if (this.resInfo.state === '等待审批') {
        return true
      }
      if (!this.resInfo.approvalTime || !this.resInfo.approvalResult ||
        this.resInfo.cancelTime) {
        return false
      }
      let now = new Date() // 获取毫秒级时间戳
      let cancelableLimit = new Date(this.startTime - 30 * 60 * 1000) // 会议开始前半个小时可以取消
      return cancelableLimit > now
    },

    useResultString () { // 待修改
      if (this.resInfo.state === '等待审批') {
        return '等待审批'
      } else if (this.resInfo.state === '审批通过') {
        return '通过审批'
      } else if (this.resInfo.state === '已被拒绝') {
        return '未通过审批'
      } else if (this.resInfo.state === '已撤销') {
        return '已取消预约'
      } else if (this.resInfo.state === '已过期') {
        console.log('已过期')
        return '审批过期'
      } else if (this.resInfo.state === '正在使用') {
        return '正在使用'
      } else if (this.resInfo.state === '已完成') {
        return '已完成使用'
      } else if (this.resInfo.state === '已完成（晚退）') {
        return '使用超时'
      } else if (this.resInfo.state === '签到超时') {
        return '未到场使用'
      }
    },
    stepActiveIndex () {
      let index = 1 // 默认当前处于等待审批状态
      if (this.hasBeenApproved) {
        if (this.resInfo.arrivalTime && this.resInfo.leaveTime) {
          index = 3 // 使用结束
        } else {
          index = 2 // 待使用状态
        }
      }
      return index
    },
    finishStepStatus () {
      if (this.resInfo.state === '已完成') {
        return 'success'
      } else if (this.resInfo.state === '已完成（晚退）') {
        return 'error'
      }
      return 'wait'
    },
    finishStepTitle () {
      if (this.resInfo.state === '已完成') {
        return '按时完成使用'
      } else if (this.resInfo.state === '已完成（晚退）') {
        return '使用超时'
      }
      return '尚未完成使用'
    },
    waitEaxmineStatus () {
      if (this.resInfo.approvalResult) {
        return 'success'
      } else if (this.resInfo.state === '已被拒绝' || this.resInfo.state === '已过期') {
        return 'error'
      } else if (!this.resInfo.approvalResult && this.resInfo.state === '已撤销') { // 尚未审批前就已经撤销
        return 'error'
      }
      return 'finish'
    },
    waitEaxmineTitle () {
      if (this.resInfo.approvalResult) {
        return '通过审批'
      } else if (this.resInfo.state === '已被拒绝') {
        return '未通过审批'
      } else if (this.resInfo.state === '已过期') {
        return '审批过期'
      } else if (!this.resInfo.approvalResult && this.resInfo.state === '已撤销') { // 尚未审批前就已经撤销
        return '已取消预约'
      }
      return '等待审批'
    },
    waitUseStatus () {
      if (!this.resInfo.approvalResult) {
        return 'wait'
      } else if (this.resInfo.state === '已完成' || this.resInfo.state === '已完成（晚退）') {
        return 'success'
      } else if (this.resInfo.state === '签到超时' || this.resInfo.state === '已撤销') {
        return 'error'
      }
      return 'finish'
    },
    waitUseTitle () {
      if (this.resInfo.state === '已完成' || this.resInfo.state === '已完成（晚退）') {
        return '完成使用'
      } else if (this.resInfo.state === '签到超时') {
        return '未到场使用'
      } else if (this.resInfo.state === '已撤销') {
        return '已取消预约'
      } else if (this.resInfo.state === '正在使用') {
        return '正在使用'
      }
      return '等待使用'
    },
    timeSpanString () {
      let startTimeString = new Date(this.startTime).toLocaleTimeString()
      let endTimeString = new Date(this.endTime).toLocaleTimeString()
      return startTimeString + ' - ' + endTimeString
    }
  },
  methods: {
    handleCollapse () {
      this.isCollapsed = !this.isCollapsed
      // console.log(this.isCollapsed)
    },
    cancelReservation () {
      // console.log('emit cancel')
      this.$emit('cancel', this.resInfo)
    },
    tokenVisibleChange (callback) {
      // console.log(callback)
      this.showTokenText = !this.showTokenText
    }
  }
}
</script>

<style scoped>
.collapse-panel {
  width: 100%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid #e3e6f0;
  border-radius: 0.35rem;
  border-left: 0.25rem solid #3498db !important;
  margin: 5px;
}

.panel-header {
  background-color: white;
  color: white;
  box-sizing: border-box;
  text-align: center;
}

.panel-body {
  padding: 10px 2px;
  text-align: left !important;
}

.submit-time {
  display: inline-block;
  background-color: #3498db;
  border: 1px solid rgb(187, 222, 251);
  border-radius: 20px;
  padding: 6px 10px;
  color: white;
  position: relative;
  box-sizing: border-box;
  margin: 2px 0;
}

.room-name {
  display: inline-block;
  background-color: #3498db;
  border: 1px solid rgb(187, 222, 251);
  border-radius: 20px;
  padding: 6px 10px;
  color: white;
  position: relative;
  box-sizing: border-box;
  margin: 2px 0;
}

.res-status {
  color: white;
  padding: 6px 10px;
  border-style: solid;
  border-width: 1px;
  border-radius: 20px;
  position: relative;
  display: inline-block;
  margin: 2px 0;
}

.collapse-button {
  display: inline-block;
  box-sizing: border-box;
  margin-bottom: 2px;
  margin-top: 2px;
  margin-left: 260px;
  width: 50px !important;
  position: absolute;
  right: 1%;
  border: none;
}

.res-step {
  padding: 30px 2px;
  border-top: 1px solid #3498db;
  margin: 5px;
}

.res-item {
  padding: 2px;
  /*border-top: 1px solid rgb(33, 150, 243);*/
  margin: 5px;
}

.res-item div {
  padding: 0;
  border: 0;
  margin: 0;
  text-align: left;
  justify-content: left;
}

.cancel-button {
  display: inline-block;
  box-sizing: border-box;
  background-color: #3498db;
  color: white;
  font-size: medium;
  padding: 2px 10px;
  border-width: 0;
  width: fit-content;
  height: 26px;
}

.token-text {
  display: inline-block;
  font-family: "Times New Roman", serif;
  color: #3498db;
}
</style>
