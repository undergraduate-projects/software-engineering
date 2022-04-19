<!--会议室时间表基本行-->
<template>
  <tr style="display: inline-block; width: 900px; font-size: 0px">
    <td>
      <el-button
        @click="click"
        style="width: 100px; height: 42px; font-size: 15px; text-align: center margin:-1px 0px -1px 0px;color: #909399"
      >
        {{ Name }}
      </el-button>
    </td>
    <td v-for="item in Column" :key="item.id">
      <div :style="item.style"></div>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'RoomCalendarLine',
  props: {
    name: {// 房间名
      type: String,
      default: () => ''
    },
    string: {// 时间串
      type: String,
      default: () => ''
    }
  },
  data () {
    return {
      Name: this.name,
      Column: []
    }
  },
  methods: {
    click: function () {
      this.$emit('click')
    }
  },
  watch: {
    name: {
      handler (val) {
        this.Name = val
      }
    },
    string: {
      handler (val) {
        for (let i = 16; i < 46; i++) {
          if (val[i] === '0') { // 空闲
            this.Column[i - 16].style.backgroundColor = '#ffffff'
          } else if (val[i] === '1') { // 占用
            this.Column[i - 16].style.backgroundColor = '#eeeeee'
          } else if (val[i] === '3') { // 正在预约
            this.Column[i - 16].style.backgroundColor = '#F8C471'
          } else if (val[i] === '2') { // 用户已预约
            this.Column[i - 16].style.backgroundColor = '#94DC5A'
          }
        }
      }
    }

  },
  created () {
    for (let i = 16; i < 46; i++) {
      if (this.string[i] === '0') { // 空闲
        this.Column.push({
          id: i,
          style: {
            width: '25px',
            height: '40px',
            backgroundColor: '#ffffff',
            border: '1px solid #dddddd',
            margin: '0px -4px -2px -0px'
          }
        })
      } else if (this.string[i] === '1') { // 占用
        this.Column.push({
          id: i,
          style: {
            backgroundColor: '#eeeeee',
            width: '25px',
            height: '40px',
            margin: '0px -4px -2px -0px',
            border: '1px solid #dddddd'
          }
        })
      } else if (this.string[i] === '3') { // 正预约
        this.Column.push({
          id: i,
          style: {
            width: '25px',
            height: '40px',
            backgroundColor: '#F8C471',
            margin: '0px -4px -2px -0px',
            border: '1px solid #dddddd'
          }
        })
      } else if (this.string[i] === '2') { // 用户已预约
        this.Column.push({
          id: i,
          style: {
            backgroundColor: '#94DC5A',
            width: '25px',
            height: '40px',
            border: '1px solid #dddddd',
            margin: '0px -4px -2px -0px'
          }
        })
      }
    }
  }
}
</script>
