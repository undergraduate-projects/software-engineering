<template>
  <el-container v-loading="Loading">
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
        <el-menu
          default-active="0"
          @select="HandleAsideSelect"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="0"
            ><i class="el-icon-house"></i>会议室信息
          </el-menu-item>
          <el-menu-item index="1"
            ><i class="el-icon-date"></i>预约
          </el-menu-item>
          <el-menu-item index="4" v-if="isAdmin">
            <i class="el-icon-document"></i>使用记录
          </el-menu-item>
          <el-menu-item index="3"
            ><i class="el-icon-question"></i>预约条件
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!--el-main start-->

      <el-main>
        <div v-show="ShowDetail" style="display: flex">
          <!--显示房间信息-->
          <el-card class="box-card-blue" style="line-height: 250%; width: 70%">
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
              {{ "类型： " + RoomInfo.size }}
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
        <div v-if="ShowReservation">
          <!--预约-->
          <el-card class="box-card-blue">
            <div slot="header" class="clearfix">
              <span>预约</span>
            </div>

            <div class="medium-block">
              <!-- <span class="demonstration" style="margin: 0px 20px 0px 0px"
                >预约时间段
              </span> -->
              <el-row :gutter="15" class="legend" type="flex" align="middle">
                <el-col :span="1.5"> <span class="not_available" /> </el-col>
                <el-col :span="4">
                  <span class="legend_text">不可用 & 已被预约</span>
                </el-col>
                <el-col :span="1.5"> <span class="self_applied" /> </el-col>
                <el-col :span="3">
                  <span class="legend_text">自己正在申请</span>
                </el-col>
                <el-col :span="1.5"> <span class="self_reserved" /> </el-col>
                <el-col :span="3">
                  <span class="legend_text">自己已预约</span>
                </el-col>
              </el-row>

              <el-tabs v-model="active_date">
                <el-tab-pane
                  v-for="date in dates"
                  :key="date.index"
                  :label="date.date"
                  :name="date.index"
                >
                </el-tab-pane>
              </el-tabs>
              <el-row>
                <el-col :xl="20">
                  <el-slider
                    class="range_slider"
                    range
                    v-model="sliderRange"
                    :format-tooltip="formatTooltip"
                    :marks="slider_marks"
                    :style="slider_style"
                    :min="0"
                    :max="30"
                  >
                  </el-slider>
                </el-col>
              </el-row>
            </div>
            <div class="medium-block">
              <span class="demonstration">预约理由</span>
              <span
                class="demonstration"
                style="margin: 0px 0px 0px 20px; color: #aaaaaa"
                >理由不超过200字</span
              >
              <el-input
                type="textarea"
                :rows="5"
                placeholder="填写理由"
                v-model="ReservationReason"
                style="margin: 10px 0px 0px 0px"
              >
              </el-input>
            </div>
            <div class="medium-block">
              <el-button @click="SubmitReservation">提交预约申请</el-button>
            </div>
          </el-card>
        </div>
        <div v-show="ShowPrerequisite">
          <!--          展示房间的使用先决条件-->
          <el-card class="box-card-green">
            <div slot="header" class="clearfix">
              <span>可预约群体</span>
            </div>
            <div
              v-if="!RoomInfo.teacher_only && !RoomInfo.cs_only"
              class="text item"
            >
              <span>全体师生</span>
            </div>
            <div
              v-if="!RoomInfo.teacher_only && RoomInfo.cs_only"
              class="text item"
            >
              <span>全体计算机系师生</span>
            </div>
            <div
              v-if="RoomInfo.teacher_only && RoomInfo.cs_only"
              class="text item"
            >
              <span>全体计算机系教职工</span>
            </div>
            <div
              v-if="RoomInfo.teacher_only && !RoomInfo.cs_only"
              class="text item"
            >
              <span>全体教职工</span>
            </div>
          </el-card>
          <el-card class="box-card-red">
            <div slot="header" class="clearfix">
              <span>不可预约群体</span>
            </div>
            <div
              v-if="RoomInfo.cs_only && !RoomInfo.teacher_only"
              class="text item"
            >
              <span>非计算机系师生</span>
            </div>
            <div
              v-else-if="RoomInfo.teacher_only && !RoomInfo.cs_only"
              class="text item"
            >
              <span>全体学生</span>
            </div>
            <div
              v-else-if="RoomInfo.teacher_only && RoomInfo.cs_only"
              class="text item"
            >
              <span>非计算机系师生及计算机系学生</span>
            </div>
            <div v-else class="text item">
              <span>无</span>
            </div>
          </el-card>
          <el-card class="box-card-orange">
            <div slot="header" class="clearfix">
              <span>预约须知</span>
            </div>
            <div v-for="text in ReserveRules" :key="text" class="text item">
              {{ text }}
            </div>
          </el-card>
        </div>

        <div v-if="showRoomResHistory">
          <el-table :data="filteredRoomResList">
            <el-table-column type="expand" min-width="60">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="审批人：">
                    <span>{{ props.row.approval_person }}</span>
                  </el-form-item>
                  <el-form-item label="审批时间：">
                    <span>{{
                      new Date(props.row.approval_time).toLocaleDateString() +
                      " " +
                      new Date(props.row.approval_time).toLocaleTimeString()
                    }}</span>
                  </el-form-item>
                  <el-form-item label="签到时间：">
                    <span v-if="props.row.arrival_time">{{
                      new Date(props.row.arrival_time).toLocaleDateString() +
                      " " +
                      new Date(props.row.arrival_time).toLocaleTimeString()
                    }}</span>
                    <span v-else>无</span>
                  </el-form-item>
                  <el-form-item label="签退时间：">
                    <span v-if="props.row.leave_time">{{
                      new Date(props.row.leave_time).toLocaleDateString() +
                      " " +
                      new Date(props.row.leave_time).toLocaleTimeString()
                    }}</span>
                    <span v-else>无</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <!--常规表格-->
            <el-table-column label="申请人" align="center" min-width="100">
              <template slot-scope="scope">
                <span>{{ scope.row.applicant.fullname }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="申请使用时间"
              align="center"
              min-width="250"
            >
              <template slot-scope="scope">
                <span>{{
                  getTimeSpanString(scope.row.date, scope.row.time_span)
                }}</span>
              </template>
            </el-table-column>
            <el-table-column label="使用情况" align="center" min-width="150">
              <template slot-scope="scope">
                <el-tag v-if="scope.row.state === '已完成'" type="success">{{
                  scope.row.state
                }}</el-tag>
                <el-tag
                  v-if="scope.row.state === '已完成（晚退）'"
                  type="warning"
                  >{{ scope.row.state }}</el-tag
                >
                <el-tag v-if="scope.row.state === '签到超时'" type="danger">{{
                  scope.row.state
                }}</el-tag>
                <el-tag v-if="scope.row.state === '正在使用'">{{
                  scope.row.state
                }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            background
            @current-change="handleCurrentChange"
            layout="prev, pager, next, total, jumper"
            :total="resTotalCount"
            v-if="filteredRoomResList.length !== 0"
            :style="{ textAlign: 'center' }"
          >
          </el-pagination>
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
import { CheckToken, GetRoomInfo, RoomReserve, GetRoomReservation } from '@/utils/communication.js'
import { reservationTips } from '@/data/roomdata.js'

export default {
  name: 'RoomInfo',
  components: {
    NaviBar,
    FooterBar
  },
  data () {
    return {
      // 以下为页面的显示与隐藏绑定
      ShowDetail: true,
      ShowReservation: false,
      ShowHistory: false,
      ShowPrerequisite: false,
      Loading: false,
      isAdmin: false, // 登录人是否管理该会议室
      showRoomResHistory: false,

      roomResList: [],
      filteredRoomResList: [], // 可用于筛选
      resPageCount: 0, // 分页数
      resTotalCount: 0, // 总记录数

      // 以下为房间基本信息
      ReserveRules: reservationTips, // 预约须知
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
        time_span: 房间预约情况，day_range个48位4进制[0,1,2,3]字符串组成的list
                   1表示已被预约，2表示当前用户成功预约的，3表示当前用户正在申请
        current_user_allowed: 是否允许当前用户预约
        note: 房间备注，为空则为None
        has_screen
        has_projector
        has_mic
      */},
      ReservationList: [], // 预约列表
      RoomId: 1, // 该房间id

      // 时间框显示需求
      List: [], // 含该房间的RoomInfo
      Today: '', // 今天
      DayRange: 0, // 可预约时间段
      CalendarButtonActive: false,

      // 以下用于预约
      DayPickerOptions: {// 日期栏的属性

      },
      ReservationReason: '', // 预约理由
      dates: [],
      active_date: '0',
      sliderRange: [0, 0],
      slider_marks: {},
      sliderValid: true
    }
  },
  methods: {
    HandleAsideSelect (key) {
      if (key === '0') { // 展示房间详细信息
        this.ShowDetail = true
        this.ShowReservation = false
        this.ShowHistory = false
        this.ShowPrerequisite = false
        this.showRoomResHistory = false
      } else if (key === '1') { // 展示房间预约主界面
        this.ShowReservation = true
        this.ShowDetail = false
        this.ShowHistory = false
        this.ShowPrerequisite = false
        this.showRoomResHistory = false
      } else if (key === '2') { // 展示房间使用记录
        this.ShowDetail = false
        this.ShowReservation = false
        this.ShowHistory = true
        this.ShowPrerequisite = false
        this.showRoomResHistory = false
      } else if (key === '3') { // 展示房间使用先决条件
        this.ShowDetail = false
        this.ShowReservation = false
        this.ShowHistory = false
        this.ShowPrerequisite = true
        this.showRoomResHistory = false
      } else if (key === '4') { // 展示房间的历史使用记录
        this.ShowDetail = false
        this.ShowReservation = false
        this.ShowHistory = false
        this.ShowPrerequisite = false
        this.showRoomResHistory = true
        this.getRoomResHistory(1)
      }
    },
    getRoomResHistory (pageNum) {
      GetRoomReservation(this.RoomId, pageNum).then((res) => {
        console.log(res)
        this.roomResList = res['data']['list']
        this.filteredRoomResList = res['data']['list']
        this.resTotalCount = res['data']['total']
        this.resPageCount = res['data']['page_count']
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '获取使用记录失败!',
          duration: 3000
        })
      })
    },
    handleCurrentChange (val) {
      this.getRoomResHistory(val)
    },
    SubmitReservation () { // 提交预约申请
      let start = this.sliderRange[0] + 16
      let end = this.sliderRange[1] + 16
      if (start === end) { // 预约区间为0
        this.$message({
          type: 'error',
          message: '预约区间不能为0!',
          duration: 3000
        })
        return
      }
      if (end - start > 8) { // 预约区间过长
        this.$message({
          type: 'error',
          message: '预约区间不能超过4小时！',
          duration: 3000
        })
        return
      }
      if (!this.sliderValid) {
        this.$message({
          type: 'error',
          message: '预约区间重合！',
          duration: 3000
        })
      }
      let timeSpan = ''
      for (let i = 0; i < 48; i++) { // 填充timeSpan
        if (i >= start && i < end) { // 要预约的时间
          timeSpan += '1'
        } else {
          timeSpan += '0'
        }
      }

      // 再判断预约理由的合法性
      if (this.ReservationReason.length === 0) { // 预约理由为空
        this.$message({
          type: 'info',
          message: '必须填写预约理由！',
          duration: 3000
        })
        return
      }
      if (this.ReservationReason.length >= 200) { // 预约理由太长
        this.$message({
          type: 'info',
          message: '预约理由太长！',
          duration: 3000
        })
        return
      }

      // 计算时间
      let resDate = new Date(this.Today)
      resDate.setDate(resDate.getDate() + parseInt(this.active_date))

      let dateStr = `${resDate.getFullYear()}-${resDate.getMonth() + 1}-${resDate.getDate()}`

      // 成功通过检查，发送请求
      RoomReserve(this.RoomId, dateStr, timeSpan, this.ReservationReason).then((r) => {
        if (r['code'] === 432) { // 预约时间冲突
          this.$message({
            type: 'error',
            message: '与自己预约的其他时间冲突！',
            duration: 3000
          })
        } else if (r['code'] !== 200) { // 申请失败
          this.$message({
            type: 'error',
            message: '申请失败！',
            duration: 3000
          })
        } else { // 申请成功
          this.$message({
            type: 'success',
            message: '申请成功！',
            duration: 3000
          })
          GetRoomInfo(this.RoomId).then((res) => { // 更新信息
            this.SetData(res)
          })
        }
      }
      )
    },
    getTimeSpanString (date, timeSpan) {
      let offset1 = 0 // 时间间隔为半个小时
      let offset2 = 0
      for (let i = 0; i < 48; i++) {
        if (timeSpan[i] === '1') {
          offset1 = (i - 16) * 30 * 60
          break
        }
      }
      for (let i = 0; i < 48; i++) {
        if (timeSpan[i] === '1') {
          offset2 = (i - 15) * 30 * 60
        }
      }
      let startTime = offset1 * 1000
      let startTimeString = new Date(startTime).toLocaleTimeString()
      let endTime = offset2 * 1000
      let endTimeString = new Date(endTime).toLocaleTimeString()
      let dateString = new Date(date).toLocaleDateString()
      return dateString + ' ' + startTimeString + ' - ' + endTimeString
    },
    SetData (res) { // 根据返回的数据设置信息
      this.Today = res['data']['today']
      this.DayRange = res['data']['day_range']
      this.RoomInfo = res['data']['room_list'][0]

      this.isAdmin = this.RoomInfo.admin

      // 预约成功后重置
      this.ReservationReason = ''
      this.active_date = '0'

      // 填充dates，用于tab
      let d = new Date(this.Today)
      this.dates = []
      for (let i = 0; i < this.DayRange; i++) {
        this.dates.push({
          'index': i.toString(),
          'date': `${d.getMonth() + 1}月${d.getDate()}日`
        })
        d.setDate(d.getDate() + 1)
      }

      if (this.DayRange === 7) {
        this.DayPickerOptions = {
          disabledDate (time) { // 禁用掉不能预约的日期
            let date = new Date()
            date.setDate(date.getDate() - 1)// 之前的禁用
            if (time.getTime() < date.getTime()) { return true }
            date.setDate(date.getDate() + 7)// 7天之后禁用
            if (time.getTime() > date.getTime()) { return true }
            return false
          }
        }
      } else {
        this.DayPickerOptions = {
          disabledDate (time) { // 禁用掉不能预约的日期
            let date = new Date()
            date.setDate(date.getDate() - 1)// 之前的禁用
            if (time.getTime() < date.getTime()) { return true }
            date.setDate(date.getDate() + 14)// 14天之后禁用
            if (time.getTime() > date.getTime()) { return true }
            return false
          }
        }
      }

      let tmplist = []
      tmplist.push(this.RoomInfo)
      let nowdate = new Date()// 当前时间
      let alreadypass = nowdate.getHours() * 2 + Math.floor(nowdate.getMinutes() / 30)

      // 将滑条放在无效时间后
      this.sliderRange = [
        (alreadypass >= 16) ? alreadypass - 16 + 1 : 0,
        (alreadypass >= 16) ? alreadypass - 16 + 1 : 0
      ]
      for (let i = 0; i < tmplist.length; i++) {
        let tmpstring = ''
        for (let j = 0; j < 48; j++) {
          if (j <= alreadypass) { // 时间已经过去，不接受预约；或是与已经预约的时间段冲突
            tmpstring += '1'
          } else {
            tmpstring += tmplist[i].time_span[0][j]
          }
        }
        tmplist[i].time_span[0] = tmpstring// 修改今天的timespan
      }
      for (let i = 0; i < this.DayRange; i++) {
        let tmpstring = ''
        for (let j = 0; j < 48; j++) {
          if (res['data']['waiting_time_span'][i][j] === '1' && tmplist[0].time_span[i][j] === '0') { // 时间与已经预约的时间段冲突
            tmpstring += '1'
          } else {
            tmpstring += tmplist[0].time_span[i][j]
          }
        }
        tmplist[0].time_span[i] = tmpstring// 修改今天的timespan
      }

      this.List = tmplist
      /* res['data']['reservation_info'].forEach((elem) => {
        if (elem['approval_time'] !== null) {
          elem['timeString'] = this.startTimeString(elem['date'], elem['time_span']) +
            ' —— ' + this.endTimeString(elem['date'], elem['time_span'])
          this.ReservationList.push(elem)
        }
      }) */
      // 信息转化
      if (this.RoomInfo.institute != null) {
        this.RoomInfo.institute = this.RoomInfo.institute.name
      } else {
        this.RoomInfo.institute = '系属'
      }
      if (this.RoomInfo.size === 'L') {
        this.RoomInfo.size = '大型'
      } else if (this.RoomInfo.size === 'M') {
        this.RoomInfo.size = '中型'
      } else {
        this.RoomInfo.size = '小型'
      }
      this.RoomInfo.building = this.RoomInfo.building.id === 1 ? '新系馆' : '东主楼'
      this.RoomInfo.note = (this.RoomInfo.note === null || this.RoomInfo.note.length === 0) ? '无' : this.RoomInfo.note
    },
    formatTooltip (value) {
      return (Math.floor(value / 2) + 8).toString().padStart(2, '0') + ':' +
        (value % 2 * 30).toString().padStart(2, '0')
    }
  },
  mounted () {
    this.Loading = true
    this.RoomId = this.$route.params.RoomId
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('0')
          GetRoomInfo(this.RoomId).then((res) => {
            if (res['code'] !== 200) { // 会议室不存在
              this.$message({
                type: 'error',
                message: '会议室不存在！',
                duration: 3000
              })
              this.$router.push('/RoomReserve')
            } else { // 正确，设置信息
              this.SetData(res)
              for (let i = 0; i <= 15; i++) {
                this.slider_marks[i * 2] = `${i + 8}:00`
              }
              for (let i = 0; i < 15; i++) {
                this.slider_marks[i * 2 + 1] = ''
              }
              this.Loading = false
            }
          })
        } else { // 登录无效
          this.$router.push('/')
        }
      })
    }
  },
  computed: {
    slider_style () {
      let colors = []
      const min = 0
      const max = 30
      const range = max - min

      const color = ['transparent', '#A6ACAF', '#94DC5A', '#F8C471'] // 对应0123

      let span = this.List[0].time_span[parseInt(this.active_date)]
      let status = 0
      let now = 0
      for (let i = 16; i < 46; i++) {
        now = parseInt(span[i])
        if (now !== status) {
          colors.push(`${color[status]} ${(i - 16) / range * 100}%`)
          colors.push(`${color[now]} ${(i - 16) / range * 100}%`)
          status = now
        }
      }
      colors.push(`${color[status]} 100%`)

      status = 0
      let activeColors = []
      let left = this.sliderRange[0]
      let right = this.sliderRange[1]
      const activeRange = right - left
      let valid = true
      for (let i = left + 16; i < right + 16; i++) {
        now = parseInt(span[i])
        if (now !== status) {
          activeColors.push(`${color[status]} ${(i - 16 - left) / activeRange * 100}%`)
          activeColors.push(`${color[now]} ${(i - 16 - left) / activeRange * 100}%`)
          status = now
          valid = false
        }
      }
      activeColors.push(`${color[status]} 100%`)

      let colorInvalid = '#409EFF'
      let colorButton = 'white'
      if (!valid) {
        colorInvalid = '#EC7063'
        colorButton = '#FDEDEC'
      }
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.sliderValid = valid

      return {
        '--track-bg': `linear-gradient(to right,${colors.join(',')})`,
        '--active-track-bg': `linear-gradient(to right,${activeColors.join(',')})`,
        '--slider-color': colorInvalid,
        '--slider_button_bg': colorButton
      }
    }
  }
}
</script>

