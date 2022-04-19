<!--会议室时间表-->
<template>
  <div class="RoomCalendarBlock" v-loading="Loading">
    <div class="Hint">
      <TextBlock
        class="hint_color_block"
        fontSize="15px"
        backgroundColor="#eeeeee"
        width="45px"
      />
      <TextBlock
        fontSize="15px"
        content="不可用 & 已被预约"
        width="180px"
        color="#909399"
      />
      <TextBlock
        class="hint_color_block"
        fontSize="15px"
        backgroundColor="#94DC5A"
        width="45px"
        v-show="HintType === 1"
      />
      <TextBlock
        fontSize="15px"
        content="自己已预约"
        width="120px"
        color="#909399"
        v-show="HintType === 1"
      />
      <TextBlock
        class="hint_color_block"
        fontSize="15px"
        backgroundColor="#F8C471"
        width="45px"
        v-show="HintType === 1"
      />
      <TextBlock
        fontSize="15px"
        content="自己正在申请"
        width="120px"
        color="#909399"
        v-show="HintType === 1"
      />
    </div>
    <el-menu mode="horizontal" style="width: 880px" default-active="0">
      <el-menu-item
        v-for="item in DateColumn"
        :index="item.id"
        :key="item.id"
        @click="DateChange(item.id)"
      >
        {{ item.content }}
      </el-menu-item></el-menu
    >
    <table style="border-spacing: 0px; width: 900px">
      <tr style="display: inline-block; font-size: 0px">
        <td>
          <div
            style="
              width: 75px;
              height: 40px;
              font-size: 16px;
              background-color: transparent;
            "
          ></div>
        </td>
        <td v-for="item in TimeColumn" :key="item.id" style="color: #909399">
          <div :style="item.style">{{ item.hour }}<br />{{ item.minute }}</div>
        </td>
      </tr>
      <RoomCalendarLine
        v-for="line in List"
        :key="line.id"
        :name="line.name"
        :string="line.string"
        @click="RoomInfo(line.id)"
      />
      <div style="margin: 10px; text-align: center; color: #909399">
        <span v-if="Loading === false && List.length === 0"
          >没有符合条件的会议室！</span
        >
      </div>
    </table>
  </div>
</template>

<script>

