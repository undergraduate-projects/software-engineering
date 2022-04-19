from datetime import timedelta

# 登录token失效时间
token_expire_timedelta = timedelta(hours=1)

# 签到允许延迟时间
ARRIVAL_LATENCY = timedelta(minutes=20)
# 签退允许延迟时间
LEAVE_LATENCY = timedelta(minutes=5)

# 会议开始前提醒
START_REMIND_TIME = [timedelta(minutes=30)]
# 提交申请后提醒管理员审批
APPROVE_REMIND_TIME = [timedelta(hours=6), timedelta(hours=12)]

# 允许申请日期范围
DAY_RANGE = 14
# 允许学生申请日期范围
STUDENT_DAY_RANGE = 7

# 24小时每隔半小时为一个预约时间段，允许预约时间为[START_TIME,END_TIME) 即[8:00,23:00)
TIME_SPAN_LENGTH = 48
START_TIME = 16
END_TIME = 46

# 每页的用户数/预约数
USER_PER_PAGE = 10
RES_PER_PAGE = 10

# 验证格式的正则表达式
email_re = r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}'
phone_re = r'(13|14|15|17|18|19)[0-9]{9}'

# 用于识别计算机系
CS_NAMES = ['计算机系', '计算机科学与技术系']

GET = 'GET'
PUT = 'PUT'
POST = 'POST'
