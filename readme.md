# 新系馆会议室预约管理系统
## 软件设计文档

Antijuan


[TOC]


# 需求及分析

## 应用背景
计算机系新系馆正在建设阶段，新系馆共有 10 多个公共会议室，20 多个各单位所在楼层会议室，以及 10 多个实验室。本系统旨在更好地管理会议室资源，方便师生员工预约，提高利用率。

## 功能需求
### 系统需求
* 数据库推荐用 MySQL。
* 支持 chrome，Firefox 等主要浏览器。
* 数据库和网页服务分别实现。
* 数据库能自动备份。
* 登录采用 OAuth 验证系统。

### 角色需求
#### 管理员
1. 超级管理员
    * 查看、统计所有会议室基本信息和使用情况。
    * 增加、删除和修改会议室。
    * 设置会议室与普通管理员的对应关系。
    * 超级管理员仅有一名。
    * 修改普通管理员属性（个人信息）。


3. 普通管理员
    * 查看、统计所管理的会议室基本信息和使用情况。
    * 对所管理会议室的预约进行审批。

#### 用户
1. 教师
    * 具有较高优先级，可以借用更多的会议室。
3. 学生
    * 具有较低优先级，有一些会议室无法借用。

* 教师可预约时间段大于学生。
* 教师可预约教室范围大于学生。

#### 会议室
* 分为仅教师可预约、教师和学生均可预约两个等级。
* 预约等级由系统管理员设定。

#### 会议室终端
* 支持查看本会议室预约信息。
* 能够点击确认到达，确保预约者准时参会。



### 用例图
<center class="half">    
    <img src="https://z3.ax1x.com/2021/05/21/gbNjTP.png" />
    <span>超级管理员用例图</span>
</center>


<center class="half">    
    <img src="https://z3.ax1x.com/2021/05/21/gHw0MQ.png" />
    <span>普通管理员用例图</span>
</center>


<center class="half">    
    <img src="https://z3.ax1x.com/2021/05/21/gbwOgS.png" />
    <span>普通用户用例图</span>
</center>


<center class="half">    
    <img src="https://z3.ax1x.com/2021/05/21/gbDr7j.png" />
    <span>会议室终端用例图</span>
</center>


### 用例描述

#### 登录

