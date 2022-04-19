<!--会议室终端页-->
<template>
  <el-container style="border: 1px solid #eee">
    <NaviBar ref="NaviBar" />
    <el-container>
      <el-aside>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '10%',
            'font-size': '20px',
          }"
        >
          <span class="el-icon-location"> {{ RoomInfo.name }}</span>
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
        >
          <span class="el-icon-monitor"> 屏幕</span>
          <span class="el-icon-check" v-if="RoomInfo.has_screen" />
          <span class="el-icon-close" v-if="RoomInfo.has_screen === false" />
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
        >
          <span class="el-icon-video-camera"> 投影</span>
          <span class="el-icon-check" v-if="RoomInfo.has_projector" />
          <span class="el-icon-close" v-if="RoomInfo.has_projector === false" />
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
        >
          <span class="el-icon-microphone"> 话筒</span>
          <span class="el-icon-check" v-if="RoomInfo.has_mic" />
          <span class="el-icon-close" v-if="RoomInfo.has_mic === false" />
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
        >
          <span class="el-icon-time">
            {{ NowTime.hour }}:{{ NowTime.minute }}:{{ NowTime.second }}</span
          >
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
          v-if="OnMeeting"
        >
          <span class="el-icon-data-line"> 会议正在进行中</span>
        </div>
        <div
          :style="{
            'justify-content': 'center',
            'text-align': 'center',
            padding: '3%',
          }"
          v-if="OnMeeting === false"
        >
          <span class="el-icon-data-board"> 当前会议室空闲</span>
        </div>
        <el-menu
          default-active="0"
          @select="HandleAsideSelect"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="0"
            ><i class="el-icon-house"></i>会议室信息
          </el-menu-item>
          <el-menu-item index="1"
            ><i class="el-icon-notebook-2"></i>签到
          </el-menu-item>
          <el-menu-item index="2"
            ><i class="el-icon-notebook-2"></i>签退
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!--el-main start-->

      <el-main>
        <div v-show="ShowDetail">
          <!--显示时间栏-->
          <div style="text-align: center">
            <RoomCalendarBlock
              :list="List"
              :today="Today"
              :dayRange="DayRange"
              :active="CalendarButtonActive"
              :hintType="HintType"
            />
          </div>
          <!--显示房间信息-->
          <div style="display: flex">
            <el-card
              class="box-card-blue"
              style="line-height: 250%; width: 70%"
            >
              <div slot="header" class="clearfix">
                <span>会议室信息</span>
              </div>
              <div class="text item">
                {{ "名称： " + RoomInfo.name }}
              </div>
              <div class="text item">
                {{ "所属研究所： " + RoomInfo.institute }}
              </div>
              <div class="text item">
                {{ "楼宇： " + RoomInfo.building }}
              </div>
              <div class="text item">
                {{ "楼层： " + RoomInfo.floor }}
              </div>
              <div class="text item">
                {{ "编号： " + RoomInfo.id }}
              </div>
              <div class="text item">
                {{ "可容纳人数： " + RoomInfo.capacity }}
              </div>
              <div class="text item">
                {{ "备注： " + RoomInfo.note }}
              </div>
            </el-card>
            <el-card class="photo-card">
              <div class="room-photo" style="text-align: center">
                <img
                  src="@/assets/room.jpg"
                  alt="room-photo"
                  style="width: 100%"
                />
              </div>
            </el-card>
          </div>
        </div>
        <div v-show="ShowArrive">
          <!--签到-->
          <el-card class="box-card-blue">
            <div slot="header" class="clearfix">
              <span>签到</span>
            </div>

            <div class="medium-block">
              <span class="demonstration">请输入预约token </span>
            </div>
            <div class="medium-block">
              <el-input v-model="ArriveToken"> </el-input>
            </div>
            <div class="medium-block">
              <el-button @click="SubmitArrive">确认签到</el-button>
            </div>
          </el-card>
        </div>
        <div v-show="ShowLeave">
          <!--签到-->
          <el-card class="box-card-orange">
            <div slot="header" class="clearfix">
              <span>签退</span>
            </div>

            <div class="medium-block">
              <span class="demonstration">请输入预约token </span>
            </div>
            <div class="medium-block">
              <el-input v-model="LeaveToken"> </el-input>
            </div>
            <div class="medium-block">
              <el-button @click="SubmitLeave">确认签退</el-button>
            </div>
          </el-card>
        </div>
      </el-main>

      <!--el-main end-->
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
import RoomCalendarBlock from '@/components/RoomCalendarBlock.vue'
import { TerminalRoomInfo, TerminalArrive, TerminalLeave } from '@/utils/communication.js'

