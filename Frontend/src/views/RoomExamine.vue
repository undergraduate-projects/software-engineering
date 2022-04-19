<template>
  <el-container>
    <NaviBar ref="NaviBar" />
    <el-container class="container">
      <el-main class="main_examine">
        <div>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="查看等待审批" name="first"></el-tab-pane>
          <el-tab-pane label="查看审批记录" name="second"></el-tab-pane>
        </el-tabs>
        <el-table
          v-loading.fullscreen="loading"
          :data="ReserveList"
          key="ReserveList"
          stripe
          :style="{ width: '100%' }"
          :cell-style="cellStyle"
        >
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="conflict_expand">
                <el-form-item label="学号">
                  <span>{{ props.row.uid }}</span>
                </el-form-item>
                <el-form-item label="身份">
                  <span>{{ props.row.is_teacher }}</span>
                </el-form-item>
                <el-form-item label="研究所">
                  <span>{{ props.row.institute }}</span>
                </el-form-item>
                <el-form-item label="提交时间">
                  <span>{{ props.row.submit_time }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            label="序号"
            prop="orderId"
            min-width="50"
            align="center"
          />

          <el-table-column
            label="预约人"
            prop="fullname"
            min-width="120"
            align="center"
          />

          <el-table-column
            label="预约时间段"
            prop="time_range"
            min-width="220"
            align="center"
          />

          <el-table-column label="预约房间" min-width="200" align="center">
            <template slot-scope="scope0">
              <el-button
                type="text"
                @click="
                  showroominfo(scope0.row.roomid);
                  dialog_room_info_visible = true;
                "
                >{{ scope0.row.reserveroom }}</el-button
              >

              <el-dialog
                class="dialog_room_info"
                title="详细信息"
                :visible.sync="dialog_room_info_visible"
                :append-to-body="true"
                :close-on-click-modal="false"
                center
                @close="
                  dialog_room_info_visible = false;
                  cleanData();
                "
              >
                <el-form label-position="center" style="text-align: center">
                  <!-- 第一行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="会议室名称:"
                    v-model="roominfo_name"
                    label-width="170px"
                    >{{ roominfo_name }}
                  </el-form-item>

                  <!-- 第二行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="地点:"
                    v-model="roominfo_site"
                    label-width="170px"
                    >{{ roominfo_site }}
                  </el-form-item>

                  <!-- 第三行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="容纳人数:"
                    v-model="roominfo_capacity"
                    label-width="170px"
                    >{{ roominfo_capacity }}
                  </el-form-item>

                  <!-- 第四行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="归属研究所:"
                    v-model="roominfo_institute"
                    label-width="170px"
                    color="#999"
                    >{{ roominfo_institute }}
                  </el-form-item>

                  <!-- 第五行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="预约权限:"
                    v-model="roominfo_csonly"
                    label-width="170px"
                  >
                    {{ roominfo_csonly }}
                  </el-form-item>

                  <!-- 第六行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="提供设备:"
                    v-model="roominfo_equip"
                    label-width="170px"
                  >
                    {{ roominfo_equip }}
                  </el-form-item>

                  <!-- 第七行  -->
                  <el-form-item
                    class="roominfo_item"
                    label="房间备注:"
                    v-model="roominfo_note"
                    label-width="170px"
                    >{{ roominfo_note }}
                  </el-form-item>
                </el-form>
                <span slot="footer">
                  <div align="center">
                    <el-button
                      type="primary"
                      @click="
                        dialog_room_info_visible = false;
                        cleanData();
                      "
                      >确认
                    </el-button>
                  </div>
                </span>
              </el-dialog>
            </template>
          </el-table-column>

          <el-table-column
            label="预约原因"
            prop="apply_reason"
            min-width="150"
            align="center"
          />
          <el-table-column
            label="审批时间"
            prop="approval_time"
            min-width="150"
            align="center"
            key="2"
            v-if="examine_result_show"
            v-show="examine_result_show"
          ></el-table-column>
          <el-table-column
            label="当前状态"
            prop="state"
            min-width="150"
            align="center"
            key="0"
            v-if="examine_result_show"
            v-show="examine_result_show"
          ></el-table-column>

          <el-table-column
            label="审批"
            min-width="150"
            align="center"
            key="1"
            v-if="examine_show"
            v-show="examine_show"
          >
            <template slot-scope="scope">
              <el-button
                size="small"
                type="success"
                v-show="examine_show"
                @click="
                  setAgreeId(scope.row.id);
                  setResultTrue();
                  agree();
                "
                >同意</el-button
              >

              <!-- 预约时间冲突对话框 -->
              <el-dialog
                class="dialog_conflict"
                title="以下预约与当前预约存在时间和地点上的冲突，是否全部拒绝？"
                :visible.sync="dialog_conflict_visible"
                :append-to-body="true"
                :close-on-click-modal="false"
                center
                @close="dialog_conflict_visible = false"
                :lock-scroll="false"
              >
                <el-table :data="ConflictList" :key="11">
                  <el-table-column
                    label="预约人"
                    prop="applicant.fullname"
                    width="80"
                    align="center"
                  >
                  </el-table-column>

                  <el-table-column
                    label="身份"
                    prop="applicant.is_teacher"
                    width="80"
                    align="center"
                  >
                  </el-table-column>

                  <el-table-column
                    label="预约时间段"
                    prop="time_range"
                    width="200"
                    align="center"
                  >
                  </el-table-column>
                  <el-table-column
                    label="预约理由"
                    prop="apply_reason"
                    width="150"
                    align="center"
                  >
                  </el-table-column>
                </el-table>
                <el-pagination
                  @current-change="conflictpage_Change"
                  layout="total, prev, pager, next, jumper"
                  :total="conflict_total"
                  :current-page="conflictpage"
                  :page-size="3"
                  background
                  hide-on-single-page
                  style="margin-top: 30px"
                >
                </el-pagination>
                <span slot="footer">
                  <el-button
                    type="danger"
                    @click="
                      refuse_conflict(), (dialog_conflict_visible = false)
                    "
                    >全部拒绝</el-button
                  >
                  <el-button type="big" @click="dialog_conflict_visible = false"
                    >取消</el-button
                  >
                </span>
              </el-dialog>
              <!----------------------->

              <el-button
                @click="
                  dialog_refuse_visible = true;
                  setRefuserId(scope.row.id);
                "
                size="small"
                type="danger"
                v-show="examine_show"
                >拒绝</el-button
              >

              <el-dialog
                class="dialog_examine"
                title="拒绝理由"
                :visible.sync="dialog_refuse_visible"
                :append-to-body="true"
                :close-on-click-modal="false"
                @close="dialog_refuse_visible=false;clean_input()"
                style="height:max-content"
              >
                <el-form :model="examineForm">
                  <el-form-item>
                    <el-select v-model="value" placeholder="请选择理由" @change="select_change">
                      <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item style="height: 50px" prop="refuseText">
                    <el-input
                      type="textarea"
                      v-model="examineForm.refuseText"
                      maxlength="300"
                      :autosize="{ minRows: 5, maxRows: 5 }"
                      resize="none"
                      show-word-limit
                    >
                    </el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer">
                  <div align="center">
                    <el-button @click="dialog_refuse_visible = false;clean_input()" style="margin-top:20px">取消</el-button>
                    <el-button
                      type="primary"
                      @click="setResultFalse();refuse();clean_input()" style="margin-top:20px">确认</el-button>
                  </div>
                </span>
              </el-dialog>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @current-change="handleCurrentChange"
          layout="total, prev, pager, next, jumper"
          :total="examine_total"
          :current-page="pagenumber"
          background
          hide-on-single-page
        >
        </el-pagination>
        </div>
      </el-main>
    </el-container>
    <el-footer>
      <FooterBar/>
    </el-footer>
  </el-container>
</template>

<script>

import { readCookie } from '@/utils/cookies.js'
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import { CheckToken, GetUserInfo, ExamineReservation, GetRoomInfo, GetExamResList, GetConflictList } from '@/utils/communication.js'

export default {
  name: 'RoomExamine',
  components: {
    NaviBar,
    FooterBar
  },
  data () {
    return {
      activeName: 'first',
      ReserveList: [],
      ConflictList: [],
      examine_total: 0,
      pagenumber: 1,
      conflictpage: 1,
      text: '',
      dialog_refuse_visible: false,
      dialog_room_info_visible: false,
      dialog_conflict_visible: false,
      form: '',
      refuseId: '',
      agreeId: '',
      result: '',
      examineForm: {
        refuseText: '' // 输入框中的文字
      },
      loading: false,
      roominfo_site: '',
      roominfo_name: '',
      roominfo_csonly: '',
      roominfo_capacity: '',
      roominfo_note: '',
      roominfo_institute: '',
      roominfo_equip: '',
      roominfo_stu_allowed: '',
      state_: 'state:W',
      examine_show: true,
      examine_result_show: false,
      conflict_total: 0,
      orderBy: false,
      options: [
        {
          value: 1,
          label: '会议室不开放'
        }
      ],
      value: ''
    }
  },
  methods: {
    select_change () {
      if (this.value === 1) {
        this.examineForm.refuseText = '很抱歉，该会议室当天不开放。'
      }
    },
    clean_input () {
      this.examineForm.refuseText = ''
      this.value = null
    },
    refuse_conflict () {
      console.log('执行')
      this.loading = true
      GetConflictList(this.agreeId).then((res) => {
        let List = res['data']
        for (let i = 0; i < List.length; i++) {
          ExamineReservation(false, '您的手速稍慢了一点点，该房间已被他人抢先预约了~', List[i].id).then((r) => {
            if (r['code'] !== 200) {
              this.$message({
                message: '数据发送失败！',
                type: 'error'
              })
            }
          })
        }
        ExamineReservation(this.result, this.examineForm.refuseText, this.agreeId).then((r) => {
          if (r['code'] !== 200) {
            this.$message({
              message: '数据发送失败！',
              type: 'error'
            })
          } else {
            this.$message({
              message: '批准成功,并拒绝了所有冲突申请！！',
              type: 'success'
            })
            this.get(1)
          }
        })
      })
      this.loading = false
    },
    conflictpage_Change (val) {
      this.conflictpage = val
      this.get_conflict(val)
    },
    cellStyle ({ row, column, rowIndex, columnIndex }) {
      // 状态列字体颜色
      if (row.state === '已完成' && columnIndex === 7) {
        return 'color: #0CB618'
      } else if (row.state === '已被拒绝' && columnIndex === 7) {
        return 'color: #EA1B29'
      } else if (row.state === '已撤销' && columnIndex === 7) {
        return 'color: #A9A9A9'
      } else if (row.state === '签到超时' && columnIndex === 7) {
        return 'color: #A9A9A9'
      } else if (row.state === '等待审批' && columnIndex === 7) {
        return 'color: #FFA500'
      } else if (row.state === '已过期' && columnIndex === 7) {
        return 'color: #EA1B29'
      } else if (row.state === '审批通过' && columnIndex === 7) {
        return 'color: #0CB618'
      }
    },
    handleClick (tab) {
      if (tab.name === 'first') {
        this.orderBy = false
        this.state_waiting()
      } else if (tab.name === 'second') {
        this.orderBy = true
        this.state_all()
      }
    },
    state_all () {
      this.state_ = ''
      this.examine_show = false
      this.examine_result_show = true
      this.pagenumber = 1
      this.get(1)
    },
    state_waiting () {
      this.state_ = 'state:W'
      this.examine_show = true
      this.examine_result_show = false
      this.pagenumber = 1
      this.get(1)
    },

    // 展示房间信息
    // 1.会议室名称
    // 2.会议室地点
    // 3.会议室容量
    // 4.会议室使用权限（是否仅限计算机系、教师、学生使用）
    // 5.提供设备 话筒、投影、屏幕
    // 5.会议室备注
    showroominfo (id) {
      GetRoomInfo(id).then((res) => {
        let allroominfo = res['data'].room_list[0]
        console.log(res['data'])
        this.roominfo_name = allroominfo.name
        this.roominfo_site = allroominfo.building.name + ' ' + allroominfo.floor + '层'
        this.roominfo_capacity = allroominfo.capacity + '人'
        if (allroominfo.has_projector === true) {
          this.roominfo_equip += '投影' + ' '
        }
        if (allroominfo.has_mic === true) {
          this.roominfo_equip += '话筒' + ' '
        }
        if (allroominfo.roominfo_equip === null) {
          this.roominfo_equip = '无'
        }
        if (allroominfo.has_screen === true) {
          this.roominfo_equip += '屏幕' + ' '
        }

        if (allroominfo.note === '') {
          this.roominfo_note = '无'
        } else {
          this.roominfo_note = allroominfo.note
        }

        if (allroominfo.cs_only === true && allroominfo.teacher_only === false) {
          this.roominfo_csonly = '仅限计算机系教师/学生'
        } else if (allroominfo.cs_only === false && allroominfo.teacher_only === true) {
          this.roominfo_csonly = '仅限教师(全校)'
        } else if (allroominfo.cs_only === true && allroominfo.teacher_only === true) {
          this.roominfo_csonly = '仅限计算机系教师'
        } else if (allroominfo.cs_only === false && allroominfo.teacher_only === false) {
          this.roominfo_csonly = '全校'
        }

        if (allroominfo.institute === null) {
          this.roominfo_institute = '计算机系'
        } else {
          this.roominfo_institute = allroominfo.institute.name
        }
      })
    },

    // 清除对话框中的数据，以防再次弹出时显示上次的数据
    cleanData () {
      this.roominfo_name = ''
      this.roominfo_site = ''
      this.roominfo_capacity = ''
      this.roominfo_csonly = ''
      this.roominfo_note = ''
      this.roominfo_institute = ''
      this.roominfo_equip = ''
    },

    // 赋值
    setAgreeId (id) {
      this.agreeId = id
    },
    setRefuserId (id) {
      this.refuseId = id
    },
    setResultTrue () {
      this.result = true
    },
    setResultFalse () {
      this.result = false
    },

    get_conflict (val) {
      // this.loading = true
      GetConflictList(this.agreeId).then((res) => {
        let ConflictLen = res['data']['length']
        if (ConflictLen === 0) {
          this.agree_()
        } else {
          this.loading = false
          this.conflict_total = res['data'].length
          this.ConflictList = res['data'].slice((val - 1) * 3, Math.min(3 * val, 3 * val + this.conflict_total - 3 * val))
          this.dialog_conflict_visible = true
          // 信息处理
          let start = true
          let StartNum = 0
          let EndNum = 0
          let StartHour = ''
          let time = ''
          let StartMinute = ''
          let EndHour = ''
          let EndMinute = ''
          for (let i = 0; i < this.ConflictList.length; i++) {
            if (this.ConflictList[i].applicant.is_teacher) {
              this.ConflictList[i].applicant.is_teacher = '教师'
            } else {
              this.ConflictList[i].applicant.is_teacher = '学生'
            }
            if (this.ConflictList[i].applicant.institute === null) {
              this.ConflictList[i].applicant.institute = '无'
            } else {
              this.ConflictList[i].applicant.institute = this.ConflictList[i].applicant.institute.name
            }

            // tanSpan转换
            for (let j = 0; j < 48; j++) {
              if (this.ConflictList[i].time_span[j] === '0' && start === true) {
                StartNum += 1
                EndNum += 1
              } else if (this.ConflictList[i].time_span[j] === '1' && start === true) {
                start = false
                StartHour = (StartNum % 2 === 0) ? (StartNum / 2).toString() : (StartNum / 2 - 0.5).toString()
                StartMinute = (StartNum % 2 === 0) ? '00' : '30'
                EndNum += 1
              } else if (this.ConflictList[i].time_span[j] === '1' && start === false) {
                EndNum += 1
              } else if (this.ConflictList[i].time_span[j] === '0' && start === false) {
                EndHour = (EndNum % 2 === 0) ? (EndNum / 2).toString() : (EndNum / 2 - 0.5).toString()
                EndMinute = (EndNum % 2 === 0) ? '00' : '30'
                break
              }
            }
            time = StartHour + ':' + StartMinute + ' ' + '~' + ' ' + EndHour + ':' + EndMinute
            this.ConflictList[i].time_range = this.ConflictList[i].date + '\n' + time
          }
        }
      })
    },

    // 审批---同意
    agree () {
      this.examineForm.refuseText = null
      this.agreeId = this.agreeId.toString()
      this.get_conflict(this.conflictpage)
    },

    agree_ () {
      ExamineReservation(this.result, this.examineForm.refuseText, this.agreeId).then((r) => {
        if (r['code'] === 200) {
          this.$message({
            message: '批准成功！',
            type: 'success'
          })
          this.get(1)
          this.pagenumber = 1
        } else {
          this.$message({
            message: '数据发送失败！',
            type: 'error'
          })
        }
      })
      this.loading = false
    },

    // 审批---拒绝
    refuse () {
      this.loading = true
      if (this.examineForm.refuseText.trim() === '') {
        this.$message({
          message: '请填写拒绝理由！!',
          type: 'error'
        })
      } else {
        this.dialog_refuse_visible = false
        this.refuseId = this.refuseId.toString()
        ExamineReservation(this.result, this.examineForm.refuseText.trim(), this.refuseId).then((r) => {
          if (r['code'] === 200) {
            this.get(1)
            this.pagenumber = 1
            this.$message({
              message: '已拒绝申请!',
              type: 'success'
            })
          } else {
            this.$message({
              message: '数据发送失败！',
              type: 'error'
            })
          }
        })
      }
      this.loading = false
    },

    // 跳转页面
    handleCurrentChange: function (val) {
      this.loading = true
      this.pagenumber = val
      this.get(val)
    },

    // 判管理员
    Judge: function () {
      GetUserInfo().then((res) => {
        let info = res['data']
        if (info.role === 'U') { // 是普通用户则跳出
          this.$router.push('/')
          this.$message({
            message: '请以管理员身份登录!',
            type: 'error'
          })
        }
      })
    },

    // 同意 / 拒绝之后，重新获取审批列表，立刻刷新数据
    get (val) {
      this.loading = true
      GetExamResList(val, this.state_, this.orderBy).then((res) => {
        this.ReserveList = res['data']['list']
        console.log(this.ReserveList)
        this.examine_total = res['data']['total']
        if (this.state_ === 'state:W') {
          this.$refs.NaviBar.ExamineTotal = this.examine_total
        }
        for (let i = 0; i < this.ReserveList.length; i++) {
          this.ReserveList[i].fullname = this.ReserveList[i].applicant.fullname
          this.ReserveList[i].reserveroom = this.ReserveList[i].room.building.name + ' ' + this.ReserveList[i].room.floor + '层' + '\n' + this.ReserveList[i].room.name
          this.ReserveList[i].uid = this.ReserveList[i].applicant.uid
          this.ReserveList[i].orderId = 10 * (this.pagenumber - 1) + i + 1 + '.'
          this.ReserveList[i].roomid = this.ReserveList[i].room.id
          if (this.ReserveList[i].is_teacher === true) {
            this.ReserveList[i].is_teacher = '教师'
          } else {
            this.ReserveList[i].is_teacher = '学生'
          }

          if (this.ReserveList[i].approval_time !== null) {
            let approvaltime1 = ''
            let approvaltime2 = ''
            // let approvaltime12 = ''
            for (let k = 0; k < 10; k++) {
              approvaltime1 = approvaltime1 + this.ReserveList[i].approval_time[k]
            }
            for (let k = 11; k < 16; k++) {
              approvaltime2 = approvaltime2 + this.ReserveList[i].approval_time[k]
            }
            this.ReserveList[i].approval_time = approvaltime1 + '\n' + approvaltime2
          }

          // 展示院系
          if (this.ReserveList[i].applicant.department.name === null || this.ReserveList[i].applicant.department.name === '') {
            this.ReserveList[i].department = '无'
          } else {
            this.ReserveList[i].department = this.ReserveList[i].applicant.department.name
          }

          // 展示研究所
          if (this.ReserveList[i].applicant.institute === null || this.ReserveList[i].applicant.institute === '') {
            this.ReserveList[i].institute = '无'
          } else {
            this.ReserveList[i].institute = this.ReserveList[i].applicant.institute.name
          }

          // timeSpan 转换为 预约时间范围
          let start = true
          let StartNum = 0
          let EndNum = 0
          let StartHour = ''
          let time = ''
          let SubmitDate = ''
          let SubmitMinSec = ''
          let StartMinute = ''
          let EndHour = ''
          let EndMinute = ''
          for (let j = 0; j < 48; j++) {
            if (this.ReserveList[i].time_span[j] === '0' && start === true) {
              StartNum += 1
              EndNum += 1
            } else if (this.ReserveList[i].time_span[j] === '1' && start === true) {
              start = false
              StartHour = (StartNum % 2 === 0) ? (StartNum / 2).toString() : (StartNum / 2 - 0.5).toString()
              StartMinute = (StartNum % 2 === 0) ? '00' : '30'
              EndNum += 1
            } else if (this.ReserveList[i].time_span[j] === '1' && start === false) {
              EndNum += 1
            } else if (this.ReserveList[i].time_span[j] === '0' && start === false) {
              EndHour = (EndNum % 2 === 0) ? (EndNum / 2).toString() : (EndNum / 2 - 0.5).toString()
              EndMinute = (EndNum % 2 === 0) ? '00' : '30'
              break
            }
          }
          time = StartHour + ':' + StartMinute + ' ' + '~' + ' ' + EndHour + ':' + EndMinute
          this.ReserveList[i].time_range = this.ReserveList[i].date + '\n' + time
          for (let k = 0; k < 10; k++) {
            SubmitDate += this.ReserveList[i].submit_time[k]
          }
          for (let k = 11; k < 16; k++) {
            SubmitMinSec += this.ReserveList[i].submit_time[k]
          }
          this.ReserveList[i].submit_time = SubmitDate + '\n' + SubmitMinSec
        }
        this.loading = false
      })
    }
  },

  // 第一次进入页面---数据处理
  mounted () { // 打开时，通过cookie检测登陆状态
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
      this.$message({
        message: '请以管理员身份登录!',
        type: 'error'
      })
    } else {
      CheckToken().then((r) => {
        if (r['data'] === 'True' && r['code'] === 200) { // 有效登录
          this.$refs.NaviBar.LoginStatus('7')
          this.Judge()
        } else { // 登录无效
          this.$router.push('/')
          this.$message({
            message: '请以管理员身份登录!',
            type: 'error'
          })
        }
      })
    }
    this.get(1)
  }
}