| 说明 | 用户使用酒井账号登录，会议室终端使用账号密码登录 |
| -------- | -------- | 
| 前提条件     | 用户已经注册酒井账号，会议室账号与密码匹配     | 
| 触发条件| 用户在登录页面点击`用户登录`选项或`会议室公共终端`选项 |
| 流程 | [![gb0xxO.png](https://z3.ax1x.com/2021/05/21/gb0xxO.png)](https://imgtu.com/i/gb0xxO)|
| 后置条件 |  用户进入系统首页，如果用户是普通管理员或超级管理员，导航栏会显示额外选项。会议室终登录后，页面不提供退出登录的选项|


#### 查看个人信息
| 说明 | 查看或修改个人手机号、邮箱和所在研究所等信息 |
| -------- | -------- | 
| 前提条件     | 用户登录信息有效| 
| 触发条件| 用户在首页点击`个人信息`选项 |
| 流程 | [![gbyfjf.png](https://z3.ax1x.com/2021/05/22/gbyfjf.png)](https://imgtu.com/i/gbyfjf)|
| 后置条件 |  用户修改的个人信息在数据库中更新|

#### 查看个人预约记录
| 说明 | 查看用户全部预约记录、已使用预约记录、待审批预约记录、待使用预约记录、已取消预约记录、未通过预约记录、已失效预约记录和违约记录。在通过审批的记录中查看会议室的签到码，在申请使用的时间之前可以取消预约 |
| -------- | -------- | 
| 前提条件     | 用户登录信息有效| 
| 触发条件| 用户在首页点击`预约记录`选项 |
| 流程 | [![gbMYHe.png](https://z3.ax1x.com/2021/05/21/gbMYHe.png)](https://imgtu.com/i/gbMYHe)|
| 后置条件 |  用户取消的预约在数据库中更新|


#### 进行预约
| 说明 | 学生可预约一周以内的会议室，教师可预约两周以内的会议室。用户待预约时间段不能与已有预约时间段冲突 |
| -------- | -------- | 
| 前提条件     | 用户登录信息有效且不在封禁期内| 
| 触发条件| 用户在首页点击`预约`选项 |
| 流程 | [![gbMZBF.png](https://z3.ax1x.com/2021/05/21/gbMZBF.png)](https://imgtu.com/i/gbMZBF)|
| 后置条件 |  用户申请的预约在数据库中更新，所预约会议室对应管理员会收到该请求。对于递交后6小时和12小时尚未审批的预约，系统会以邮件方式提醒管理员。审批结果会以邮件方式告知用户|

#### 审批预约
| 说明 | 审批用户的预约请求 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为管理员或超级管理员并管辖预约请求对应的会议室| 
| 触发条件| 用户在首页点击`审批`选项 |
| 流程 | [![gbugsS.png](https://z3.ax1x.com/2021/05/21/gbugsS.png)](https://imgtu.com/i/gbugsS)|
| 后置条件 |  审批结果在数据库中更新，并以邮件方式告知申请人|

#### 查看审批记录
| 说明 | 查看已审批的全部预约请求 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为管理员或超级管理员| 
| 触发条件| 用户在首页点击`审批`选项，进入审批页面后点击`查看审批记录`选项 |
| 流程 | [![gbK3wQ.png](https://z3.ax1x.com/2021/05/21/gbK3wQ.png)](https://imgtu.com/i/gbK3wQ)|
| 后置条件 |  无|

#### 查看管辖房间的使用记录
| 说明 | 查看所管辖会议室的历史使用记录 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为管理员或超级管理员并管辖待查看的会议室| 
| 触发条件| 用户在首页点击`预约`选项，进入会议室列表页面后，选择并点击进入自己管辖的某一会议室，进入会议室详情页面后点击`使用记录`选项 |
| 流程 | [![gbKW6K.png](https://z3.ax1x.com/2021/05/21/gbKW6K.png)](https://imgtu.com/i/gbKW6K)|
| 后置条件 |  无|

#### 添加/删除房间
| 说明 | 添加新会议室或删除已有会议室 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为超级管理员| 
| 触发条件| 超级管理员点击`房间管理`选项，进入会议室列表页面后点击 `+`按钮或选择一个会议室点击`删除会议室`按钮 |
| 流程 | [![gbyzbF.png](https://z3.ax1x.com/2021/05/22/gbyzbF.png)](https://imgtu.com/i/gbyzbF)|
| 后置条件 |  增加或删除的会议室在数据库中更新|

#### 修改房间信息
| 说明 | 修改已有会议室的基本信息 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为超级管理员| 
| 触发条件| 超级管理员点击`房间管理`选项，进入会议室列表页面后点击`修改信息`按钮 |
| 流程 | [![gb3gs0.png](https://z3.ax1x.com/2021/05/21/gb3gs0.png)](https://imgtu.com/i/gb3gs0)|
| 后置条件 |  修改后的会议室信息在数据库中更新|

#### 添加/删除房间组
| 说明 | 添加新房间组或删除已有房间组 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为超级管理员| 
| 触发条件| 超级管理员点击`房间管理`选项，之后点击`房间组列表`选项进入房间组列表页面，然后点击`+`按钮或选择一个房间点击`删除房间组`按钮 |
| 流程 | [![gbtNE6.png](https://z3.ax1x.com/2021/05/21/gbtNE6.png)](https://imgtu.com/i/gbtNE6)|
| 后置条件 |  增加或删除的房间组在数据库中更新|


#### 修改房间组
| 说明 | 修改已有房间组的信息 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为超级管理员| 
| 触发条件| 超级管理员点击`房间管理`选项，之后点击`房间组列表`选项进入房间组列表页面，然后选择一个房间组点击`修改房间组`按钮 |
| 流程 | [![gbNWe1.png](https://z3.ax1x.com/2021/05/21/gbNWe1.png)](https://imgtu.com/i/gbNWe1)|
| 后置条件 |  修改后的房间组信息在数据库中更新|

#### 修改用户信息
| 说明 | 修改数据库内全部用户的信息 |
| -------- | -------- | 
| 前提条件     | 登录信息有效，用户角色为超级管理员| 
| 触发条件| 超级管理员点击`用户管理`选项，然后选择一个用户点击点击`修改权限`按钮 |
| 流程 | [![gbdJzD.png](https://z3.ax1x.com/2021/05/21/gbdJzD.png)](https://imgtu.com/i/gbdJzD)|
| 后置条件 |  修改后的用户信息在数据库中更新|

#### 显示会议室信息/签到/签退
| 说明 | 在会议室终端页面可以查看会议室当日预约时间和其他基本信息，可进行签到和签退 |
| -------- | -------- | 
| 前提条件     | 以会议室账号密码登录| 
| 触发条件| 在终端页面点击`签到`或`签退`选项 |
| 流程 | [![gbspsU.png](https://z3.ax1x.com/2021/05/21/gbspsU.png)](https://imgtu.com/i/gbspsU)|
| 后置条件 |  签到和签退时间在数据库中更新|

## 拓展需求
* 良好支持支持 PC 及手机的浏览器自适应使用，支持 IE 和其他更多浏览器。
* 能够根据关键字和其他信息检索历史实验室使用情况。

## 非功能需求
* 项目代码风格良好，逻辑清晰，注释完整，便于维护和拓展。
* 运行稳定，鲁棒性高。
* 系统安全性高，具体体现在：
    * 网页后退不能够重新进入系统
    * 不能够被没有账号密码的人看到系统内部数据。
    * 不能够采用网站地址更改后面页面名字的形式看到别的页面，例如`http://166.111.68.150/index.hmtl`，在网站目录下有个 `list.html` 的页面，如果通过输入地址`http://166.111.68.150/list.html` 就能够访问 `list.html`,就是不可以的。
* 开发过程符合软件工程开发流程


# 数据库设计

### 总述

数据库选用 `Mariadb`

`DEFAULT CHARACTER SET` 为 `utf8`

`COLLATE` 为 `utf8_general_ci`

数据库设计如下图

![](https://raw.githubusercontent.com/tz039e/images/master/img/db.png)


### 特殊说明

图中的介绍已经很清晰，下面将仔细说明一下值得注意的地方

> 在 `models.py` 中我们还给`User`, `Room`, `Reservation` 等table的类添加了method，例如返回一个用户的信息等，以便视图函数调用

#### `User` 用户

普通用户、管理员、超级管理员均在此表中

- `role` 权限
  
    包含：
    ```python
    NORMAL_USER = 'U'  # 普通用户
    ADMIN = 'A'        # 管理员
    ROOT = 'R'         # 超级管理员
    ```

- `unban_time` 解封时间
    - 晚于当前时间则为封禁状态
    - `NULL` 或早于当前时间则为未封禁

#### `Building` 楼

仅可通过数据库更改，目前有新系馆和东主楼


#### `Room` 会议室房间

- `size` 会议室大小
  
    包含
    ```python
    LARGE_SIZE = 'L'   # 大型
    MEDIUM_SIZE = 'M'  # 中型
    SMALL_SIZE = 'S'   # 小型
    ```
    
- `institute` 所属研究所
    若为系属则存为 `NULL`

- `terminal_token` 终端登录的密码
    - 仅可通过数据库更改

#### `RoomGroup` 房间组

用于设置管理权限，每个房间组可包含多个房间，可对应多个管理员


#### `Reservation` 预约记录

- `time_span` 申请时间段
    - 由于预约的最小分度为半小时，所以将一天划分为48个部分，用48位二进制表示
    - `1` 代表申请， `0` 代表未申请
- `state` <span id="state">状态</span>

    包含以下状态：
    ```python
    WAITING = 'W'          # 等待审批
    APPROVED = 'A'         # 审批通过
    REFUSED = 'R'          # 已被拒绝
    CANCELED = 'C'         # 已撤销
    EXPIRED = 'E'          # 已过期
    USING = 'U'            # 正在使用
    FINISHED = 'F'         # 已完成
    FINISHED_LATE = 'L'    # 已完成（晚退）
    ABSENT = 'B'           # 签到超时
    ```
    
    状态转移示意图如下：
    ![](https://raw.githubusercontent.com/tz039e/images/master/img/20210519212433.png)


### 自动备份

采用Mariadb的主从备份方式，参考 https://blog.51cto.com/u_11010461/2128561

- 首先保证主从库初始数据一致，主库版本不高于从库版本
- 更改主库配置

    ```conf
    #唯一标示的id段，不可重复
    server-id=1 
    #开启二进制日志，可以自定义路径和文件名
    log-bin=mysql-bin
    #开启二进制中继日志并定义命名格式
    relay-log=mysq-relay-bin
    #复制的过滤项，负责过滤掉不需要复制的库和表
    replicate-wild-ignore-table=mysql.%
    replicate-wild-ignore-table=test.%
    replicate-wild-ignore-table=information_schema.%
    ```

- 更改从库配置

    ```conf
    #唯一标示的id段，不可重复
    server-id=2
    #开启二进制日志，可以自定义路径和文件名
    log-bin=mysql-bin
    #开启二进制中继日志并定义命名格式
    relay-log=mysq-relay-bin
    #复制的过滤项，负责过滤掉不需要复制的库和表
    replicate-wild-ignore-table=mysql.%
    replicate-wild-ignore-table=test.%
    replicate-wild-ignore-table=information_schema.%
    ```

- 在主库创建备份账号

    ```sql
    GRANT REPLICATION SLAVE ON *.* TO "username"@"SlaveIP" IDENTIFIED BY "userpassword";
    ```

- 查看主库的二进制日志信息

    ```
    MariaDB [(none)]> show master status;
    +------------------+----------+--------------+------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
    +------------------+----------+--------------+------------------+
    | mysql-bin.000002 | 41836004 |              |                  |
    +------------------+----------+--------------+------------------+
    ```

- 配置从数据库

    ```
    mariadb> change master to \
            -> master_host='masterIP',  # 主库位置
            -> master_user='slave_username',  # 上上步创建的账号名
            -> master_password='slave_password',  # 上上步创建的账号密码
            -> master_log_file='mysql-bin.000002',  # 上一步中主库二进制日志名
            -> master_log_pos=41836004;  # 上一步中二进制文件的位置
    ```

- 从库开启slave

    ```
    start slave;
    ```

- 检查运行状态

    ```
    MariaDB [(none)]> show slave status\G;
    *************************** 1. row ***************************
                    Slave_IO_State: Waiting for master to send event
                       Master_Host: 172.17.0.1
                       Master_User: slave
                       Master_Port: 3306
                     Connect_Retry: 60
                   Master_Log_File: mysql-bin.000002
               Read_Master_Log_Pos: 41836004
                    Relay_Log_File: mysql-relay-bin.000004
                     Relay_Log_Pos: 21709904
             Relay_Master_Log_File: mysql-bin.000002
                  Slave_IO_Running: Yes
                 Slave_SQL_Running: Yes
                   Replicate_Do_DB:
               Replicate_Ignore_DB:
                Replicate_Do_Table:
            Replicate_Ignore_Table:
           Replicate_Wild_Do_Table:
       Replicate_Wild_Ignore_Table: mysql.%,information_schema.%,performance_schema.%,django_test.%
                        Last_Errno: 0
                        Last_Error:
                      Skip_Counter: 0
               Exec_Master_Log_Pos: 41836004
                   Relay_Log_Space: 21710213
                   Until_Condition: None
                    Until_Log_File:
                     Until_Log_Pos: 0
                Master_SSL_Allowed: No
                Master_SSL_CA_File:
                Master_SSL_CA_Path:
                   Master_SSL_Cert:
                 Master_SSL_Cipher:
                    Master_SSL_Key:
             Seconds_Behind_Master: 0
     Master_SSL_Verify_Server_Cert: No
                     Last_IO_Errno: 0
                     Last_IO_Error:
                    Last_SQL_Errno: 0
                    Last_SQL_Error:
       Replicate_Ignore_Server_Ids:
                  Master_Server_Id: 1
                    Master_SSL_Crl:
                Master_SSL_Crlpath:
                        Using_Gtid: No
                       Gtid_IO_Pos:
           Replicate_Do_Domain_Ids:
       Replicate_Ignore_Domain_Ids:
                     Parallel_Mode: optimistic
                         SQL_Delay: 0
               SQL_Remaining_Delay: NULL
           Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
                  Slave_DDL_Groups: 217
    Slave_Non_Transactional_Groups: 0
        Slave_Transactional_Groups: 53423
    1 row in set (0.000 sec)
    ```

# 前后端结构设计及通信接口设计

## 接口设计

### 总述

> 均为前端向后端请求增删改查数据时调用



#### 根URL

API的根URL：`/api/`，以下API的URL均为根URL后的相对路径

#### 请求参数格式

- 所有 ***GET*** 请求的请求参数均为Query String Parameters，即url string的形式；
- **其余类型** 请求的参数content-type为application/json，即JSON格式

#### 返回格式

返回信息为 `JSON` 格式，形如：
```json
{
    "code": `HTTP请求响应码`,
    "data": `后端返回的数据`（各API说明中的返回指的就是这里）
}
```

#### 共通返回

这些返回在所有的接口都有可能返回，它们是所有接口共通的，在此统一说明，下面的接口将不再列出。

| 响应码 | 描述 |
| -------- | -------- |
| 200 | 请求成功 |
| 405 | 请求的方法不允许 |
| 401 | 登录过期或未登录 |
| 400 | 请求的格式或参数错误 |
| 403 | 当前用户无权访问 |

#### `time_span`

该参数在参数返回中出现频率较高，表示时间段，一般为48位的01字符串，也可能有2、3来表示更多含义

#### 鉴权

- 用户、管理员、超管：

    除登录外的API均需要在Cookie中包含 `api_token` 一项用于认证，否则会返回401错误

- 终端：

    除登录外的API均需要在Cookie中包含 `terminal_token` 一项用于认证，否则会返回401错误

### 登录

#### `check_token`

验证用户是否有效登录

***GET***

要求Cookie中应有 `api_token` 一项，后端会根据此项token判断用户登录的有效性

返回：
```json
有效： "True"
无效： "False"
```

---

#### `login`

登录操作

***POST***

请求参数：

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `auth_code`  | 前端通过OAuth获得的auth_code | 是 |
| `path` | 前端OAuth后需要重定向至的uri | 是 |

返回：
```json
{
    "result": "success" or "fail",
    "api_token": 成功登录则返回后端生成的token，用于以后的验证,
    "error": 若失败则返回，表示错误信息
}
```

由于历史原因这个接口的返回值是直接返回而不是和其他接口一样存在`data`里的

---

#### `logout`

登出操作

***GET***

除了Cookie中有 `api_token` 一项正常登出的情况外，未登录时登出也认为登出成功

返回：
```
正常登出： "Logout OK"
未登录： "Login timeout or not logged in"
```

### 研究所

#### `institutes`

***GET***

获取研究所列表

返回示例：
```json
[
    {
        "id": 2,
        "name": "人机交互与媒体集成研究所"
    },
    {
        "id": 6,
        "name": "基础与实验教学部"
    },
    {
        "id": 1,
        "name": "智能技术与系统国家重点实验室"
    },
    {
        "id": 3,
        "name": "计算机网络技术研究所"
    },
    {
        "id": 5,
        "name": "计算机软件研究所"
    },
    {
        "id": 4,
        "name": "高性能计算研究所"
    }
]
```



### 用户

#### `user/info`

用户信息的改、查

***GET***

获取自己的个人信息

返回示例：
```json
{
    "id": 6,  // 数据库中的id
    "uid": "2019010101",  // 学工号
    "username": "aragorn19",  // 酒井id的用户名
    "fullname": "阿拉贡",  // 中文姓名
    "is_teacher": false,  // 学生为false，教师为true
    "email": "username@mail.com",  // 邮箱，没有则为空字符串
    "phone_number": "",  // 手机号，没有则为空字符串
    "role": "R",  // 权限：普通用户(U) 管理员(A) 超级管理员(R)
    "department": {  // 院系
        "id": 1,  // 数据库中的id
        "name": "计算机科学与技术系"  // 院系名
    },
    "institute": {  // 研究所，若为本科生则此项为null
        "id": 5,  // 数据库中的id
        "name": "计算机软件研究所"  // 研究所名
    },
    "unban_time": 1620451396093.799,  // 解封时间，毫秒时间戳
    "recent_breach": 9  // 近30天违约次数
}
```

***PUT***

*请求参数：*

1. 用户更改自己信息：

    | 参数名 | 描述 | 是否必选 |
    | -------- | -------- | -------- |
    | `email`  | 邮箱，需符合格式 | 否 |
    | `phone_number` | 手机号，需符合格式 | 否 |
    | `institute_id` | 研究所id | 否 |

2. 管理员更改其他用户信息，需要Root身份

    | 参数名 | 描述 | 是否必选 |
    | -------- | -------- | -------- |
    | `id`  | 要修改的用户的id | 是 |
    | `role` | 权限 `[U\|A\|R]` | 否 |
    | `is_teacher` | 是否为教师 | 否 |
    | `department_id` | 院系id | 否 |
    | `institute_id` | 研究所id | 否 |
    | `ban_days` | 从当前起封禁的天数，0即为解封 | 否 |


---

#### `user/list`

***GET***

获取用户列表，需Root权限，功能包括：
- 分页
- 排序
- 筛选

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `page_num`  | 想要查看的分页页数，不传则不分页返回全部 | 否 |
| `order_by` | 排序，详情见表格下方参数详情 | 是 |
| `only` | 筛选，详情见表格下方参数详情 | 是 |

*参数详情：*
- `order_by`
    - 若传入空值默认为按学号升序排序
    - 参数值最前面若有 `-` 则为降序排序，否则为升序
    - 可选的值：`uid`, `username`, `fullname`, `is_teacher`, `email`, `phone_number`, `role`, `department`, `institute`
    - `fullname` 为按汉语拼音排序
- `only`
    - 若不筛选则传入空值即可
    - 格式：形如 `fullname:张三,role:U`，表示只看名为张三的普通用户
    - 常规参数：`uid`, `username`, `fullname`, `is_teacher`, `email`, `phone_number`, `role`, `department`, `institute`
    - 特殊参数：
        - `role__in:AR`：筛选权限，此句表示筛选权限为管理员和超级管理员的
        - `institute__in:1|2|3`：筛选研究所，此句表示筛选研究所id为1或2或3的
        - `banned:true`：筛选被封禁用户
        - `uid__contains`：学工号的子串搜索
        - `fullname__contains`：姓名的子串搜索

*返回数据：*

返回一个列表，列表内每个元素为一个人的信息，每个人的信息与 [***GET*** `user/info`](#userinfo) 的返回值完全一致

---

#### `user/reservation`

***GET***

获取当前用户的全部历史预约记录，按提交时间从新到旧排序

*请求参数：*

无

*返回示例：*

```json
{
    "list": [
        {
            "id": 154,
            "date": "2021-05-15",
            "apply_reason": "hi",
            "submit_time": "2021-05-15T00:30:12.212",
            "approval_result": null,
            "refuse_reason": null,
            "approval_time": null,
            "token": null,
            "arrival_time": null,
            "leave_time": null,
            "cancel_time": null,
            "applicant": {
                "id": 6,
                "uid": "2019011288",
                "username": "zhoutz19",
                "fullname": "周天泽",
                "is_teacher": false,
                "email": "tz03e@gmail.com",
                "phone_number": "",
                "role": "R",
                "department": {
                    "id": 1,
                    "name": "计算机科学与技术系"
                },
                "institute": {
                    "id": 5,
                    "name": "计算机软件研究所"
                },
                "unban_time": 1620451396093.799,
                "recent_breach": 9
            },
            "room": {
                "id": 3,
                "name": "报告厅402",
                "size": "L",
                "capacity": 268,
                "floor": 4,
                "teacher_only": true,
                "cs_only": false,
                "has_screen": true,
                "has_projector": true,
                "has_mic": false,
                "note": "",
                "building": {
                    "id": 1,
                    "name": "新系馆"
                },
                "institute": null
            },
            "time_span": "000000000000000000000011100000000000000000000000",
            "approval_person": "暂未审批",
            "state": "已过期"
        },
        {
            ...同上
        }
    ]
}
```


### 房间

#### `room/list`

***GET***

返回当前用户有预约权限的房间的信息列表

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `only`  | `only=room:1` 表示只看id为1的房间 | 否 |
| `reserving` | 若为 `True` 则包括时间信息，详情见下方 | 否 |

*返回示例：*

若 `reserving` 不为 `True`：

返回列表，包含每个房间的信息（和 [***GET*** `room/info`](#roominfo) 一致）

```json
[
     {
        "id": 1,
        "name": "会议室501",
        "size": "L",
        "capacity": 150,
        "floor": 2,
        "teacher_only": false,
        "cs_only": true,
        "has_screen": false,
        "has_projector": true,
        "has_mic": false,
        "note": "",
        "building": {
            "id": 1,
            "name": "新系馆"
        },
        "institute": {
            "id": 2,
            "name": "人机交互与媒体集成研究所"
        }
    },
    {
        "id": 2,
        "name": "报告厅502",
        "size": "L",
        "capacity": 5,
        "floor": 5,
        "teacher_only": false,
        "cs_only": true,
        "has_screen": false,
        "has_projector": true,
        "has_mic": false,
        "note": "",
        "building": {
            "id": 1,
            "name": "新系馆"
        },
        "institute": null
    }
]
```

若 `reserving` 为 `True`：
```json
{
    "today": "2021-05-22",  // 当前日期 string 用于前后端统一日期
    "day_range": 7,  // 当前用户能申请的天数范围
    "waiting_time_span": [  // 当前用户已申请的时间信息
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000000000"
    ],
    "room_list": [
        {
            "id": 1,
            "name": "会议室501",
            "size": "L",
            "capacity": 150,
            "floor": 2,
            "teacher_only": false,
            "cs_only": true,
            "has_screen": false,
            "has_projector": true,
            "has_mic": false,
            "note": "",
            "building": {
                "id": 1,
                "name": "新系馆"
            },
            "institute": {
                "id": 2,
                "name": "人机交互与媒体集成研究所"
            },
            "time_span": [
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000"
            ],
            "admin": true
        },
        {
            "id": 2,
            "name": "报告厅502",
            "size": "L",
            "capacity": 5,
            "floor": 5,
            "teacher_only": false,
            "cs_only": true,
            "has_screen": false,
            "has_projector": true,
            "has_mic": false,
            "note": "",
            "building": {
                "id": 1,
                "name": "新系馆"
            },
            "institute": null,
            "time_span": [
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000",
                "000000000000000000000000000000000000000000000000"
            ],
            "admin": true
        }
    ]
}
```

`reserving` 为 `True` 时每个房间新增的参数：

- `time_span`
    - `1` 代表已被他人预约
    - `2` 代表当前用户以预约
    - `3` 代表当前用户申请中

- `admin`
    - 表示当前用户是否有该房间的管理权限


---

#### `room/info`

房间信息的增删改查

***GET***

获取房间信息，任何用户都有权限

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id`  | 要查看信息的房间id | 是 |

*返回示例：*

```json
{
    "id": 1,
    "name": "会议室501",
    "size": "L",
    "capacity": 150,
    "floor": 2,
    "teacher_only": false,
    "cs_only": true,
    "has_screen": false,
    "has_projector": true,
    "has_mic": false,
    "note": "",
    "building": {
        "id": 1,
        "name": "新系馆"
    },
    "institute": {
        "id": 2,
        "name": "人机交互与媒体集成研究所"
    }
}
```

***PUT***

更改房间信息，需Root权限

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id`  | 要修改信息的房间id | 是 |
| `name`, `size`, `capacity`, `floor`, `teacher_only`, `cs_only`, `has_screen`, `has_projector`, `has_mic`, `note`, `building`, `institute` | 要修改的信息 | 否 |

***DELETE***

删除房间，需Root权限

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id`  | 要删除的房间id | 是 |

***POST***

添加房间，需Root权限

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `name`, `size`, `capacity`, `floor`, `teacher_only`, `cs_only`, `has_screen`, `has_projector`, `has_mic`, `note`, `building`, `institute` | 房间的信息 | 全部必选 |


### 预约

#### `reservation/conflict`

***GET***

获取与一个预约时间冲突的预约信息列表，需要对应房间的管理权限

*请求参数：*
| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `res_id` | 一个预约id（Number） | 是 |

*返回数据：*

返回一个与res_id在预约时间冲突的预约的列表，格式同 [***GET*** `reservation/list`](#reservationlist)

---

#### `reservation/submit`

***POST***

提交预约申请

*请求参数：*
| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `room_id` | room_id：预约的房间id | 是 |
| `date` | 预约日期（例：2021-04-06） | 是 |
| `time_span` | 48位01字符串，1为要预约的时间 | 是 |
| `reason` | 最大长度为255的字符串，预约理由 | 是 |

*响应码：*

除[共通响应码](#共通返回)外，还包括：

| 响应码 | 描述 |
| -------- | -------- |
| 431 | 所选时间已被预约 |
| 432 | 与自己的其他预约时间冲突 |
| 433 | 已被封禁 |

---

#### `reservation/examine`

***PUT***

管理员审批预约

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id` | 预约记录的id | 是 |
| `result` | 审批结果（Boolean，true批准申请，false为拒绝申请） | 是 |
| `reason` | 拒绝理由（String）| `result` 为 false 时必选，否则无需此项 |

---

#### `reservation/cancel`


***PUT***

取消预约

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id` | 预约记录的id | 是 |


---

#### `reservation/list`

***GET***

用于管理员分页获取预约信息列表，默认返回当前用户拥有管理权的所有房间的所有预约信息，按提交时间从新到旧排序

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `page_num` | 列表页数 | 是 |
| `only` | 筛选，详情见表格下方参数详情 | 是 |
| `order_by` | 排序，详情见表格下方参数详情 | 否 |

*参数详情：*

- `only`
    - 若不筛选则传入空值即可
    - 格式：形如 `applicant:2,state__in:WA`，表示只看申请人id为2、状态为等待审批和审批通过的所有预约信息
    - 常规参数：
        - `state`：预约状态，所有的状态列表见 [`state` 状态](#state)
        - `applicant`：申请人id
        - `room`：房间id，需要该房间的管理权限
        - `examined`：`true` 为被审批过，`false` 为未被审批过
    - 特殊参数：
        - `state__in:AF`：筛选权限，此句表示筛选状态为审批通过和已完成的，所有的状态列表见 [`state` 状态](#state)

- `order_by`
    - 若传入空值默认为按提交时间从新到旧排序
    - 可选的值：`submit_time`（提交时间）, `approval_time`（审批时间）
    - 参数值最前面若有 `-` 则为从新到旧排序，否则为从旧到新


*返回示例：*

```json
{
    "total": 1,
    "page_count": 1,
    "list": [
        {
            "id": 172,
            "date": "2021-05-23",
            "apply_reason": "d",
            "submit_time": "2021-05-23T13:25:45.054",
            "approval_result": true,
            "refuse_reason": null,
            "approval_time": "2021-05-23T13:26:53.633",
            "token": "225212",
            "arrival_time": null,
            "leave_time": null,
            "cancel_time": null,
            "applicant": {
                "id": 6,
                "uid": "2019011288",
                "username": "zhoutz19",
                "fullname": "周天泽",
                "is_teacher": false,
                "email": "tz03e@gmail.com",
                "phone_number": "",
                "role": "R",
                "department": {
                    "id": 1,
                    "name": "计算机科学与技术系"
                },
                "institute": {
                    "id": 5,
                    "name": "计算机软件研究所"
                },
                "unban_time": 1620451396093.799,
                "recent_breach": 9
            },
            "room": {
                "id": 14,
                "name": "会议室410",
                "size": "S",
                "capacity": 48,
                "floor": 4,
                "teacher_only": false,
                "cs_only": true,
                "has_screen": true,
                "has_projector": false,
                "has_mic": true,
                "note": "",
                "building": {
                    "id": 1,
                    "name": "新系馆"
                },
                "institute": {
                    "id": 5,
                    "name": "计算机软件研究所"
                }
            },
            "time_span": "000000000000000000000000000000111100000000000000",
            "approval_person": "周天泽",
            "state": "审批通过"
        }
    ]
}

```

### 权限

#### `room_group`

对房间组的增删改查，所有操作均需Root权限

***GET***

获取房间组列表

*返回示例：*

```json
[
    {
        "id": 12,  // 房间组id
        "name": "empty",  // 房间组名
        "rooms": [  // 包含的房间
            {
                "id": 1,
                "name": "会议室501"
            },
            {
                "id": 2,
                "name": "报告厅502"
            }
        ],
        "admins": [  // 有权限的管理员
            {
                "id": 4,
                "fullname": "阿拉贡"
            },
            {
                "id": 6,
                "fullname": "索伦"
            }
        ]
    },
    {
        "id": 15,
        "name": "Ad发啊",
        "rooms": [],
        "admins": [
            {
                "id": 4,
                "fullname": "阿拉贡"
            }
        ]
    }
]
```

***POST***

创建空房间组

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `name` | 组名 | 是 |

*返回示例：*

```json
{
    "id": 6  // 新创建组的id
}
```

***PUT***

- 修改房间组

    *请求参数：*

    | 参数名 | 描述 | 是否必选 |
    | -------- | -------- | -------- |
    | `group_id` | 要修改的组的id | 是 |
    | `name` | 房间组名 | 否 |
    | `rooms` | 房间id构成的列表 | 否 |
    | `admins` | 管理员id构成的列表 | 否 |

    其中 `name`, `rooms`, `admins` 均为要修改为的值

- 为管理员设置房间组

    若请求参数中含有 `admin_id` 一项，则为对管理员设置房间组
    
    *请求参数：*

    | 参数名 | 描述 | 是否必选 |
    | -------- | -------- | -------- |
    | `admin_id` | 管理员id |  |
    | `groups` | 房间组id构成的列表 | 是 |

***DELETE***

删除房间组

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `id` | 房间组id | 是 |


### 终端

#### `terminal/login`

***POST***

用于终端登录，检查token是否正确

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `room_id` | 要登录的房间id | 是 |
| `token` | 对应密码 | 是 |

*返回响应码：*

除[共通响应码](#共通返回)外，还包括：

| 响应码 | 描述 |
| -------- | -------- |
| 420 | room_id或token错误 |

---

#### `terminal/room_info`

***GET***

查看当前会议室信息

*返回示例：*

```json
{
    "id": 1,
    "name": "会议室501",
    "size": "L",
    "capacity": 150,
    "floor": 2,
    "teacher_only": false,
    "cs_only": true,
    "has_screen": false,
    "has_projector": true,
    "has_mic": false,
    "note": "",
    "building": {
        "id": 1,
        "name": "新系馆"
    },
    "institute": {
        "id": 2,
        "name": "人机交互与媒体集成研究所"
    },
    "today": "2021-05-23",  // 当天日期
    "time_span": "000000000000000000000000000000000000000000000000"  // 当天已被预约的时间信息
}
```

---

#### `terminal/arrive`

***POST***

签到确认

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `token` | 预约审批通过后获得的token | 是 |

*返回响应码：*

除[共通响应码](#共通返回)外，还包括：

| 响应码 | 描述 |
| -------- | -------- |
| 210 | 不在预约时间段内 |
| 212 | 已签过到 |
| 420 | token错误 |

*返回示例：*

响应码为 `200`, `210`, `212` 时，会返回对应预约01串格式的 `time_span`：

```json
{
    "time_span": "000000000000000000000000000000111100000000000000"
}
```

---

#### `terminal/leave`

***POST***

签离确认

*请求参数：*

| 参数名 | 描述 | 是否必选 |
| -------- | -------- | -------- |
| `token` | 预约审批通过后获得的token | 是 |

*返回响应码：*

除[共通响应码](#共通返回)外，还包括：

| 响应码 | 描述 |
| -------- | -------- |
| 210 | 还未签到 |
| 211 | 晚退 |
| 420 | token错误 |

*返回示例：*

响应码为 `200`, `210`, `211` 时，会返回对应预约01串格式的 `time_span`：

```json
{
    "time_span": "000000000000000000000000000000111100000000000000"
}
```


## 前端设计

前端页面渲染逻辑如下：在主目录`$MAIN_DIR`下的`index.html`使用一个id为CSOrder的盒。`$MAIN_DIR/src/main.js`创建了CSOrder这个vue应用，它使用vue-router，并将CSOrder作为应用唯一的组件。主组件`$MAIN_DIR/src/CSOrder.vue`将router-view包装在一个盒中。router-view实际上根据路由渲染各个网页，这些网页组件实现在`$MAIN_DIR/src/views`目录下。其中，一部分网页用到了一些子组件，这些子组件实现在`$MAIN_DIR/src/components`目录下。

以下自底向上，说明各个网页主要的设计：

### 1.`$MAIN_DIR/src/components`中的组件

#### 1.1 NaviBar

**使用子组件：无**

**被应用于组件：2.1 2.3 2.4 2.5 2.6 2.7 2.8 2.9 2.10**

各个网页的统一化导航栏，位于页面的最上方。该组件在用户未登录时，提供“用户登录”和“会议室公共终端”两个菜单选项。在用户登录时，根据用户的角色权限（普通用户/管理员/超级管理员），提供可用的网页菜单选项。用户可以点击菜单选项进入对应页面。特别地，为了防止误操作，公共终端页面的导航栏不提供任何菜单选项。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `LOCALHOST` |String | 记录项目运行的根url，用于后端正确定位前端 |
| `Authorized` |Boolean| 记录用户是否真实登录 |
| `TextContent` |String| 向用户显示的信息文字 |
| `ShowLogin、ShowManager`等 |Boolean| 控制各个菜单选项的显示与隐藏 |
| `MenuIndex` |String | 记录当前导航栏所在菜单位置 |
| `ExamineTotal`|Number| 提示当前需要审批的预约数量|

**created ()**

根据环境配置`LOCALHOST`。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `Login` |无 | 用户登录，跳转到与Oauth验证相关的url |
| `Logout` |无 | 用户退出登录，删除token并转为登出状态 |
| `LoginStatus` |`val` | 设置`MenuIndex`为`val`，并转为登录状态 |
| `LogoutStatus` |无 | 转为登出状态 |
| `TerminalLogin` |无| 打开终端登录框（组件1.3） |
| `Refresh` |无| 刷新页面 |
| `RoomReserve、Index`等 |无| 处理用户点击菜单栏的选项，跳转到各个页面 |
| `SaveUserInfoAndJudge` |无| 向后端发送请求，若成功则保存用户信息，并判断其角色权限来决定显示的菜单选项 |


#### 1.2 FooterBar

**使用子组件：无**

**被应用于组件：2.1 2.3 2.4 2.5 2.6 2.7 2.8 2.9 2.10**

各个网页的统一化页尾栏，位于页面的最下方。这是一个静态组件，各种情况下渲染结果均相同。

#### 1.3 TerminalLoginDialog

**使用子组件：无**

**被应用于组件：2.1**

会议室公共终端登录框，提供会议室id和token两个输入表单，用于终端的登录。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `DialogVisible` |Boolean | 控制该组件是否显示 |
| `RoomId` |String | 记录终端对应的会议室id |
| `Token` |String | 记录终端登录所需的token |

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `Login` |无 | 向后端发送含RoomId和Token的请求，验证其合法性，若合法则跳转到对应的会议室终端页面 |
| `Cancel` |无 | 清空表单内容，取消该组件的显示 |

#### 1.4 InfoBlock

**使用子组件：无**

**被应用于组件：2.4**

展示、修改个人信息（电话、邮箱和研究所）。

**主要data**

| 名称| 类型|功能|
| -------- | -------- | -------- |
| `phone_`|String |展示或修改的电话|
| `email_`|String |展示或修改的邮箱| 
|`institute_`|Number |展示或修改的研究所id|

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `SaveUserInfoAndJudge`| 无|获取后端传来的个人信息，将它们展示出来
| `Save` | formname | 保存修改后的电话、邮箱和研究所|


#### 1.5 TextBlock

**使用子组件：无**

**被应用于组件：1.7**

提供一种封装好样式的文本框。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `TextBlockStyle` |struct | 记录文本框的css样式 |
| `Content` |String | 记录文本框的内容 |

**watch**

| 监听的props |  操作 |
| -------- | -------- | 
| `width、height、color`等 | 修改`TextBlockStyle` |
| `content` | 修改`Content` |

#### 1.6 RoomCalendarLine

**使用子组件：无**

**被应用于组件：1.7**

会议室时间表的一行，是会议室时间表（组件1.7）的基本构成组件。它能将一个48位控制串对应到一天中的各个半小时，通过串的内容用不同的颜色显示该时间段的状态（可用/不可用/自己已预约/自己正预约）。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `Name` |String | 这一行对应的会议室名称 |
| `Column` |String | 控制这一行对应的颜色显示 |

**watch**

| 监听的props |  操作 |
| -------- | -------- | 
| `name` | 修改`Name` |
| `string` | 修改`Column`，并改变颜色显示 |

**created ()**

初始化一个链接到会议室的按钮，及30个显示颜色用的盒。

#### 1.7 RoomCalendarBlock

**使用子组件：1.5 1.6**

**被应用于组件：2.3 2.5 2.6**

会议室时间表。直观地显示一系列会议室在多日的各个时间段内被预约的情况。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `List` |Array | 会议室列表 |
| `TimeColumn` |Array | 静态显示各个时间分段 |
| `DateColumn` |Array | 显示各个日期菜单 |
| `Today` |String | 今天的日期 |
| `DayRange` |Number | 总共显示的日期按钮数 |
| `DateId` |Number | 当前时间表显示的日期 |

**watch**

| 监听的props |  操作 |
| -------- | -------- | 
| `list` | 修改`List`，并更新时间表的显示 |
| `today` | 修改`Today`，并更新时间表的显示 |
| `dayRange` | 修改`DayRange`，并更新时间表的显示 |

**created ()**

初始化`TimeColumn`和`Today`，并初始化时间表的显示。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `DateSync` |y,m,d | 接受年、月、日参数，计算`DateColumn`并修改相关组件的显示样式|
| `RoomInfo` |id | 接受会议室id，跳转到对应的会议室详情页 |
| `DateChange` |id | 接受日期id，修改`DateId`并更新时间表的显示 |

#### 1.8 CollapsePanel
**被应用于组件：2.8**

折叠面板，用于展示用户个人的历史预约记录。

**data**
| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `isCollapsed` |Boolean | 记录面板是否展开 |
| `showTokenText` |Boolean | 记录是否以明文展示口令 |
| `switchValue` |String | 显示口令按钮的提示文字 |

**props**
| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `resInfo` |Object | 接受父组件传递的详细预约信息 |

**主要computed**
| 名称 |  返回值类型|功能 |
| -------- | -------- | -------- |
| `startTime` |Number | 从`resInfo.timeSpan`中获取预约会议开始时间 |
| `endTime` |Number |从`resInfo.timeSpan`中获取预约会议结束时间 |
| `timeSpanString` |String | 根据`startTime`和`endTime`获取预约会议的时间段字符串  |
| `approvalResultString` |String | 根据`resInfo`获取本次预约的审批结果 |
| `approvalResultBgColor` |String | 根据`resInfo`选择审批结果的背景颜色 |
| `cancelable` |Boolean | 根据`resInfo`判断本次预约是否可取消 |
| `useResultString` |String | 根据`resInfo.state`返回本次预约的使用结果 |
| `stepActiveIndex` | Number | 根据`resInfo`返回预约进度条被激活步骤的最大索引 |
| `finishStepStatus` | String | 根据`resInfo.state`返回预约进度条最后步骤的状态 |
| `finishStepTitle` | String | 根据`resInfo.state`返回预约进度条最后步骤的说明文字 |
| `waitEaxmineStatus` | String | 根据`resInfo`返回预约进度条等待审批步骤的状态 |
| `waitEaxmineTitle` | String | 根据`resInfo`返回预约进度条等待审批步骤的说明文字 |
| `waitUseStatus` | String | 根据`resInfo`返回预约进度条等待使用步骤的状态 |
| `waitUseTitle` | String | 根据`resInfo`返回预约进度条等待使用步骤的说明文字 |

**methods**
| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `handleCollapse` |无 | 将`isCollapsed`的值取反，控制面板的展开和收起|
| `cancelReservation` |无 | 向父组件发送取消预约的信号，并将`resInfo`传递给父组件 |
| `tokenVisibleChange` |无 | 将`showTokenText`的值取反，控制口令以明文或密文形式显示 |

### 2.`$MAIN_DIR/src/views`中的组件

#### 2.1 Index

**使用子组件：1.1 1.2 1.3**

**被应用于组件：3**

网站的主页，其核心功能基本被导航栏（组件1.1）包含。当用户处于未登录状态或某操作权限不足时，会自动跳转到该页面，并不能获得任何有价值信息。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `DialogVisible` |Boolean | 控制终端登录框是否显示 |

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录则调用导航栏的`LoginStatus`方法，否则调用其`LogoutStatus`方法。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `TerminalLogin` |无 | 显示终端登录框|
| `Cancel` |无 | 隐藏终端登录框 |

#### 2.2 LoginRedirect

**使用子组件：无**

**被应用于组件：3**

一个简单的登录跳转页，等待后端的验证结果，在Oauth验证成功后跳转回网站主页。

**created ()**

先根据环境配置LOCLALHOST，再从url中获取Oauth验证的`auth_code`并通过请求发送给后端。若验证成功，则根据后端返回的token对应设置cookie中的`api_token`字样，最后跳转回主页；若验证失败，直接跳转回主页，不设置cookie。

#### 2.3 Terminal

**使用子组件：1.1 1.2 1.7**

**被应用于组件：3**

会议室公共终端页，显示了会议室的详细信息，并用时间表显示会议室当天的被预约情况。提供签到和签退功能，用户需要使用预约成功后获得的token进行操作，终端会反馈签到和签退的信息。原则上，该页面在会议室的门口展示，故一旦进入就无法退出（除非跳转url）。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `RoomInfo` |struct | 记录终端对应的会议室信息 |
| `ArriveToken` |String | 记录签到token |
| `LeaveToken` |String | 记录签退token |
| `Timer` |setInterval | 定时器，每隔1s触发一次定时时间 |
| `NowTime` |struct | 记录当前时间 |

**mounted ()**

通过读取cookie中的`terminal_token`字样，并向后端发送请求来检测终端登录状态。如果已登录则调用导航栏的`LoginStatus`方法，设置`Timer`并从返回值重读取并保存会议室信息。否则返回主页。

**destroyed ()**

取消`Timer`的计时。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `HandleAsideSelect` |key | 根据key值来判断侧边菜单栏的选项，从而改变显示|
| `SubmitArrive` |无 | 签到，读取`ArriveToken`并向后端发送请求，若成功则提示会议的时间段，否则根据后端返回状态码提示错误 |
| `SubmitLeave` |无 | 签退，读取`LeaveToken`并向后端发送请求，若成功则提示成功，否则根据后端返回状态码提示错误 |
| `SetData` |res | 根据返回信息res设置会议室基本信息，用于显示|
| `TimeEvent` |无 | 定时事件，每秒获取当前时间并显示。每5分钟刷新页面|

#### 2.4 Info
**使用子组件：1.1 1.2 1.4**

**被应用于组件：3**

展示和修改个人信息的页面。用户可修改并保存自己的手机、邮箱和所属研究所，其他信息只可查看。
只有合法的信息才能保存，且邮箱为必填项。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `InfoBlockStyle` |struct | 控制信息框（组件1.4）的显示样式 |

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录则调用导航栏的`LoginStatus`及信息框的`SaveUserInfoAndJudge`方法，否则返回主页。


#### 2.5 RoomReserve

**使用子组件：1.1 1.2 1.7**

**被应用于组件：3**

预约主页（会议室列表页）。该页面将用户可预约的所有会议室展示在时间表中，并可以查询会议室以及筛选列表中的会议室。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `Tips` |Array | 记录预约须知 |
| `Help` |Array | 记录预约帮助 |
| `Search` |struct | 记录会议室查询的参数 |
| `List` |Array | 记录筛选后显示的会议室列表 |
| `FullList` |Array | 记录完整的会议室列表 |
| `SizeType、BuildingType`等 |String | 会议室筛选的选项 |

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录则调用导航栏的`LoginStatus`方法，并再次向后端请求获取会议室列表，成功后保存会议室信息并显示。否则返回主页。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `HandleAsideSelect` |key | 根据key值来判断侧边菜单栏的选项，从而显示隐藏的对话框等|
| `Filt` |key | 筛选。改变筛选的选项，并从`FullList`中根据选项获得 `List`，并将其显示在时间表中|
| `OnSearchRoomSubmit` |无 | 直接在`FullList`中搜索符合条件的会议室，若找到唯一的会议室则进入该会议室详情页，否则提示错误 |

#### 2.6 RoomInfo

**使用子组件：1.1 1.2 1.7**

**被应用于组件：3**

会议室详情页。展示会议室的位置、名称、设备等基本信息，以及预约条件。如果用户管理该会议室，可以分页查看该会议室的预约记录列表。任何用户都可以在自己可查看的会议室进行预约，预约需要选择合法的时间段并填写预约理由。

**页面参数**

进入该页面需要在vue-router中传入参数`RoomId`。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `isAdmin` |Boolean | 用户是否管理该会议室，即能否看到预约列表 |
| `roomResList` |Array | 记录该会议室的预约记录 |
| `filteredRoomResList` |Array | 记录筛选后的会议室预约记录 |
| `ReserveRules` |Array | 记录预约须知 |
| `RoomInfo` |struct | 记录该会议室信息 |
| `DayPickerOptions` |struct | 记录日期栏的属性 |
| `ReservationReason` |String | 记录预约理由 |
| `dates` |Array | 记录可用的预约日期 |
| `active_date` |String | 记录当前选择的日期 |
| `sliderValid` | Boolean| 记录预约时间滑条是否有效 |
| `sliderRange` | Array| 含两个数的数组，记录预约的时间段 |

**computed**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `slider_style` |struct | 实时监听预约时间栏的日期选择、滑条位置并改变显示 |

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录则调用导航栏的`LoginStatus`方法，并读取传入的参数`RoomId`，再次向后端请求获取该会议室信息，成功则保存会议室信息并显示。若权限认证失败则返回主页，若获取会议室信息失败则返回预约主页（组件2.5）。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `HandleAsideSelect` |key | 根据key值来判断侧边菜单栏的选项，从而在右侧显示一个特定的页面|
| `SetData` |res | 根据后端返回的res设置会议室基本信息、预约时间栏的显示等|
| `SubmitReservation` |无 | 读取`active_date`、`sliderRange`和`ReservationReason`，首先判断合法性，若合法则向后端发起预约请求。若预约成功则更新信息，若失败则提示对应的错误 |
| `getRoomResHistory` |pageNum| 向后端请求第pageNum页的会议室预约信息，若成功则保存，否则提示错误|
| `getTimeSpanString` |date,timeSpan| 用于在时间栏中显示选择的时间段|
| `formatTooltip` |value| 将时间数value格式化为小时:分钟显示|


#### 2.7 RoomExamine
**使用子组件：1.1 1.2**

**被应用于组件：3**

管理员审批预约申请、查看已审批记录的页面。审批预约申请分同意和拒绝两种操作，若拒绝则需要填写拒绝理由。若同意一个与其他申请有冲突的请求，会弹出提示确认。审批记录可以分页查看。

**主要data**

| 名称 |  类型|功能 |
| --------|--------|--------|
| `ReserveList`| Array | 预约申请列表或审批记录列表 |
| `ConflictList`| Array | 预约冲突列表|
| `pagenumber`| Number | 预约申请列表或审批记录列表当前页数 |
| `dialog_refuse_visible`| Boolean |是否显示拒绝对话框 |
| `dialog_room_info_visible`| Boolean |是否显示房间信息展示对话框|
| `dialog_conflict_visible`| Boolean |是否显示预约冲突对话框|
| `state_`| String | 当前展示的列表的状态 |
| `roominfo_siteroominfo_name`等| String | 预约房间的各种信息 |

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `get`| val| 获取第val页的预约申请列表或预约记录列表|
| `agree_` | result reason id|同意申请 |
| `refuse` | 无|拒绝申请|
| `get_conflict`| val|获取第val页的预约冲突列表|
| `refuse_conflict`|无|拒绝预约冲突的申请|
| `showroominfo`| id| 获取并展示房间id为id的房间信息|
| `handleClick`|tab| tab:first 切换为查看预约申请列表 tab:second 切换为查看审批记录| 

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录并且有管理员权限则调用导航栏的`LoginStatus`方法，否则提示错误并返回主页。

#### 2.8 UserReservationHistory
**使用子组件：1.1 1.2 1.8**

**被应用于组件：3**

个人预约记录页。可以分页查看自己处于各种状态（未被审批、已被审批、未按时到达、已完成、已取消等）的预约记录。选中任意一条预约记录，可以查看其详细信息（包括预约时间、预约理由、审批情况、以及预约成功后用于终端签到的token）等。未使用的预约，也可以在该页面取消。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `allReservationList` | Array |全部预约记录 |
| `dishonestReservationList` | Array | 违约记录 |
|`fulfilledReservationList`| Array |已使用预约记录 |
|`upcomingReservationList`| Array |待使用预约记录|
|`cancelledReservationList`| Array |已取消预约记录|
|`rejectedReservationList`| Array |未通过预约记录|
|`unexaminedReservationList`| Array |待审批预约记录|
|`expiredReservationList`| Array |已失效预约记录|
|`activeList`| Array |当前展示的预约记录|
|`activeListIndex、activePageNum、itemPerPage`| Number |分页信息|

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录并且有管理员权限则调用导航栏的`LoginStatus`方法，否则提示错误并返回主页。

**主要methods**
| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `handleAsideSelect` | key |查看选项`key`对应的预约记录 |
| `handleCurrentChange` | val | 跳转到第`val`页|
| `cancelReservation` | resInfo | 取消`resInfo.id`对应的预约|
| `updateResList` | res | 用`res.data`更新预约记录|


**computed**
| 名称 |  返回值类型|功能 |
| -------- | -------- | -------- |
| `activeListSliceStart` | Number |计算`activeList`切片的起始元素索引 |
| `activeListSliceEnd` | Number |计算`activeList`切片的终止元素索引 |

#### 2.9 UserPermissionManage

**使用子组件：1.1 1.2**

**被应用于组件：3**

用户权限管理页，仅超级管理员可见。可以看到其他所有用户并进行筛选、排序。可以修改非超级管理员的其他用户的角色（管理员/普通用户）、身份（教师/非教师）、所属研究所信息。同时，可以对非超级管理员的其他用户进行封禁和解封操作，封禁时间可设定。若一个用户处于封禁状态，则不能够进行预约（已经完成的预约不受影响）。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `ShowRoleChangeDialog` | Boolean | 是否显示权限修改框 |
| `UserName、UserId`等 | String | 记录当前操作用户的信息 |
|`institute_filters`| Array | 筛选研究所 |
|`role_filters`| Array | 筛选角色 |
| `userlist`| Array | 用户列表 |
| `orderBy`| String | 通过姓名/学号排序 |
| `search_select`| String| 选择搜索姓名或学号 |
| ``search_content``| String| 搜索的内容 |

**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录并且有超级管理员权限则调用导航栏的`LoginStatus`方法，并获取第1页的用户列表。否则提示错误并返回主页。

**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `OpenRoleChange` |val | 根据用户学工号val匹配到该用户，将该用户信息保存到`UserName`、`UserId`等串中，并打开权限修改框|
| `RoleChange` |无 | 读取修改后的用户信息并判合法性，合法则向后端发送权限修改请求。若成功则再次发送请求更新用户信息列表并关闭权限修改框，失败则提示错误|

#### 2.10 RoomInfoManage  
**使用组件：1.1 1.2**

**被应用于组件：3**

房间信息管理页面。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `addGroupForAdminDialogVisible` | Boolean |为管理员添加房间组对话框的可见性|
|`basicInfoDialogVisible`| Boolean |修改会议室信息对话框的可见性 |
|`roomGroupDialogVisible`| Boolean |增加房间组对话框的可见性|
|`addRoomDialogVisible`| Boolean |增加会议室对话框的可见性|
|`addRoomGroupDialogVisible`| Boolean |增加或修改房间组对话框的可见性|
|`showModifyRoomGroup`| Boolean |修改房间组|
|`showRoomList、showAdminList、showRoomGroup`| Boolean |展示会议室列表、管理员列表或房间组列表|
| `groupForAdminForm` | Object |为管理员添加的房间组|
|`institutes`| Object |全部研究所的基本信息|
|`selectedRoom、selectedAdmin`| Array |在对话框的复选框中被勾选房间或管理员|
|`roomList、adminList、roomGroupList`| Array |会议室列表、管理员列表或房间组列表|
|`roomFilterForm、adminFilterForm、groupFilterForm`| Object |会议室、管理员或房间组的筛选信息|
|`filteredRoomList、filteredAdminList、filteredRoomGroupList`| Array |筛选出的会议室列表、管理员列表或房间组列表|
| `modifiedRoomForm、roomGroupForm` | Object |修改后的会议室信息或房间组信息|
| `rootRoomRules` | Object |新增会议室的信息字段限制条件|
| `roomGroupRule` | Object |新增或修改房间组的信息字段限制条件|


**mounted ()**

通过读取cookie中的`api_token`字样，并向后端发送请求来检测登录状态。如果已登录并且有管理员权限则调用导航栏的`LoginStatus`方法，否则提示错误并返回主页。

**主要methods**
| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `handleAsideSelect` | key |查看选项`key`对应的列表 |
| `handleResetFilterRoomForm` | 无 | 情况会议室列表的筛选条件|
| `handleRoomFilterFormSubmit` | 无 | 根据`roomFilterForm`筛选会议室|
| `addGroupForAdmin` | adminId | 显示为管理员添加房间组对话框，修改`groupForAdminForm.id`|
| `cancelModifyGroupForAdmin` | 无 | 清空`groupForAdminForm`，关闭对话框|
| `confirmModifyGroupForAdmin` | 无 | 将`groupForAdminForm`发送给后端，关闭对话框|
| `handleGroupForAdminSelectionChange` | selectedGroups | 修改`groupForAdminForm.selectedGroups`|
| `handleResetFilterAdminForm` | 无 | 清空`adminFilterForm`，显示全部管理员列表|
| `handleAdminFilterFormSubmit` | 无 | 根据`adminFilterForm`筛选管理员|
| `resetAllFilterForm` | 无 | 清空`roomFilterForm、adminFilterForm、groupFilterForm`|
| `getRootRoomList` | 无 | 与后端通信获取会议室列表，更新`roomList`|
| `getAdminList` | 无 | 与后端通信获取管理员列表，更新`adminList`|
| `handleModifyRootRoom` | index | 显示修改会议室信息对话框|
| `handleCancelModifyBasic` | 无 | 清空`modifiedRoomForm`，关闭对话框|
| `handleConfirmModifyBasic` | 无 | 将`modifiedRoomForm`发送给后端，用于修改会议室信息，关闭对话框|
| `handleAddRootRoomSubmit` | 无 | 显示增加会议室对话框，清空`modifiedRoomForm`|
| `resetAddRootRoom` | 无 | 清空`modifiedRoomForm`|
| `handleAddRootRoom` | 无 | 检验`modifiedRoomForm`字段的合法性后，将`modifiedRoomForm`发送给后端，用于增加会议室，关闭对话框|
| `handleDeleteRootRoom` | id | 弹出提示框，用户点击确定后将待删除会议室id发送给后端，删除成功后更新会议室列表|
| `handleGroupRoomSelectionChange、handleGroupAdminSelectionChange` | selectedRows | 更新`roomGroupForm.selectedRooms`或`roomGroupForm.selectedAdmins`|
| `handleAddRoomGroupSubmit` | 无 | 清空`roomGroupForm`，显示增加房间组对话框|
| `resetRoomGroupForm` | 无 | 清空`roomGroupForm`|
| `getGroupList` | 无 | 与后端通信获取房间组列表，更新`roomGroupList`|
| `handleCancelRoomGroupSubmit` | 无 | 清空`roomGroupForm`，隐藏对话框|
| `handleConfirmRoomGroupSubmit` | 无 | 将`roomGroupForm`发送给后端，用于新增或修改房间组，隐藏对话框|
| `handleModifyRoomGroup` | groupId | 显示修改房间组对话框，在复选框中勾选groupId对应房间组已有的房间和管理员|
| `handleDeleteRoomGroup` | groupId | 弹出提示框，用户点击确定后将groupId发送给后端，用于删除该房间组，删除成功后更新房间组列表|
| `getRoomGroupForAdmin` | id | 获取id对应管理员所管辖的全部房间组|
| `resetGroupFilterForm` | 无 | 清空`groupFilterForm`,展示全部房间组列表|
| `confirmGroupFilterForm` | 无 | 根据`groupFilterForm`筛选房间组|


### 3.`$MAIN_DIR/src/CSOrder.vue`

**使用子组件：<router-view>（相当于使用了2中的每个组件）**

**被应用于组件：4中的new Vue()**

项目主组件，使用vue-router来链接到各个页面组件完成实际的渲染。

**主要data**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `Show` |Boolean | 控制整个盒子是否显示，用于重新加载 |

**provide ()**

| 名称 |  类型|功能 |
| -------- | -------- | -------- |
| `PageReload` |function | 提供给每个子组件的重新加载方法 |

**mounted ()**

禁用F5和ctrl+R两种快捷键来刷新页面，并禁用右键菜单。
    
**主要methods**

| 名称 |  参数|功能 |
| -------- | -------- | -------- |
| `Reload` |无 | 通过将`Show`设为0而在下一刻将`Show`设为1来完成对页面的刷新|

### 4.`$MAIN_DIR/src/main.js`

**创建组件：new Vue（）**    
    
**使用子组件：3**
    
**特殊行为**
    
监听window.onbeforeunload事件，在其触发时删除cookie中的`api_token`字样。实际上在页面刷新、关闭、输入url跳转时都会触发这一事件，导致退出登录。
    
    
## 后端设计

### 返回函数

为了尽可能使视图函数的返回格式一致以及编写简洁，在`views/views_response.py`中定义了以下用于生成返回值的函数：
    
| 函数 | 响应码 | 数据 | 描述|
| --- | --- | --- | --- |
| gen_response(code, data) | code | data | 通用接口 |
| success(data='success') | 200 | data | 请求成功 |
| not_logged_in() | 401 | 'Login timeout or not logged in' | 登录过期或未登录 |
| method_not_allowed(method) | 405 | 'Method {method} not allowed' | 请求的方法不被允许 |
| bad_request(info) | 400 | info | 请求的格式或参数错误 |
| invalid_format() | 400 | 'Invalid format' | 请求的格式错误 |
| missing_parameter(param) | 400 | 'Missing required parameter \`{param}`' | 缺少参数 |
| type_error(param, expected_type, param_type) | 400 | 'Parameter \`{param}\` expected type \`{expexted_type}\` but found \`{param_type}\`' | 参数类型错误 |
| invalid_value(param='', value='') | 400 | 'Invalid value' 或 'Invalid value for parameter \`{param}\`: {value}' | 输入的参数不合法 |
| no_permission() | 403 | 'No permission' | 该用户无权访问 |

视图函数会尽可能选择较为详细的返回值函数以向前端提供信息
    
### 输入数据处理

为便捷地获取输入数据并判断合法性，在`views/request.py`中实现了统一的数据处理接口
    
#### `get_body(request)`

获取传入json格式数据的请求的数据
    
#### `get_params(params_dict, param_type_dict)`

可以便捷地从传入数据中获取各个参数
    
`params_dict` 在 ***GET*** 请求时为 `request.GET`，其他请求时为 [`get_body(request)`](#get_bodyrequest)

`param_type_dict` 为需要获取的参数名和对应类型的字典

例如可以用
```python
[a,b] = get_params(request.GET, {'a': int, 'b': str})
```
从 ***GET*** 请求的 `request` 对象中获取整数参数 `a` 和字符串参数 `b`。另外，当请求类型为 ***GET*** 时所有的参数一开始都会被认为是`str`类型，为了便于使用，如果需求 `int` 类型但参数类型为 `str` 时函数会尝试进行类型转换。
    
#### `trans_dict(only)`

可以将部分视图函数用于筛选的参数 `only` 从字符串转成字典的格式
    
当获取参数时遇到格式错误、缺少参数、参数类型错误等问题时会抛出 `GetParamError` 异常，从异常的 `response` 成员可以获取视图函数应该返回的错误信息

视图函数中除了需要单独判断的特殊参数，尽可能多使用统一的获取参数接口可以使代码更加简单、清晰并减少潜在的问题
    
### 定时检测

为了实现自动邮件提醒和预约状态实时变更（如过期、迟到等）的功能，后端在 `wsgi.py`（即Django开启后）中新建一个线程执行 `check.py` 中的 `solve()` 函数
    
`solve()`函数会不断运行，并以分钟为单位进行检测，每分钟检查所有可能要提醒或可能状态变更的预约记录。所有时间会被取整为分钟（取最近的分钟），如果某条预约记录的提交时间或预约时间与当前时间相差的分钟数恰好为某个设定值，函数会进行邮件提醒或状态变更。由于检测的预约不会太多，一分钟的时间足以完成一次检测。


# 测试及部署

## 前端

### 测试

使用Jest + Vue Test Utils进行单元测试

#### 运行测试

单元测试使用jest的默认配置`jest.conf.js`。`package.json`中配置如下：

```
"scripts": {
    "test": "npm run unit -- -u 2>console.txt 1>coverage.txt"
}
```

运行单元测试使用`npm test`，这实际上运行了`npm run unit`，并将控制台输出保存至主目录下的`console.txt`，覆盖率输出保存至主目录下的`coverage.txt`。这样方便查看单元测试的结果信息。

#### 测试方法及结果

前端单元测试代码所在目录为`$MAIN_DIR/test/unit/specs`

单元测试包含三个部分：

- 一是渲染正确性测试，文件为`snapshot.test.js`。它生成各种组件的快照，并在下一刻将得到的html与之比对，以确认组件渲染正确。具体而言，它使用了Vue Test Utils的`mount`方法来渲染组件，并使用jest的`expect`方法来验证正确性、`toMatchSnapshot`方法来匹配快照。

- 二是监听测试，文件为`watch.test.js`。它对组件中的一些数据进行修改，并确认组件能够正确监听到变化并作出修改。这种测试方法应用于几个不需要权限验证的子组件。同样使用`mount`和`expect`方法，同时还运用了Vue Test Utils的`setProps`和`setData`方法用于修改数据。

- 三是页面完整测试。这一部分是单元测试的核心，涉及到的组件较多，分为多个后缀为`.test.js`的文件。它针对一个具体的页面，模拟权限认证、按钮点击、输入表单等用户的真实行为，并模拟后端的返回数据，来完整地测试一个组件的正确性。由于前端向后端发送请求全部使用`fetch`的异步请求，故在测试中用`jest.fn()`方法对`fetch`进行mock，控制返回的假数据，从而模拟一个“假后端”。测试的假数据集中保存在`test_data.js`中。同时，使用Vue Test Utils的`findAll`或`find`方法，定位到页面中的一个组件，从而模拟用户的点击、输入等行为，进而能够覆盖该页面中的一些方法和数据监听、修改等。

有效的单元测试需要针对各个页面进行精确的组件行为模拟、后端假数据模拟，还需要考虑不合法的分支、可能的错误操作等，比较复杂且与页面耦合性大。由于项目进入后期，前端页面结构变化较大，且某些复杂页面的单元测试遇到困难，最终我们只实现了一部分页面和组件的测试。覆盖率约为35%。


### 部署

- 项目需求: 
  ```
  npm=6.14.11 
  node=14.15.5
  ```
  
- 服务器上运行：
  ```
  # install node_modules
  npm install
  
  # build
  npm run build
  
  # test
  npm run lint
  npm test
  
  # deploy
  # do something to deploy
  ```

- 在nginx容器中，连接到后端需要反向代理，在主目录下设置nginx目录，存放`frontend.conf`：
  ```conf=
  server {
    listen 80;
    server_name default_server;
    root /opt/app/dist;
  
    location / {
        try_files $uri $uri/ @router;
        index  index.html index.htm;
    }
  
    location @router {
        rewrite ^.*$ /index.html last;
    }
  
    location ^~ /api {
      proxy_pass http://tianze.ml:8000/api;
    }
  }
  ```

  

## 后端

### 测试

使用 `django.test` 中的 `TestCase`
    
为了便于编写单元测试，我们在`tests/case.py`中由`TestCase`类派生了`ViewsTestCase`类，其中实现了一些简单的测试用功能

#### 测试用数据库

由于单元测试可能并发，若测试数据库使用同一个会出现问题，所以我们自定义了一个Mariadb镜像

`Dockerfile`：
```dockerfile=
FROM mariadb:10.5

ENV WORK_PATH /usr/local/work
ENV AUTO_RUN_DIR /docker-entrypoint-initdb.d
ENV FILE_0 init.sql
ENV INIT_SHELL init.sh

RUN mkdir -p $WORK_PATH

COPY ./$FILE_0 $WORK_PATH/
COPY ./$INIT_SHELL $AUTO_RUN_DIR/

RUN chmod a+x $AUTO_RUN_DIR/$INIT_SHELL
```

`init.sh`：
```shell=
#!/bin/bash
mysql -uroot -p$MYSQL_ROOT_PASSWORD <<EOF
source $WORK_PATH/$FILE_0;
```

`init.sql`：
```sql=
CREATE DATABASE django_test DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

use mysql;
UPDATE user SET host = '%' WHERE user = 'root';
```

并在ci配置文件中添加环境变量 `MYSQL_ROOT_PASSWORD` 为 `测试用数据库的密码`

#### Pytest

由于Django测试只能在 `settings.py` 中设置测试用的数据库名，而不能切换为其他的数据库服务，所以我们使用 `Pytest` 并指定另一个使用测试数据库的 `settings_test.py`

其配置文件 `pytest.ini` 如下：
```ini=
[pytest]
addopts = --nomigrations
DJANGO_SETTINGS_MODULE = backend.settings_test  ;指定settings文件
```


### 部署

- Python环境最好为 `3.8.5`
- 安装需要的库：`pip install -r requirements.txt`
- 运行：`python manage.py runserver [IP:DOMAIN]`

也可根据如下Dockerfile构建Docker镜像：
```dockerfile=
FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . /usr/src/app

# For Django
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
```

