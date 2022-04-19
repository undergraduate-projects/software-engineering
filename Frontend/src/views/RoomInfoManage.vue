<template>
  <el-container style="border: 1px solid #eee">
    <NaviBar ref="NaviBar" />

    <el-container>
      <el-aside>
        <el-menu
          default-active="2-1"
          :default-openeds="['2', '3']"
          @select="handleAsideSelect"
          active-text-color="#ffd04b"
        >
          <el-submenu index="2">
            <template slot="title">
              <span>会议室审批权限</span>
            </template>
            <el-menu-item index="2-1">会议室列表</el-menu-item>
            <el-menu-item index="2-2">管理员列表</el-menu-item>
            <el-menu-item index="2-3">会议室群组</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-main>
        <div class="room-filter" v-if="showRoomList">
          <!--          筛选表单-->
          <el-form
            :inline="true"
            :model="roomFilterForm"
            class="demo-form-inline"
            center
          >
            <el-row :gutter="0">
              <el-col :span="5">
                <el-form-item>
                  <el-input
                    v-model="roomFilterForm.roomName"
                    placeholder="会议室名称"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="5">
                <el-form-item>
                  <el-select
                    v-model="roomFilterForm.buildingId"
                    placeholder="楼宇"
                    style="
                       {
                        width: 50%;
                      }
                    "
                  >
                    <el-option label="全部" :value="0"></el-option>
                    <el-option label="新系馆" :value="1"></el-option>
                    <el-option label="东主楼" :value="2"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item>
                  <el-select
                    v-model="roomFilterForm.instituteId"
                    placeholder="研究所"
                  >
                    <el-option label="全部" :value="-1"></el-option>
                    <el-option
                      v-for="ins in institutes"
                      :label="ins.name"
                      :value="ins.id"
                      :key="ins.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-form-item>
                  <el-button @click="handleResetFilterRoomForm"
                    >重置
                  </el-button>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-form-item>
                  <el-button type="primary" @click="handleRoomFilterFormSubmit"
                    >筛选
                  </el-button>
                </el-form-item>
              </el-col>
              <el-col :span="2" :offset="2">
                <el-tooltip
                  class="item"
                  effect="light"
                  content="增加会议室"
                  placement="left-start"
                >
                  <el-button
                    @click="handleAddRootRoomSubmit"
                    icon="el-icon-plus"
                  ></el-button>
                </el-tooltip>
              </el-col>
            </el-row>
          </el-form>
        </div>

        <!--        房间列表-->
        <div class="room-list" v-if="showRoomList">
          <el-table
            v-loading="roomLoading"
            :data="filteredRoomList"
            :default-sort="{ prop: 'building', order: 'descending' }"
          >
            <!--            下拉表格-->
            <el-table-column type="expand" min-width="50">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="所在楼层：">
                    <span>{{ props.row.floor }}</span>
                  </el-form-item>
                  <el-form-item label="会议室容量：">
                    <span>{{ props.row.capacity }}</span>
                  </el-form-item>
                  <el-form-item label="电子屏幕：">
                    <span v-if="props.row.has_screen">{{ "有" }}</span>
                    <span v-else>{{ "无" }}</span>
                  </el-form-item>
                  <el-form-item label="投影仪：">
                    <span v-if="props.row.has_projector">{{ "有" }}</span>
                    <span v-else>{{ "无" }}</span>
                  </el-form-item>
                  <el-form-item label="麦克风：">
                    <span v-if="props.row.has_mic">{{ "有" }}</span>
                    <span v-else>{{ "无" }}</span>
                  </el-form-item>
                  <el-form-item label="备注：">
                    <span>{{ props.row.note }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <!--常规表格-->
            <el-table-column label="楼宇" min-width="100" align="center">
              <template slot-scope="scope">
                <i class="el-icon-office-building"></i>
                <span style="margin-left: 10px">{{
                  scope.row.building.name
                }}</span>
              </template>
            </el-table-column>
            <el-table-column label="会议室" min-width="180" align="center">
              <template slot-scope="scope">
                <el-tag size="medium">{{ scope.row.name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="研究所" min-width="220" align="center">
              <template slot-scope="scope">
                <el-tag size="medium">{{ scope.row.institute.name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center" min-width="300">
              <template slot-scope="scope">
                <!--                <el-button-->
                <!--                  size="mini"-->
                <!--                  @click="showRoomReservation(scope.row.id)"-->
                <!--                >使用记录-->
                <!--                </el-button>-->
                <el-button
                  size="mini"
                  type="success"
                  @click="handleModifyRootRoom(scope.$index, scope.row.id)"
                  >修改信息
                </el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDeleteRootRoom(scope.$index, scope.row.id)"
                  >删除会议室
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="admin-filter" v-if="showAdminList">
          <!--          管理员搜索框-->
          <el-form
            :inline="true"
            :model="adminFilterForm"
            class="demo-form-inline"
            center
          >
            <el-row>
              <el-col :span="5">
                <el-form-item>
                  <el-input
                    v-model="adminFilterForm.uid"
                    placeholder="学工号"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="5">
                <el-form-item>
                  <el-input
                    v-model="adminFilterForm.fullname"
                    placeholder="姓名"
                  ></el-input>
                </el-form-item>
              </el-col>

              <el-col :span="4">
                <el-form-item>
                  <el-select
                    v-model="adminFilterForm.institute"
                    placeholder="研究所"
                  >
                    <el-option label="全部" value="全部"></el-option>
                    <el-option
                      v-for="ins in institutes"
                      :label="ins.name"
                      :value="ins.name"
                      :key="ins.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>

              <el-col :span="5">
                <el-form-item>
                  <el-button @click="handleResetFilterAdminForm"
                    >重置</el-button
                  >
                  <el-button type="primary" @click="handleAdminFilterFormSubmit"
                    >筛选</el-button
                  >
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </div>
        <!--        管理员列表-->
        <div class="admin-list" v-if="showAdminList">
          <el-table
            v-loading="adminLoading"
            :data="filteredAdminList"
            :default-sort="{ prop: 'id', order: 'descending' }"
          >
            <!--            下拉表格-->
            <el-table-column type="expand" min-width="60">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="联系电话：">
                    <span>{{ props.row.phone_number }}</span>
                  </el-form-item>
                  <el-form-item label="电子邮箱：">
                    <span>{{ props.row.email }}</span>
                  </el-form-item>
                  <el-form-item label="身份：">
                    <span v-if="props.row.role === 'A'">普通管理员</span>
                    <span v-if="props.row.role === 'R'">超级管理员</span>
                  </el-form-item>
                  <el-form-item label="是否任教：">
                    <span v-if="props.row.is_teacher">是</span>
                    <span v-else>否</span>
                  </el-form-item>
                  <el-form-item label="管辖房间组：" :style="{ width: '100%' }">
                    <el-tag
                      type="success"
                      :style="{ margin: '1px' }"
                      v-for="group in props.row.groups"
                      :key="group.id"
                    >
                      {{ group.name }}
                    </el-tag>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <!--常规表格-->
            <el-table-column label="学工号" min-width="150" align="center">
              <template slot-scope="scope">
                <i class="el-icon-user"></i>
                <span style="margin-left: 10px">{{ scope.row.uid }}</span>
              </template>
            </el-table-column>
            <el-table-column label="姓名" min-width="150" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.fullname }}</span>
              </template>
            </el-table-column>
            <el-table-column label="研究所" min-width="220" align="center">
              <template slot-scope="scope">
                <el-tag size="medium">{{ scope.row.institute.name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="管辖房间组" min-width="200" align="center">
              <template slot-scope="scope">
                <el-tag
                  type="success"
                  :style="{ margin: '1px' }"
                  v-for="group in getSubArray(scope.row.groups)"
                  :key="group.id"
                >
                  {{ group.name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center" min-width="200">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="success"
                  @click="addGroupForAdmin(scope.row.id)"
                  >修改管辖房间组
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!--        房间组管理-->
        <!--        房间组筛选框-->
        <div class="group-filter" v-if="showRoomGroup">
          <el-form
            :inline="true"
            :model="groupFilterForm"
            class="demo-form-inline"
            center
          >
            <el-row :gutter="0">
              <el-col :span="6">
                <el-form-item>
                  <el-input
                    v-model="groupFilterForm.name"
                    placeholder="房间组名称"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item>
                  <el-select
                    v-model="groupFilterForm.roomId"
                    placeholder="包含会议室"
                  >
                    <el-option label="全部" :value="0"></el-option>
                    <el-option
                      v-for="room in roomList"
                      :key="room.id"
                      :label="room.name"
                      :value="room.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item>
                  <el-select
                    v-model="groupFilterForm.adminId"
                    placeholder="包含管理员"
                  >
                    <el-option label="全部" :value="0"></el-option>
                    <el-option
                      v-for="admin in adminList"
                      :key="admin.id"
                      :label="admin.fullname"
                      :value="admin.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-form-item>
                  <el-button @click="resetGroupFilterForm">重置</el-button>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-form-item>
                  <el-button type="primary" @click="confirmGroupFilterForm"
                    >筛选</el-button
                  >
                </el-form-item>
              </el-col>

              <el-col :span="2" :offset="4">
                <el-tooltip
                  class="item"
                  effect="light"
                  content="增加房间组"
                  placement="left-start"
                >
                  <el-button
                    @click="handleAddRoomGroupSubmit"
                    icon="el-icon-plus"
                  ></el-button>
                </el-tooltip>
              </el-col>
            </el-row>
          </el-form>
        </div>

        <!--        增加房间组弹框-->
        <div class="add-group-dialog" v-if="roomGroupDialogVisible">
          <el-dialog
            :title="roomGroupDialogTitle"
            :visible.sync="roomGroupDialogVisible"
            center
            :fullscreen="false"
          >
            <el-form
              :inline="true"
              :model="roomGroupForm"
              :ref="roomGroupForm"
              :rules="roomGroupRule"
              class="demo-form-inline"
            >
              <el-form-item label="房间组名称" required prop="name">
                <el-input
                  v-model="roomGroupForm.name"
                  placeholder="名称"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="handleCancelRoomGroupSubmit">取消</el-button>
                <el-button type="primary" @click="handleConfirmRoomGroupSubmit"
                  >确定
                </el-button>
              </el-form-item>
            </el-form>

            <el-tabs type="border-card">
              <el-tab-pane label="添加会议室">
                <el-table
                  ref="multipleTableRoom"
                  :data="roomList"
                  :height="250"
                  tooltip-effect="dark"
                  :default-sort="{ prop: 'id', order: 'descending' }"
                  @selection-change="handleGroupRoomSelectionChange"
                >
                  <el-table-column
                    type="selection"
                    min-width="60"
                  ></el-table-column>
                  <el-table-column label="楼宇" align="center">
                    <template slot-scope="scope"
                      >{{ scope.row.building.name }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="房间名"
                    align="center"
                    min-width="150"
                  >
                    <template slot-scope="scope"
                      >{{ scope.row.name }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="研究所"
                    align="center"
                    min-width="150"
                  >
                    <template slot-scope="scope"
                      >{{ scope.row.institute.name }}
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <el-tab-pane label="添加管理员">
                <el-table
                  ref="multipleTableAdmin"
                  :data="adminList"
                  height="250"
                  tooltip-effect="dark"
                  :default-sort="{ prop: 'id', order: 'descending' }"
                  @selection-change="handleGroupAdminSelectionChange"
                >
                  <el-table-column
                    type="selection"
                    min-width="30"
                  ></el-table-column>
                  <el-table-column label="学工号" align="center" min-width="80">
                    <template slot-scope="scope">{{ scope.row.uid }}</template>
                  </el-table-column>
                  <el-table-column label="姓名" align="center" min-width="80">
                    <template slot-scope="scope"
                      >{{ scope.row.fullname }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="研究所"
                    align="center"
                    min-width="150"
                  >
                    <template slot-scope="scope"
                      >{{ scope.row.institute.name }}
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </el-dialog>
        </div>
        <!--        房间组列表-->
        <div class="room-group-list" v-if="showRoomGroup">
          <el-table
            v-loading="groupLoading"
            :data="filteredRoomGroupList"
            :default-sort="{ prop: 'name', order: 'descending' }"
          >
            <!--            下拉表格-->
            <el-table-column type="expand" min-width="60">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="会议室">
                    <span
                      v-for="room in props.row.rooms"
                      :key="room.id"
                      :style="{ display: 'inline-block', margin: '1px' }"
                    >
                      <el-tag size="medium" type="success">{{
                        room.name
                      }}</el-tag>
                    </span>
                  </el-form-item>
                  <el-form-item label="管理员">
                    <span
                      v-for="admin in props.row.admins"
                      :key="admin.id"
                      :style="{ display: 'inline-block', margin: '1px' }"
                    >
                      <el-tag size="medium" type="success">{{
                        admin.fullname
                      }}</el-tag>
                    </span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <!--常规表格-->
            <el-table-column label="房间组名称" align="center" min-width="150">
              <template slot-scope="scope">
                <span>{{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column label="包含会议室" align="center" min-width="250">
              <template slot-scope="scope">
                <el-tag
                  size="medium"
                  :style="{ margin: '1px' }"
                  v-for="room in getSubArray(scope.row.rooms)"
                  :key="room.id"
                  >{{ room.name }}</el-tag
                >
              </template>
            </el-table-column>
            <el-table-column label="所属管理员" align="center" min-width="250">
              <template slot-scope="scope">
                <el-tag
                  size="medium"
                  :style="{ margin: '1px' }"
                  v-for="admin in getSubArray(scope.row.admins)"
                  :key="admin.id"
                  >{{ admin.fullname }}</el-tag
                >
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center" min-width="300">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="success"
                  @click="handleModifyRoomGroup(scope.$index, scope.row.id)"
                  >修改房间组
                </el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDeleteRoomGroup(scope.$index, scope.row.id)"
                  >删除房间组
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!--        修改房间的基本信息-->
        <div class="modify-room-dialog">
          <!--        修改房间信息的弹出表单 -->
          <el-dialog
            title="修改会议室基本信息"
            :visible.sync="basicInfoDialogVisible"
          >
            <el-form :model="modifiedRoomForm" class="demo-form-inline">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="楼宇">
                    <el-select
                      v-model="modifiedRoomForm.building.name"
                      :style="{ width: '50%', float: 'right' }"
                      @change="
                        handleBuildingChange(modifiedRoomForm.building.name)
                      "
                    >
                      <el-option label="新系馆" value="新系馆"></el-option>
                      <el-option label="东主楼" value="东主楼"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="楼层">
                    <el-select
                      v-model="modifiedRoomForm.floor"
                      :style="{ width: '50%', float: 'right' }"
                      :placeholder="modifiedRoomForm.floor.toString()"
                    >
                      <el-option
                        v-for="floor in Array(5)
                          .fill(0)
                          .map((el, i) => 1 + i)"
                        :key="floor"
                        :label="floor"
                        :value="floor"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="会议室">
                    <el-input
                      v-model="modifiedRoomForm.name"
                      :style="{ width: '50%', float: 'right' }"
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="研究所">
                    <el-select
                      v-model="modifiedRoomForm.institute.name"
                      :style="{ width: '50%', float: 'right' }"
                      @change="
                        handleInstituteChange(modifiedRoomForm.institute.name)
                      "
                    >
                      <el-option
                        v-for="ins in institutes"
                        :key="ins.id"
                        :label="ins.name"
                        :value="ins.name"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="会议室容量">
                    <el-input-number
                      v-model="modifiedRoomForm.capacity"
                      :style="{ width: '50%', float: 'right' }"
                      :placeholder="modifiedRoomForm.capacity.toString()"
                    ></el-input-number>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="电子屏幕">
                    <el-select
                      v-model="modifiedRoomForm.screen"
                      :style="{ width: '50%', float: 'right' }"
                    >
                      <el-option value="有"></el-option>
                      <el-option value="无"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="投影仪">
                    <el-select
                      v-model="modifiedRoomForm.projector"
                      :style="{ width: '50%', float: 'right' }"
                    >
                      <el-option value="有"></el-option>
                      <el-option value="无"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="麦克风">
                    <el-select
                      v-model="modifiedRoomForm.mic"
                      :style="{ width: '50%', float: 'right' }"
                    >
                      <el-option value="有"></el-option>
                      <el-option value="无"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="备注" prop="note">
                <el-input
                  type="textarea"
                  :style="{ width: '76%', float: 'right' }"
                  v-model="modifiedRoomForm.note"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="handleCancelModifyBasic">取消</el-button>
                <el-button type="primary" @click="handleConfirmModifyBasic"
                  >确定</el-button
                >
              </el-form-item>
            </el-form>
          </el-dialog>
        </div>

        <el-dialog :visible.sync="addRoomDialogVisible" title="增加会议室">
          <div slot="header" class="clearfix">
            <span>新增会议室</span>
          </div>
          <el-form
            class="demo-form-inline"
            :model="modifiedRoomForm"
            :ref="modifiedRoomForm"
            :rules="rootRoomRules"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="楼宇" required prop="building.name">
                  <el-select
                    v-model="modifiedRoomForm.building.name"
                    @change="
                      handleBuildingChange(modifiedRoomForm.building.name)
                    "
                    :style="{ width: '50%', float: 'right' }"
                  >
                    <el-option label="新系馆" value="新系馆"></el-option>
                    <el-option label="东主楼" value="东主楼"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="楼层" required prop="floor">
                  <el-select
                    v-model="modifiedRoomForm.floor"
                    :style="{ width: '50%', float: 'right' }"
                  >
                    <el-option
                      v-for="floor in Array(5)
                        .fill(0)
                        .map((el, i) => 1 + i)"
                      :key="floor"
                      :label="floor"
                      :value="floor"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="会议室名称" required prop="name">
                  <el-input
                    v-model="modifiedRoomForm.name"
                    :style="{ width: '50%', float: 'right' }"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="所属研究所" required prop="institute.name">
                  <el-select
                    :style="{ width: '50%', float: 'right' }"
                    v-model="modifiedRoomForm.institute.name"
                    @change="
                      handleInstituteChange(modifiedRoomForm.institute.name)
                    "
                  >
                    <el-option
                      v-for="ins in institutes"
                      :key="ins.id"
                      :label="ins.name"
                      :value="ins.name"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="会议室容量" required prop="capacity">
                  <el-input-number
                    v-model="modifiedRoomForm.capacity"
                    :placeholder="modifiedRoomForm.capacity.toString()"
                    :style="{ width: '50%', float: 'right' }"
                  ></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="电子屏幕" required prop="screen">
                  <el-select
                    v-model="modifiedRoomForm.screen"
                    :style="{ width: '50%', float: 'right' }"
                  >
                    <el-option value="有"></el-option>
                    <el-option value="无"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="投影仪" required prop="projector">
                  <el-select
                    v-model="modifiedRoomForm.projector"
                    :style="{ width: '50%', float: 'right' }"
                  >
                    <el-option value="有"></el-option>
                    <el-option value="无"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="麦克风" required prop="mic">
                  <el-select
                    v-model="modifiedRoomForm.mic"
                    :style="{ width: '50%', float: 'right' }"
                  >
                    <el-option value="有"></el-option>
                    <el-option value="无"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="备注" prop="note">
              <el-input
                type="textarea"
                v-model="modifiedRoomForm.note"
                :style="{ width: '76%', float: 'right' }"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="resetAddRootRoom">全部清空</el-button>
              <el-button type="primary" @click="handleAddRootRoom"
                >确定添加</el-button
              >
            </el-form-item>
          </el-form>
        </el-dialog>

        <el-dialog
          :visible.sync="addGroupForAdminDialogVisible"
          center
          @close="cancelModifyGroupForAdmin"
          title="修改管理员管辖房间组"
          class="add-group-for-admin"
        >
          <el-table
            ref="multipleTableGroupForAdmin"
            :data="roomGroupList"
            :height="250"
            tooltip-effect="light"
            @selection-change="handleGroupForAdminSelectionChange"
          >
            <el-table-column type="selection" min-width="80"></el-table-column>
            <el-table-column label="房间组编号" align="center" min-width="100">
              <template slot-scope="scope">{{ scope.row.id }} </template>
            </el-table-column>
            <el-table-column label="房间组名称" align="center" min-width="140">
              <template slot-scope="scope">{{ scope.row.name }} </template>
            </el-table-column>
            <el-table-column label="包含房间数" align="center" min-width="120">
              <template slot-scope="scope"
                >{{ scope.row.rooms.length }}
              </template>
            </el-table-column>
            <el-table-column label="管理员人数" align="center" min-width="120">
              <template slot-scope="scope"
                >{{ scope.row.admins.length }}
              </template>
            </el-table-column>
          </el-table>
          <span slot="footer" class="dialog-footer">
            <el-button @click="cancelModifyGroupForAdmin">取 消</el-button>
            <el-button type="primary" @click="confirmModifyGroupForAdmin"
              >确 定</el-button
            >
          </span>
        </el-dialog>
      </el-main>
    </el-container>

    <el-footer>
      <FooterBar />
    </el-footer>
  </el-container>
</template>

<script>
import {
  AddGroup,
  AddRootRoom,
  CheckToken,
  DeleteRootRoom,
  GetGroup,
  GetRootRoomList,
  ModifyGroup,
  ModifyRootRoomInfo,
  GetAdminList
} from '@/utils/communication.js'
import { readCookie } from '@/utils/cookies.js'
import { DeleteGroup } from '../utils/communication'
import FooterBar from '@/components/FooterBar.vue'
import NaviBar from '@/components/NaviBar.vue'

export default {
  name: 'RoomInfoManage',
  components: {
    FooterBar,
    NaviBar
  },
  data () {
    return {
      roomLoading: true,
      adminLoading: true,
      groupLoading: true,
      addGroupForAdminDialogVisible: false,
      groupForAdminForm: {},
      basicInfoDialogVisible: false,
      roomGroupDialogVisible: false,
      addRoomDialogVisible: false,
      showRoomList: true,
      showAdminList: false,
      showRoomGroup: false,
      institutes: [
        {
          name: '系属',
          id: 0
        },
        {
          name: '智能技术与系统国家重点实验室',
          id: 1
        },
        {
          name: '人机交互与媒体集成研究所',
          id: 2
        },
        {
          name: '计算机网络技术研究所',
          id: 3
        },
        {
          name: '高性能计算研究所',
          id: 4
        },
        {
          name: '计算机软件研究所',
          id: 5
        },
        {
          name: '基础与实验教学部',
          id: 6
        }
      ],
      roomIdToDeleteAdmin: '', // 要删除管理员的会议室
      roomIdToAddAdmin: '', // 要添加管理员的会议室
      adminIdToDeleteRoom: '', // 要删除会议室的管理员
      adminIdToAddRoom: '', // 要添加会议室的管理员
      selectedRoom: [], // 在弹出对话框中被选择中的房间列表
      selectedAdmin: [], // 在弹出对话框中被选择中的管理员列表
      adminList: [],
      roomList: [],
      // dialogAdminForm: {
      //   id: '',
      //   fullname: '',
      //   institute: ''
      // },
      roomFilterForm: {
        roomName: '',
        buildingId: '',
        instituteId: ''
      },
      adminFilterForm: {
        uid: '',
        fullname: '',
        institute: ''
      },
      filteredRoomList: [],
      modifiedRoomForm: { // 修改房间信息的表单
        id: '',
        name: '',
        building: {
          name: '',
          id: ''
        },
        floor: '',
        capacity: '',
        institute: { // 会议室所属研究所，
          name: '',
          id: ''
        },
        has_screen: '',
        has_projector: '',
        has_mic: '',
        note: '',
        mic: '',
        screen: '',
        projector: ''
      },
      rootRoomRules: {
        name: [
          { required: true, message: '请输入会议室名称', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        'building.name': [
          { required: true, message: '请选择会议室所在楼宇', trigger: 'blur' }
        ],
        floor: [
          { required: true, message: '请选择会议室所在楼层', trigger: 'blur' }
        ],
        capacity: [
          { required: true, message: '请输入会议室最大容纳人数', trigger: 'blur' },
          { type: 'number', min: 1, message: '最大容纳人数不低于1人', trigger: 'blur' }
        ],
        'institute.name': [
          { required: true, message: '请选择会议室所属研究所', trigger: 'blur' }
        ],
        mic: [
          { required: true, message: '请选择会议室是否拥有麦克风设备', trigger: 'blur' }
        ],
        screen: [
          { required: true, message: '请选择会议室是否拥有电子屏幕设备', trigger: 'blur' }
        ],
        projector: [
          { required: true, message: '请选择会议室是否拥有投影仪设备', trigger: 'blur' }
        ]
      },
      roomGroupList: [],
      filteredRoomGroupList: [],
      roomGroupForm: {
        id: '',
        name: '',
        selectedRooms: [],
        selectedAdmins: [],
        rooms: [], // 记录返回给后端的id
        admins: []// 记录返回给后端的id
      },
      roomGroupRule: {
        name: [
          { required: true, message: '请输入会议室名称', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ]
      },
      addRoomGroupDialogVisible: false,
      showModifyRoomGroup: false,
      filteredAdminList: [],
      groupFilterForm: {
        name: '',
        room: '',
        admin: ''
      }
    }
  },
  methods:
  {
    goToHome () {
      this.$router.push('/')
    },
    handleAsideSelect (key, keyPath) {
      this.resetAllFilterForm()
      if (key === '2-1') {
        this.showRoomList = true
        this.showAdminList = false
        this.showRoomGroup = false
        this.getRootRoomList()
      } else if (key === '2-2') {
        this.showRoomList = false
        this.showAdminList = true
        this.showRoomGroup = false
        this.getGroupList()
        this.getAdminList()
      } else if (key === '2-3') {
        this.showRoomList = false
        this.showAdminList = false
        this.showRoomGroup = true
        this.getGroupList()
      }
    },
    handleResetFilterRoomForm () {
      this.resetAllFilterForm()
      this.filteredRoomList = this.roomList
    },
    handleRoomFilterFormSubmit () {
      console.log(this.roomFilterForm)
      this.filteredRoomList = this.roomList
      if (this.roomFilterForm.buildingId) {
        let tmpList = []
        this.filteredRoomList.forEach((elem) => {
          if (elem.building.id === this.roomFilterForm.buildingId) {
            tmpList.push(elem)
          }
        })
        this.filteredRoomList = tmpList
      }
      if (this.roomFilterForm.instituteId !== '' && this.roomFilterForm.instituteId !== -1) {
        let tmpList = []
        this.filteredRoomList.forEach((elem) => {
          if (elem.institute.id === this.roomFilterForm.instituteId) {
            tmpList.push(elem)
          }
        })
        this.filteredRoomList = tmpList
      }
      if (this.roomFilterForm.roomName) {
        let tmpList = []
        this.filteredRoomList.forEach((elem) => {
          if (elem.name.indexOf(this.roomFilterForm.roomName) !== -1) {
            tmpList.push(elem)
          }
        })
        this.filteredRoomList = tmpList
      }
    },
    addGroupForAdmin (adminId) {
      this.groupForAdminForm = {
        adminId: adminId,
        selectedGroups: []
      }
      for (let admin of this.adminList) {
        if (admin.id === adminId) {
          this.groupForAdminForm.selectedGroups = admin.groups
          console.log(admin.fullname)
          console.log(admin.groups)
          console.log(this.groupForAdminForm.selectedGroups)

          this.addGroupForAdminDialogVisible = true
          if (this.groupForAdminForm.selectedGroups.length !== 0) {
            // 不加下方的输出会执行出错
            console.log(this.groupForAdminForm.selectedGroups)
            this.$nextTick(() => {
              for (let group of this.groupForAdminForm.selectedGroups) {
                console.log('select: ', group.name)
                this.$refs.multipleTableGroupForAdmin.toggleRowSelection(group, true)
              }
            })
          }
          break
        }
      }
      // console.log(this.groupForAdminForm.selectedGroups)
    },
    cancelModifyGroupForAdmin () {
      this.addGroupForAdminDialogVisible = false
      this.groupForAdminForm = {}
      this.$refs.multipleTableGroupForAdmin.clearSelection()
    },
    confirmModifyGroupForAdmin () {
      let dic = {
        admin_id: this.groupForAdminForm.adminId,
        groups: []
      }
      this.groupForAdminForm.selectedGroups.forEach((elem) => {
        dic.groups.push(elem.id)
      })
      ModifyGroup(dic).then((res) => {
        if (res['code'] === 200) {
          this.$message({
            type: 'success',
            message: '修改成功!'
          })
          this.getGroupList()
          this.getAdminList()
          // 上边的操作表格不会立即响应
          for (let admin of this.adminList) {
            if (admin.id === this.groupForAdminForm.adminId) {
              admin.groups = this.groupForAdminForm.selectedGroups
              break
            }
          }
          this.addGroupForAdminDialogVisible = false
          this.$refs.multipleTableGroupForAdmin.clearSelection()
        } else {
          this.$message({
            type: 'info',
            message: '修改失败!'
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '修改失败!'
        })
      })
    },
    handleGroupForAdminSelectionChange (selectedGroups) {
      this.groupForAdminForm.selectedGroups = selectedGroups
    },
    handleResetFilterAdminForm () {
      this.adminFilterForm = {
        uid: '',
        fullname: '',
        institute: ''
      }
      this.filteredAdminList = this.adminList
    },
    handleAdminFilterFormSubmit () {
      console.log(this.adminFilterForm)
      this.filteredAdminList = this.adminList
      let tmpList = []
      if (this.adminFilterForm.uid) {
        this.filteredAdminList.forEach((elem) => {
          if (elem.uid.toString().indexOf(this.adminFilterForm.uid.toString()) !== -1) {
            tmpList.push(elem)
          }
        })
        this.filteredAdminList = tmpList
      }

      if (this.adminFilterForm.fullname) {
        tmpList = []
        this.filteredAdminList.forEach((elem) => {
          if (elem.fullname.indexOf(this.adminFilterForm.fullname) !== -1) {
            tmpList.push(elem)
          }
        })
        this.filteredAdminList = tmpList
      }

      if (this.adminFilterForm.institute && this.adminFilterForm.institute !== '全部') {
        tmpList = []
        this.filteredAdminList.forEach((elem) => {
          if (elem.institute.name === this.adminFilterForm.institute) {
            tmpList.push(elem)
          }
        })
        this.filteredAdminList = tmpList
      }
    },
    resetAllFilterForm () {
      this.roomFilterForm = {
        roomName: '',
        buildingId: '',
        instituteId: ''
      }
      this.adminFilterForm = {
        uid: '',
        fullname: '',
        institute: ''
      }
      this.groupFilterForm = {
        name: '',
        roomId: '',
        adminId: ''
      }
    },
    getRootRoomList () {
      this.roomLoading = true
      GetRootRoomList().then((r) => {
        console.log(r['data'])
        r['data'].forEach((elem) => {
          if (!elem.institute) {
            elem.institute = {
              id: 0,
              name: '系属'
            }
          }
          if (!elem.building) {
            elem.building = {
              id: '',
              name: ''
            }
          }
        })
        this.roomList = r['data']
        this.filteredRoomList = r['data']
      })
      this.roomLoading = false
    },
    getAdminList () {
      this.adminLoading = true
      if (this.roomGroupList.length === 0) {
        this.getGroupList()
      }
      GetAdminList().then((res) => {
        res['data'].forEach((elem) => {
          elem['groups'] = this.getRoomGroupForAdmin(elem['id']) // 管理员管辖的房间组
          if (!elem.institute) {
            elem.institute = {
              id: 0,
              name: '系属'
            }
          }
        })
        this.adminList = res['data']
        console.log(this.adminList)
        this.filteredAdminList = res['data']
      })
      this.adminLoading = false
    },
    handleBuildingChange (name) {
      if (name === '新系馆') {
        this.modifiedRoomForm.building.id = 1
      } else if (name === '东主楼') {
        this.modifiedRoomForm.building.id = 2
      }
    },
    handleInstituteChange (name) {
      for (let ins of this.institutes) {
        if (name === ins.name) {
          this.modifiedRoomForm.institute.id = ins.id
          break
        }
      }
    },
    handleModifyRootRoom (index, id) {
      // console.log(index, id)
      // 如要分页，此处的index要对应修改
      this.filteredRoomList[index]['screen'] = this.filteredRoomList[index].has_screen ? '有' : '无'
      this.filteredRoomList[index]['projector'] = this.filteredRoomList[index].has_projector ? '有' : '无'
      this.filteredRoomList[index]['mic'] = this.filteredRoomList[index].has_mic ? '有' : '无'
      let obj = JSON.stringify(this.filteredRoomList[index])
      this.modifiedRoomForm = JSON.parse(obj) // deep copy
      this.basicInfoDialogVisible = true
    },
    handleCancelModifyBasic () {
      this.basicInfoDialogVisible = false
      this.resetAddRootRoom()
    },
    handleConfirmModifyBasic () {
      this.modifiedRoomForm['size'] = 'L'
      this.modifiedRoomForm['teacher_only'] = false
      this.modifiedRoomForm['cs_only'] = true
      this.modifiedRoomForm['institute_id'] = this.modifiedRoomForm.institute.id
      this.modifiedRoomForm['building_id'] = this.modifiedRoomForm.building.id

      this.modifiedRoomForm['has_screen'] = this.modifiedRoomForm.screen === '有'
      this.modifiedRoomForm['has_projector'] = this.modifiedRoomForm.projector === '有'
      this.modifiedRoomForm['has_mic'] = this.modifiedRoomForm.has_mic === '有'

      if (this.modifiedRoomForm.institute.id === 0) { // 系属
        this.modifiedRoomForm.institute_id = null
      }
      this.basicInfoDialogVisible = false
      ModifyRootRoomInfo(this.modifiedRoomForm).then((res) => {
        if (res['code'] === 200) {
          this.$message({
            type: 'success',
            message: '修改成功!'
          })
          this.getRootRoomList()
        } else {
          this.$message({
            type: 'info',
            message: '修改失败!'
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '修改失败!'
        })
      })
    },
    handleAddRootRoomSubmit () {
      this.addRoomDialogVisible = true
      this.resetAddRootRoom()
    },
    resetAddRootRoom () {
      this.modifiedRoomForm = { // 修改房间信息的表单
        id: '',
        name: '',
        building: {
          name: '',
          id: ''
        },
        floor: '',
        capacity: '',
        institute: { // 会议室所属研究所，
          name: '',
          id: ''
        },
        has_screen: '',
        has_projector: '',
        has_mic: '',
        note: '',
        mic: '',
        screen: '',
        projector: ''
      }
      this.$refs[this.modifiedRoomForm].resetFields()
    },
    handleAddRootRoom () {
      // console.log(this.modifiedRoomForm)
      this.$refs[this.modifiedRoomForm].validate((valid) => {
        if (valid) {
          this.modifiedRoomForm['size'] = 'L'
          this.modifiedRoomForm['teacher_only'] = false
          this.modifiedRoomForm['cs_only'] = true
          this.modifiedRoomForm['institute_id'] = this.modifiedRoomForm.institute.id
          this.modifiedRoomForm['building_id'] = this.modifiedRoomForm.building.id

          this.modifiedRoomForm['has_screen'] = this.modifiedRoomForm.screen === '有'
          this.modifiedRoomForm['has_projector'] = this.modifiedRoomForm.projector === '有'
          this.modifiedRoomForm['has_mic'] = this.modifiedRoomForm.mic === '有'
          this.basicInfoDialogVisible = false
          if (this.modifiedRoomForm.institute.id === 0) { // 系属
            this.modifiedRoomForm.institute_id = null
          }
          AddRootRoom(this.modifiedRoomForm).then((res) => {
            if (res['code'] === 200) {
              this.$message({
                type: 'success',
                message: '增加会议室成功!'
              })
              this.resetAddRootRoom()
              this.getRootRoomList()
              this.addRoomDialogVisible = false
            } else {
              this.$message({
                type: 'info',
                message: '增加会议室失败!'
              })
            }
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '增加会议室失败!'
            })
          })
        } else { // 表单验证失败
          // console.log('error submit!!')
          return false
        }
      })
    },
    handleDeleteRootRoom (index, id) {
      // console.log(index, id)
      this.$confirm('您确定要永久删除此会议室吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        let dic = {
          id: id
        }
        DeleteRootRoom(dic).then((res) => {
          if (res['code'] === 200) {
            this.$message({
              type: 'success',
              message: '删除会议室成功!'
            })
            this.getRootRoomList()
          } else {
            this.$message({
              type: 'info',
              message: '删除会议室失败!'
            })
          }
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '删除会议室失败!'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除会议室!'
        })
      })
    },
    handleGroupRoomSelectionChange (selectedRows) {
      this.roomGroupForm.selectedRooms = selectedRows
      // console.log(this.$refs.multipleTableRoom.selection)
      // console.log(selectedRows)
    },
    handleGroupAdminSelectionChange (selectedRows) {
      this.roomGroupForm.selectedAdmins = selectedRows
      // console.log(this.$refs.multipleTableAdmin.selection)
      // console.log(selectedRows)
    },
    handleAddRoomGroupSubmit () {
      this.roomGroupDialogVisible = true
      this.showModifyRoomGroup = false
      this.resetRoomGroupForm()
      this.addRoomGroupDialogVisible = true
    },
    resetRoomGroupForm () {
      this.roomGroupForm = {
        id: '',
        group_id: '',
        name: '',
        selectedRooms: [],
        selectedAdmins: [],
        rooms: [], // 记录返回给后端的id
        admins: []// 记录返回给后端的id
      }
    },
    getGroupList () {
      this.groupLoading = true
      GetGroup().then((res) => {
        console.log(res['data'])
        this.roomGroupList = res['data']
        this.filteredRoomGroupList = res['data']
      }).catch(() => {
        this.$message({
          type: 'danger',
          message: '加载房间组列表失败!'
        })
      })
      this.groupLoading = false
    },
    handleCancelRoomGroupSubmit () {
      this.roomGroupDialogVisible = false
      this.resetRoomGroupForm()
      this.addRoomGroupDialogVisible = false
      this.showModifyRoomGroup = false
    },
    handleConfirmRoomGroupSubmit () {
      this.$refs[this.roomGroupForm].validate((valid) => {
        if (valid) {
          this.roomGroupForm.rooms = []
          this.roomGroupForm.admins = []
          if (this.roomGroupForm.selectedRooms) {
            this.roomGroupForm.selectedRooms.forEach((elem) => {
              this.roomGroupForm.rooms.push(elem.id)
            })
          }
          if (this.roomGroupForm.selectedAdmins) {
            this.roomGroupForm.selectedAdmins.forEach((elem) => {
              this.roomGroupForm.admins.push(elem.id)
            })
          }

          if (this.addRoomGroupDialogVisible) {
            AddGroup({ name: this.roomGroupForm.name }).then((res) => {
              if (res['code'] === 200) {
                if (this.roomGroupForm.selectedAdmins.length === 0 && this.roomGroupForm.selectedRooms.length === 0) {
                  this.roomGroupDialogVisible = false
                  this.$message({
                    type: 'success',
                    message: '新增房间组成功!'
                  })
                  this.getGroupList()
                  this.resetRoomGroupForm()
                  return true
                }
                this.roomGroupForm.id = res['data']['id']
                this.roomGroupForm['group_id'] = this.roomGroupForm.id
                ModifyGroup(this.roomGroupForm)
                  .then((response) => {
                    if (response['code'] === 200) {
                      this.$message({
                        type: 'success',
                        message: '新增房间组成功!'
                      })
                      this.resetRoomGroupForm()
                      this.getGroupList()
                      this.roomGroupDialogVisible = false
                    } else {
                      this.$message({
                        type: 'info',
                        message: '新增房间组失败!'
                      })
                    }
                  })
                  .catch(() => {
                    this.$message({
                      type: 'info',
                      message: '新增房间组失败!'
                    })
                  })
              } else if (res['code'] === 410) {
                this.$message({
                  type: 'info',
                  message: '该房间组名称已被占用，新增失败!'
                })
              }
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '新增房间组失败!'
              })
            })
          }

          if (this.showModifyRoomGroup) {
            this.roomGroupForm['group_id'] = this.roomGroupForm.id
            ModifyGroup(this.roomGroupForm).then((response) => {
              if (response['code'] === 200) {
                this.$message({
                  type: 'success',
                  message: '修改房间组成功!'
                })
                this.resetRoomGroupForm()
                this.getGroupList()
                this.roomGroupDialogVisible = false
              } else {
                this.$message({
                  type: 'info',
                  message: '修改房间组失败!'
                })
              }
            })
              .catch(() => {
                this.$message({
                  type: 'info',
                  message: '修改房间组失败!'
                })
              })
          }
        } else {
          return false
        }
      })
    },
    handleModifyRoomGroup (index, groupId) {
      console.log(groupId)
      this.showModifyRoomGroup = true
      this.addRoomGroupDialogVisible = false
      this.roomGroupDialogVisible = true
      this.resetRoomGroupForm()
      for (let group of this.roomGroupList) {
        if (group.id === groupId) {
          this.roomGroupForm = group
          this.roomGroupForm.selectedRooms = [] // 不能删除
          this.roomGroupForm.selectedAdmins = []
          for (let room of this.roomList) {
            for (let selectedRoom of group.rooms) {
              if (room.id === selectedRoom.id) {
                this.roomGroupForm.selectedRooms.push(room)
                this.$nextTick(() => {
                  this.$refs.multipleTableRoom.toggleRowSelection(room)
                })
              }
            }
          }
          for (let admin of this.adminList) {
            for (let selectedAdmin of group.admins) {
              if (admin.id === selectedAdmin.id) {
                this.roomGroupForm.selectedAdmins.push(admin)
                this.$nextTick(() => {
                  this.$refs.multipleTableAdmin.toggleRowSelection(admin)
                })
              }
            }
          }
        }
      }
    },
    handleDeleteRoomGroup (index, groupId) {
      this.$confirm('您确定要永久删除此房间组吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        DeleteGroup({ id: groupId }).then((res) => {
          if (res['code'] === 200) {
            this.$message({
              type: 'success',
              message: '删除房间组成功!'
            })
            this.getGroupList()
          } else {
            this.$message({
              type: 'info',
              message: '删除房间组失败!'
            })
          }
        })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '删除房间组失败!'
            })
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除房间组!'
        })
      })
    },
    getSubArray (array) {
      if (array && array.length > 2) {
        let ret = array.slice(0, 2)
        ret[2] = { name: '...', fullname: '...' }
        return ret
      }
      return array
    },
    getRoomGroupForAdmin (id) {
      let groupList = []
      for (let groupId in this.roomGroupList) { // 检查房间组
        for (let adminId in this.roomGroupList[groupId].admins) { // 检查组内每个房间
          // console.log(this.roomGroupList[groupId].admins[adminId])
          let groupPushed = false
          if (this.roomGroupList[groupId].admins[adminId].id === id) {
            // console.log(this.roomGroupList[groupId].admins[adminId].fullname)
            for (let i in groupList) { // 检查该房间组是否被重复添加
              if (groupList[i].id === groupId) {
                groupPushed = true
                break
              }
            }
            if (!groupPushed) {
              groupList.push(this.roomGroupList[groupId])
            }
            break
          }
        }
      }
      return groupList
    },
    resetGroupFilterForm () {
      this.resetAllFilterForm()
      this.filteredRoomGroupList = this.roomGroupList
    },
    confirmGroupFilterForm () {
      this.filteredRoomGroupList = this.roomGroupList
      let tmpList = []
      if (this.groupFilterForm.name) {
        this.filteredRoomGroupList.forEach((elem) => {
          if (elem.name.indexOf(this.groupFilterForm.name) !== -1) {
            tmpList.push(elem)
          }
        })
        this.filteredRoomGroupList = tmpList
      }

      if (this.groupFilterForm.roomId) {
        tmpList = []
        this.filteredRoomGroupList.forEach((elem) => {
          for (let room of elem.rooms) {
            if (room.id === this.groupFilterForm.roomId) {
              tmpList.push(elem)
            }
          }
        })
        this.filteredRoomGroupList = tmpList
      }

      if (this.groupFilterForm.adminId) {
        tmpList = []
        this.filteredRoomGroupList.forEach((elem) => {
          for (let admin of elem.admins) {
            if (admin.id === this.groupFilterForm.adminId) {
              tmpList.push(elem)
            }
          }
        })
        this.filteredRoomGroupList = tmpList
      }
    }
    // showRoomReservation (roomId) {
    //   this.roomResDialogVisible = true
    //   for (let room of this.roomList) {
    //     if (room.id === roomId) {
    //       this.roomResTitle = room.name + '历史使用记录'
    //     }
    //   }
    // },
  },
  mounted () {
    let apiToken = readCookie('api_token')
    if (apiToken.length === 0) { // token不存在
      this.$router.push('/')
    } else {
      CheckToken().then((r) => {
        if (r['code'] === 200 && r['data'] === 'True') { // 有效登录
          this.$refs.NaviBar.LoginStatus('0')
          this.getRootRoomList()
          GetGroup().then((res) => {
            this.roomGroupList = res['data']
            this.filteredRoomGroupList = res['data']
          })
          this.getAdminList()
        } else {
          this.$router.push('/')
        }
      })
    }
  },
  computed: {
    roomGroupDialogTitle () {
      if (this.addRoomGroupDialogVisible) {
        return '新增房间组'
      } else if (this.showModifyRoomGroup) {
        return '修改房间组'
      }
      return ''
    }
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
  width: 18% !important;
}

.el-main {
  border-left: 1px solid #e6e6e6;
}

.demo-table-expand {
  font-size: 0;
  margin-left: 45px;
  /*text-align: center;*/
}

.demo-table-expand label {
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

.clearfix {
  margin-bottom: 20px;
  font-size: larger;
}

.el-table__header {
  width: 100% !important;
}

.el-table__body {
  width: 100% !important;
}

.el-menu {
  border-right: none;
}

.el-form-item__label {
  width: 100px;
}
</style>