</script>

<style scoped>
.el-header {
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  text-align: center;
  line-height: 60px;
  letter-spacing: 20px;
  font-size: 30px;
}

.main_examine {
  display: flex;
  justify-content: center;
}

.footer_examine {
  height: 20% !important;
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #fff;
  justify-content: center;
  text-align: center;
}
.container {
  /*display: flex;*/
  min-height: 600px;
  /*background-color: ;*/
  justify-content: center;
  text-align: center;
}
.el-pagination {
  margin-top: 20px;
  text-align: center;
}
.dialog_examine {
  display: flex;
  height: 400px;
}
.el-dialog__footer {
  background: #f7f7f7;
  text-align: center;
  font-weight: 600;
  margin-top: 30px;
}
.el-dialog__header {
  background: #f7f7f7;
  text-align: center;
  font-weight: 600;
}
.el-table {
  display: table-cell !important;
  justify-content: center;
  text-align: center;
}
.el-table .cell {
  text-align: center;
  white-space: pre-line; /*保留换行符*/
}
.el-page-header__title {
  font-weight: 600;
  letter-spacing: 10px;
  color: azure;
}
.el-page-header__content {
  font-weight: 600;
  letter-spacing: 10px;
  color: azure;
  text-align: center;
}

.dialog_room_info {
  display: flex;
  width: 1200px;
  font-weight: 600;
  position: fixed;
  height: 700px;
  margin: 0 auto !important;
  justify-content: center;
  overflow: hidden;
}
.dialog_room_info__body {
  overflow: auto;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
}
.dialog_room_info__footer {
  background: #f7f7f7;
  text-align: center;
  font-weight: 600;
  margin-top: 30px;
}
.roominfo_item {
  margin-bottom: 10px;
}
.Examine_pageheader {
  margin-top: 20px;
  font-weight: 600;
  color: azure;
}
.dialog_conflict {
  display: flex;
  width: 1200px;
  height: max-content;
  margin: 0 auto !important;
  justify-content: center;
  overflow: hidden;
  overflow-y: auto;
}
.dialog_conflict__body {
  overflow: auto;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.dialog_conflict__footer {
  background: #f7f7f7;
  text-align: center;
  font-weight: 600;
  margin-top: 30px;
  position: relative;
}
.conflict_expand {
  font-size: 0;
}
.conflict_expand label {
  width: 90px;
  color: #99a9bf;
}
.conflict_expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
