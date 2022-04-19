<!--会议室预约主页-->
<template>
  <el-container style="border: 1px solid #eee">
    <NaviBar ref="NaviBar" />
    <el-dialog
      :visible.sync="TipsDialogVisible"
      :close-on-click-modal="false"
      title="预约须知"
      width="50%"
    >
      <div v-for="text in Tips" :key="text" class="text">
        {{ text }}
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="HelpVisible"
      :close-on-click-modal="false"
      title="使用帮助"
      width="50%"
    >
      <div v-for="text in Help" :key="text" class="text">
        {{ text }}
      </div>
    </el-dialog>
    <el-container>
      <el-aside style="border: 0px">
        <el-menu @select="HandleAsideSelect">
          <el-menu-item index="0"
            ><i class="el-icon-question"></i>使用帮助</el-menu-item
          >
          <el-menu-item index="1"
            ><i class="el-icon-warning"></i>预约须知</el-menu-item
          >
          <el-menu-item index="2"
            ><i class="el-icon-search"></i>会议室查询</el-menu-item
          >
          <el-submenu index="3" @select="Filt">
            <template slot="title"
              ><i class="el-icon-menu"></i>会议室筛选</template
            >
            <el-menu-item index="0-1"
              >全部&nbsp; &nbsp;&nbsp;<i
                class="el-icon-check"
                v-if="
                  SizeType === '' &&
                  BuildingType === '' &&
                  FloorType === '' &&
                  InstituteType === ''
                "
            /></el-menu-item>
            <el-menu-item-group title="按会议室等级筛选">
              <el-menu-item index="1-1"
                >只看小型会议室&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="SizeType === 's'"
                ></i
              ></el-menu-item>
              <el-menu-item index="1-2"
                >只看中型会议室&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="SizeType === 'm'"
                ></i
              ></el-menu-item>
              <el-menu-item index="1-3"
                >只看大型会议室&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="SizeType === 'l'"
                ></i
              ></el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="按会议室所在楼筛选">
              <el-menu-item index="2-1"
                >只看新系馆&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="BuildingType === 'newbuilding'"
              /></el-menu-item>
              <el-menu-item index="2-2"
                >只看东主楼&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="BuildingType === 'eastprime'"
              /></el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="按会议室楼层筛选">
              <el-menu-item index="3-1"
                >只看1层至2层&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="FloorType === '1'"
              /></el-menu-item>
              <el-menu-item index="3-2"
                >只看3层至4层&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="FloorType === '2'"
              /></el-menu-item>
              <el-menu-item index="3-3"
                >只看5层或以上&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="FloorType === '3'"
              /></el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="按所属研究所筛选">
              <el-menu-item index="5-1"
                >系属&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '1'"
              /></el-menu-item>
              <el-menu-item index="5-2"
                >智能技术与系统国家重点实验室&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '2'"
              /></el-menu-item>
              <el-menu-item index="5-3"
                >人机交互与媒体集成研究所&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '3'"
              /></el-menu-item>
              <el-menu-item index="5-4"
                >计算机网络技术研究所&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '4'"
              /></el-menu-item>
              <el-menu-item index="5-5"
                >高性能计算研究所&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '5'"
              /></el-menu-item>
              <el-menu-item index="5-6"
                >计算机软件研究所&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '6'"
              /></el-menu-item>
              <el-menu-item index="5-7"
                >基础与实验教学部&nbsp; &nbsp;&nbsp;<i
                  class="el-icon-check"
                  v-if="InstituteType === '7'"
              /></el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <div style="text-align: center">
          <RoomCalendarBlock
            :list="List"
            :dayRange="DayRange"
            :today="Today"
            ref="calendar"
          />
        </div>
        <el-dialog
          title="查询会议室"
          :visible.sync="SearchDialogVisible"
          :close-on-click-modal="false"
        >
          <el-Form :model="Search">
            <el-Form-item label="会议室名称" :label-width="LabelWidth">
              <el-input v-model="Search.name" autocomplete="off"></el-input>
            </el-Form-item>
          </el-Form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="SearchDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="OnSearchRoomSubmit"
              >确 定</el-button
            >
          </div>
        </el-dialog>
      </el-main>
    </el-container>
    <el-footer>
      <FooterBar />
    </el-footer>
  </el-container>
</template>