export default {
  name: 'Terminal',
  inject: ['PageReload'],
  components: {
    NaviBar,
    FooterBar,
    RoomCalendarBlock
  },
  data () {
    return {
      RoomInfo: {
        /* 该会议室信息
        id: 房间id int
        floor: 房间所在楼层 int
        name: 房间名 string
        capacity: 容量 int
        stu_allowed: True|False 学生可否预约
        cs_only: 是否仅计算机系师生可预约
        building: 'NewBuilding'（新系馆）|'EastPrime'（东主楼）
        institute: 归属的研究所id，公用则为null
        time_span: 房间预约情况，day_range个48位2进制[0,1]字符串组成的list，1表示已被预约
        today: 当前日期 string 用于0点瞬间前后端统一日期
        day_range: 表示会给出接下来多少天的房间预约情况
      */},
      ShowDetail: true,
      ShowArrive: false,
      ShowLeave: false,
      OnMeeting: false,
      ArriveToken: '',
      LeaveToken: '',

      // 时间框显示需求
      List: [], // 含该房间的RoomInfo
      Today: '', // 今天
      DayRange: 0, // 可预约时间段
      CalendarButtonActive: false, // 禁用按钮
      HintType: 2, // 禁用无关显示

      // 定时刷新
      Timer: null,
      NowTime: {
        hour: '08',
        minute: '00',
        second: '00'
      }
    }
  },
  methods: {
    HandleAsideSelect (key) {
      if (key === '0') { // 会议室信息
        this.ShowDetail = true
        this.ShowArrive = false
        this.ShowLeave = false
      } else if (key === '1') { // 签到
        this.ShowDetail = false
        this.ShowArrive = true
        this.ShowLeave = false
      } else if (key === '2') { // 签退
        this.ShowDetail = false
        this.ShowArrive = false
        this.ShowLeave = true
      }
    },
    SubmitArrive () { // 确认签到
      if (this.ArriveToken.length === 0) { // token为空
        this.$message({
          type: 'error',
          message: 'token不能为空!',
          duration: 3000
        })
        return
      }
      TerminalArrive(this.ArriveToken).then((r) => {
        if (r['code'] === 200) { // 成功签到
          let time = r['data']['time_span']
          let begin, end// 获取该签到用户预约的时间段
          for (let i = 0; i < 48; i++) {
            if (time[i] !== '0') {
              begin = i
              break
            }
          }
          for (let i = begin + 1; i < 48; i++) {
            if (time[i] === '0') {
              end = i
              break
            }
          }
          let starthour = Math.floor(begin / 2)
          let startmin = begin % 2 === 0 ? '00' : '30'
          let endhour = Math.floor(end / 2)
          let endmin = end % 2 === 0 ? '00' : '30'
          this.$message({
            type: 'success',
            message: '您已成功签到今日' + starthour.toString() + ':' + startmin + '至' + endhour.toString() + ':' + endmin + '的会议!',
            duration: 6000
          })
        } else if (r['code'] === 210) { // 不在正常的到达时间段内
          this.$message({
            type: 'info',
            message: '不在正常的到达时间段内!',
            duration: 3000
          })
        } else if (r['code'] === 212) { // 已经签到
          this.$message({
            type: 'info',
            message: '您已签到!',
            duration: 3000
          })
        } else { // token错误
          this.$message({
            type: 'error',
            message: 'token错误!',
            duration: 3000
          })
        }
      })
    },
    SubmitLeave () { // 确认签退
      if (this.LeaveToken.length === 0) { // token为空
        this.$message({
          type: 'error',
          message: 'token不能为空!',
          duration: 3000
        })
        return
      }
      TerminalLeave(this.LeaveToken).then((r) => {
        if (r['code'] === 200) { // 成功签退
          this.$message({
            type: 'success',
            message: '签退成功!',
            duration: 3000
          })
        } else if (r['code'] === 210) { // 还未签到
          this.$message({
            type: 'info',
            message: '您还未签到!',
            duration: 3000
          })
        } else if (r['code'] === 211) { // 晚退
          this.$message({
            type: 'info',
            message: '您晚退了!',
            duration: 3000
          })
        } else { // token错误
          this.$message({
            type: 'error',
            message: 'token错误!',
            duration: 3000
          })
        }
      })
    },
    SetData (res) {
      // 基本信息
      this.RoomInfo = res['data']
      let date = new Date()
      let val = date.getHours() * 2 + Math.floor(date.getMinutes() / 30)
      if (val >= 16 && val < 46 && this.RoomInfo.time_span[0][val] === '1') { // 正在进行会议
        this.OnMeeting = true
      }
      // 信息转化
      if (this.RoomInfo.institute != null) {
        this.RoomInfo.institute = this.RoomInfo.institute.name
      } else {
        this.RoomInfo.institute = '系属'
      }
      this.RoomInfo.building = this.RoomInfo.building.id === 1 ? '新系馆' : '东主楼'
      this.RoomInfo.note = (this.RoomInfo.note === null || this.RoomInfo.note.length === 0) ? '无' : this.RoomInfo.note

      // 设置时间框信息
      this.Today = this.RoomInfo.today
      this.DayRange = 1
      let tmplist = []
      tmplist.push(this.RoomInfo)
      let nowdate = new Date()// 当前时间
      let alreadypass = nowdate.getHours() * 2 + Math.floor(nowdate.getMinutes() / 30)

      let tmpstring = ''
      for (let j = 0; j < 48; j++) {
        if (j <= alreadypass) { // 时间已经过去，不接受预约
          tmpstring += '1'
        } else {
          tmpstring += tmplist[0].time_span[j]
        }
      }
      tmplist[0].time_span = []
      tmplist[0].time_span.push(tmpstring)// 修改今天的timespan
      tmplist[0].string = tmpstring// 增加string属性以用于时间栏显示
      this.List = tmplist
    },
    TimeEvent () { // 定时触发事件
      let date = new Date()

      this.NowTime.hour = date.getHours() < 10 ? '0' + date.getHours().toString() : date.getHours().toString()
      this.NowTime.minute = date.getMinutes() < 10 ? '0' + date.getMinutes().toString() : date.getMinutes().toString()
      this.NowTime.second = date.getSeconds() < 10 ? '0' + date.getSeconds().toString() : date.getSeconds().toString()
      if (date.getMinutes() % 5 === 0 && date.getSeconds() === 0) {
        this.PageReload()
      }
    }
  },
  mounted () { // 打开时进行验证
    let apiToken = readCookie('terminal_token')
    if (apiToken.length !== 0) { // 只要token存在就能进一步验证
      TerminalRoomInfo().then((res) => {
        if (res['code'] === 200) { /// 成功获取信息
          this.TimeEvent()
          this.$refs.NaviBar.LoginStatus('-1')
          this.Timer = setInterval(() => {
            this.TimeEvent()
          }, 1000)
          this.SetData(res)
        } else { // 不成功则返回主页
          this.$router.push('/')
        }
      })
    } else {
      this.$router.push('/')
    }
  },
  destroyed () {
    clearInterval(this.Timer)
  }
}
</script>

<style scoped>
.header {
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #fff;
  height: 15% !important;
}

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
  line-height: 200%;
  width: 20% !important;
}

.el-main {
  height: auto;
  border-left: 1px solid #e6e6e6;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card-blue {
  width: 100%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid #e3e6f0;
  border-radius: 0.35rem;
  border-left: 0.25rem solid #4e73df !important;
  margin: 5px;
}

.box-card-orange {
  width: 100%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid blanchedalmond;
  border-radius: 0.35rem;
  border-left: 0.25rem solid darkorange !important;
  margin: 5px;
}

.medium-block {
  margin: 20px;
}
.photo-card {
  width: 100%;
  padding: 0;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid #e3e6f0;
  border-radius: 0.35rem;
  border-left: 0.25rem solid #fff !important;
  margin: 5px;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}
</style>