import RoomCalendarLine from '@/components/RoomCalendarLine.vue'
import TextBlock from '@/components/TextBlock.vue'
export default {
  name: 'RoomCalendarBlock',
  components: {
    RoomCalendarLine,
    TextBlock
  },
  props: {
    list: {// 房间列表
      type: Array,
      default: () => []
    },
    today: {// 今天
      type: String,
      default: () => ''
    },
    dayRange: {// 显示多少天
      type: Number,
      default: () => 7
    },
    active: {// 是否激活跳转按钮
      type: Boolean,
      default: () => true
    },
    hintType: {// 提示的种类
      type: Number,
      default: () => 1
    }
  },
  data () {
    return {
      List: this.list,
      TimeColumn: [],
      DateColumn: [],
      Today: this.today,
      DayRange: this.dayRange,
      DateId: 0,
      Active: this.active,
      HintType: this.hintType,
      Loading: false
    }
  },
  watch: {
    list: {
      handler (val) { // 列表信息同步
        this.List = val
        this.DateSync(this.Today.slice(0, 4), this.Today.slice(5, 7), this.Today.slice(8, 10))
        this.DateChange(this.DateId)
      }
    },
    today: {// 与后端日期同步
      handler (val) {
        this.Today = val
        this.DateSync(this.Today.slice(0, 4), this.Today.slice(5, 7), this.Today.slice(8, 10))
      }
    },
    dayRange: {// 与后端日期范围同步
      handler (val) {
        this.DayRange = val
        this.DateSync(this.Today.slice(0, 4), this.Today.slice(5, 7), this.Today.slice(8, 10))
      }
    },
    active: {// 激活状态同步
      handler (val) {
        this.Active = val
      }
    },
    hintType: {
      handler (val) {
        this.HintType = val
      }
    }
  },
  methods: {
    DateSync: function (y, m, d) { // 计算并同步日期，设置按钮框
      this.DateColumn = []
      for (let i = 0; i < this.DayRange; i++) { // 共DayRange天
        let year = parseInt(y)
        let month = parseInt(m)
        let day = parseInt(d)
        day += i
        if (month === 2 && year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)) { // 闰年二月
          if (day > 28) {
            day -= 28
            month++
          }
        } else if (month === 2) { // 非闰年二月
          if (day > 29) {
            day -= 29
            month++
          }
        } else if (month === 4 || month === 6 || month === 9 || month === 11) { // 小月
          if (day > 30) {
            day -= 30
            month++
          }
        } else { // 大月
          if (day > 31) {
            day -= 31
            month++
          }
        }
        if (month > 12) { // 进年
          month -= 12
        }
        // 设置按钮
        if (this.DateId === i) { // 当前激活的按钮
          this.DateColumn.push({
            id: i,
            content: month.toString() + '月' + day.toString() + '日',
            style: {
              width: '128px',
              fontSize: '18px',
              margin: '0px',
              backgroundColor: '#46B8DA',
              borderRadius: '10px 10px 0px 0px',
              border: '1px solid #aaaaaa'
            }
          })
        } else { // 当前未激活的按钮
          this.DateColumn.push({
            id: i,
            content: month.toString() + '月' + day.toString() + '日',
            style: {
              width: '128px',
              fontSize: '18px',
              margin: '0px',
              backgroundColor: '#eeeeee',
              borderRadius: '10px 10px 0px 0px',
              border: '1px solid #aaaaaa'
            }
          })
        }
      }
    },
    RoomInfo: function (id) { // 跳转到对应的会议室详情页
      if (this.Active) { this.$router.push({ name: 'RoomInfo', params: { RoomId: id } }) }
    },
    DateChange: function (id) { // 选择日期按钮触发的日期变更
      this.DateId = id
      for (let i = 0; i < this.List.length; i++) { // 列表显示变更
        this.List[i].string = this.List[i].time_span[id]
        this.$forceUpdate()
      }
      for (let i = 0; i < this.DayRange; i++) { // 颜色变更
        if (i === id) {
          this.DateColumn[i].style.backgroundColor = '#46B8DA'
        } else { this.DateColumn[i].style.backgroundColor = '#fafafa' }
      }
    },
    SetLoading: function (val) { // 设置加载状态
      this.Loading = val
    }
  },
  created () {
    for (let i = 0; i < 31; i++) { // 初始化时间栏
      let h, mi
      if (i % 2 === 0) {
        h = (8 + Math.floor(i / 2)).toString() + ':'
        mi = i % 2 === 1 ? '30' : '00'
      } else {
        h = mi = ''
      }
      this.TimeColumn.push({
        id: i,
        hour: h,
        minute: mi,
        style: {
          fontSize: '2px',
          width: '25px',
          height: '40px',
          backgroundColor: 'transparent',
          display: 'inline-block',
          margin: '2px -1px -3px -1px'
        }
      })
    }
    let date = new Date()// 创建时使用vue日期
    // 设置时间
    let y = date.getFullYear().toString()
    let m, d
    if (date.getMonth() + 1 < 10) {
      m = '0' + (date.getMonth() + 1).toString()
    } else {
      m = (date.getMonth() + 1).toString()
    }
    if (date.getDate() < 10) {
      d = '0' + date.getDate().toString()
    } else {
      d = date.getDate()
    }
    this.Today = y + '-' + m + '-' + d
    this.DateSync(this.Today.slice(0, 4), this.Today.slice(5, 7), this.Today.slice(8, 10))// 初始化
  }
}
</script>

<style>
.RoomCalendarBlock {
  background-color: #ffffff;
  width: 900px;
  padding: 30px 30px 30px 10px;
  display: inline-block;
}
.Hint {
  display: flex;
  margin: 15px;
}
.hint_color_block {
  border-radius: 20px;
}
</style>