<script>
import RoomCalendarBlock from '@/components/RoomCalendarBlock.vue'
import NaviBar from '@/components/NaviBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import { readCookie } from '@/utils/cookies.js'
import { CheckToken, GetRoomList } from '@/utils/communication.js'
import { reservationTips, reservationHelp } from '@/data/roomdata.js'

export default {
  name: 'RoomReserve',
  components: {
    RoomCalendarBlock,
    NaviBar,
    FooterBar
  },
  data () {
    return {
      // 预约须知和帮助
      Tips: reservationTips,
      TipsDialogVisible: false,
      Help: reservationHelp,
      HelpVisible: false,
      // 搜索框
      SearchDialogVisible: false,
      LabelWidth: '120px',
      Search: {// 搜索的参数
        name: ''
      },
      // 下三个用于给子组件RoomCalendarBlock传参
      List: [/* {
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
      } */],
      Today: '',
      DayRange: 0,
      FullList: [], // 完整列表
      // 以下为筛选种类
      SizeType: '', // 大小
      BuildingType: '', // 所在楼
      FloorType: '', // 所在楼层
      InstituteType: '' // 所属研究所
    }
  },
  methods: {
    OnSearchRoomSubmit () { // 根据存好的FullList来查找会议室
      for (let i = 0; i < this.FullList.length; i++) { // 遍历保存的FullList
        if (this.FullList[i].name === this.Search.name) { // 成功找到
          this.SearchDialogVisible = false
          this.$router.push({ name: 'RoomInfo', params: { RoomId: this.FullList[i].id.toString() } })
          return
        }
      }
      this.$message({
        type: 'info',
        message: '未找到对应会议室！',
        duration: 3000
      })
    },
    HandleAsideSelect (key) {
      if (key === '0') { // 使用帮助
        this.HelpVisible = true
      } else if (key === '1') { // 预约须知
        this.TipsDialogVisible = true
      } else if (key === '2') { // 会议室查询
        this.SearchDialogVisible = true
      } else { // 筛选
        this.Filt(key)
      }
    },
    Filt (key) { // 筛选
      if (key === '0-1') { // 不筛选
        this.SizeType = ''
        this.BuildingType = ''
        this.FloorType = ''
        this.InstituteType = ''
      } else if (key === '1-1') { // 小型会议室
        this.SizeType = this.SizeType === 's' ? '' : 's'
      } else if (key === '1-2') { // 中型会议室
        this.SizeType = this.SizeType === 'm' ? '' : 'm'
      } else if (key === '1-3') { // 大型会议室
        this.SizeType = this.SizeType === 'l' ? '' : 'l'
      } else if (key === '2-1') { // 新系馆
        this.BuildingType = this.BuildingType === 'newbuilding' ? '' : 'newbuilding'
      } else if (key === '2-2') { // 东主楼
        this.BuildingType = this.BuildingType === 'eastprime' ? '' : 'eastprime'
      } else if (key === '3-1') { // <=2层
        this.FloorType = this.FloorType === '1' ? '' : '1'
      } else if (key === '3-2') { // 3-4
        this.FloorType = this.FloorType === '2' ? '' : '2'
      } else if (key === '3-3') { // >=5层
        this.FloorType = this.FloorType === '3' ? '' : '3'
      } else if (key === '5-1') { // 系属
        this.InstituteType = this.InstituteType === '1' ? '' : '1'
      } else if (key === '5-2') { // 智能技术与系统国家重点实验室
        this.InstituteType = this.InstituteType === '2' ? '' : '2'
      } else if (key === '5-3') { // 人机交互与媒体集成研究所
        this.InstituteType = this.InstituteType === '3' ? '' : '3'
      } else if (key === '5-4') { // 计算机网络技术研究所
        this.InstituteType = this.InstituteType === '4' ? '' : '4'
      } else if (key === '5-5') { // 高性能计算研究所
        this.InstituteType = this.InstituteType === '5' ? '' : '5'
      } else if (key === '5-6') { // 计算机软件研究所
        this.InstituteType = this.InstituteType === '6' ? '' : '6'
      } else if (key === '5-7') { // 基础与实验教学部
        this.InstituteType = this.InstituteType === '7' ? '' : '7'
      }

      // 四次截取列表
      let tmp = []
      let list = this.FullList
      console.log(this.list)
      if (this.SizeType === 's') { // 小型会议室
        for (let c in list) {
          if (list[c].size === 'S') { tmp.push(list[c]) }
        }
      } else if (this.SizeType === 'm') { // 中型会议室
        for (let c in list) {
          if (list[c].size === 'M') { tmp.push(list[c]) }
        }
      } else if (this.SizeType === 'l') { // 大型会议室
        for (let c in list) {
          if (list[c].size === 'L') { tmp.push(list[c]) }
        }
      } else {
        tmp = list
      }
      list = tmp
      tmp = []
      if (this.BuildingType === 'newbuilding') { // 东主楼
        for (let c in list) {
          if (list[c].building === 'NewBuilding') { tmp.push(list[c]) }
        }
      } else if (this.BuildingType === 'eastprime') { // 新系馆
        for (let c in list) {
          if (list[c].building === 'EastPrime') { tmp.push(list[c]) }
        }
      } else {
        tmp = list
      }
      list = tmp
      tmp = []
      if (this.FloorType === '1') { // <=2层
        for (let c in list) {
          if (list[c].floor <= 2) { tmp.push(list[c]) }
        }
      } else if (this.FloorType === '2') { // 3-4
        for (let c in list) {
          if (list[c].floor > 2 && list[c].floor <= 4) { tmp.push(list[c]) }
        }
      } else if (this.FloorType === '3') { // >=5层
        for (let c in list) {
          if (list[c].floor > 4) { tmp.push(list[c]) }
        }
      } else {
        tmp = list
      }
      list = tmp
      tmp = []
      if (this.InstituteType === '1') { // 系属
        for (let c in list) {
          if (list[c].institute === null) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '2') { // 智能技术与系统国家重点实验室
        for (let c in list) {
          if (list[c].institute === 1) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '3') { // 人机交互与媒体集成研究所
        for (let c in list) {
          if (list[c].institute === 2) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '4') { // 计算机网络技术研究所
        for (let c in list) {
          if (list[c].institute === 3) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '5') { // 高性能计算研究所
        for (let c in list) {
          if (list[c].institute === 4) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '6') { // 计算机软件研究所
        for (let c in list) {
          if (list[c].institute === 5) { tmp.push(list[c]) }
        }
      } else if (this.InstituteType === '7') { // 基础与实验教学部
        for (let c in list) {
          if (list[c].institute === 6) { tmp.push(list[c]) }
        }
      } else {
        tmp = list
      }
      this.List = tmp
    }
  },
  mounted () { // 打开时，通过cookie检测登陆状态并保存会议室列表
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
    } else {
      this.$refs.calendar.SetLoading(true)// 加载开始
      CheckToken().then((res) => {
        if (res['code'] === 200 && res['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('3')
          GetRoomList().then((r) => {
            if (r['code'] === 200) { // 有效信息
              let list = r['data']['room_list']
              console.log(list)
              let today = r['data']['today']
              let dayRange = r['data']['day_range']
              let date = new Date()// 当前时间
              let alreadypass = date.getHours() * 2 + Math.floor(date.getMinutes() / 30)
              for (let i = 0; i < list.length; i++) {
                let tmpstring = ''
                for (let j = 0; j < 48; j++) {
                  if (j <= alreadypass) { // 时间已经过去，不接受预约
                    tmpstring += '1'
                  } else {
                    tmpstring += list[i].time_span[0][j]
                  }
                }
                list[i].time_span[0] = tmpstring// 修改今天的timespan
                list[i].string = tmpstring// 增加string属性以用于时间栏显示
                // 信息转化
                list[i].building = list[i].building.id === 1 ? 'NewBuilding' : 'EastPrime'
                if (list[i].institute != null) { list[i].institute = list[i].institute.id }
              }

              this.FullList = list
              this.List = list
              this.Today = today
              this.DayRange = dayRange
              this.$refs.calendar.SetLoading(false)// 加载完成
            }
          })
        } else { // 登录无效
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style scoped>
.header {
  background: linear-gradient(120deg, #7f70f5, #0ea0ff);
  color: #fff;
  height: 100px !important;
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
.box-card-blue {
  width: 98%;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid #e3e6f0;
  border-radius: 0.35rem;
  border-left: 0.25rem solid #4e73df !important;
}

.text {
  font-size: 16px;
  line-height: 24px;
}
</style>