<style>
/* 滑条颜色 */
.range_slider {
  margin-bottom: 40px;
}
.el-slider__runway {
  background-image: var(--track-bg);
}
.el-slider__bar {
  background-image: var(--active-track-bg);
}
.el-slider__button {
  border: 2px solid var(--slider-color);
  background-color: var(--slider_button_bg);
}

/* 图例 */
.legend {
  margin-bottom: 20px;
}
.legend .not_available {
  display: flex;
  width: 35px;
  height: 8px;
  background-color: #a6acaf;
  border-radius: 25px;
}
.legend .self_applied {
  display: block;
  width: 35px;
  height: 8px;
  background-color: #f8c471;
  border-radius: 25px;
}
.legend .self_reserved {
  display: block;
  width: 35px;
  height: 8px;
  background-color: #94dc5a;
  border-radius: 25px;
}
.legend .legend_text {
  color: #727577;
  font-size: 15px;
}

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
  line-height: 200%;
  height: auto;
  width: 20% !important;
}

.el-main {
  height: auto;
  border-left: 1px solid #e6e6e6;
}
.el-menu {
  border-right: none;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
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

.box-card-red {
  width: 100%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid lightgoldenrodyellow;
  border-radius: 0.35rem;
  border-left: 0.25rem solid crimson !important;
  margin: 5px;
}

.box-card-green {
  width: 100%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid lightgoldenrodyellow;
  border-radius: 0.35rem;
  border-left: 0.25rem solid rgb(180, 226, 109) !important;
  margin: 5px;
}

.small-block {
  margin: 10px;
}
.medium-block {
  margin: 20px;
}
.big-block {
  margin: 30px;
}

.demo-table-expand {
  font-size: 0;
  margin-left: 45px;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
