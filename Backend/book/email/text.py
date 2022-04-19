RES_REMIND_TEXT = '''
<html>
<head>
<style>
body {{{{
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
}}}}
</style>
</head>
<body>
<h2>{{}}：</h2>
<p>&nbsp;</p>
<p style="padding-left: 40px;"><span style="font-size: 12pt;">您预约的时间为 <strong><span style="color: #e67e23;">{}</span></strong> 的 <strong><span style="color: #3598db;">{}</span></strong> 还有30分钟开始，请按时到达。</span></p>
<p>&nbsp;</p>
<p style="padding-left: 40px;"><span style="font-size: 12pt;">签到码：</span></p>
<div style="text-align: center; font-size: 16pt; color: #843fa1;"><strong>{}</strong></div>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="color: #7e8c8d;">清华大学计算机系会议室管理系统</span></p>
</body>
</html>
'''

APPROVE_REMIND_TEXT = '''
<html>
<head>
<style>
body {{{{
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
}}}}
</style>
</head>
<body>
<h2>{{}}：</h2>
<p style="padding-left: 40px; font-size: 12pt;">以下预约申请已有{}小时未审批，请及时查看：</p>
<center>
<table style="border-collapse: collapse; width: 70%; font-size: 12pt;" border="1">
<tbody>
<tr style="height: 22px;">
<td style="width: 50%; height: 22px;">预约人</td>
<td style="width: 50%; height: 22px;">{}</td>
</tr>
<tr style="height: 22px;">
<td style="width: 50%; height: 22px;">提交时间</td>
<td style="width: 50%; height: 22px;">{}</td>
</tr>
<tr style="height: 22px;">
<td style="width: 50%; height: 22px;">申请时间段</td>
<td style="width: 50%; height: 22px;">{}</td>
</tr>
<tr style="height: 22px;">
<td style="width: 50%; height: 22px;">申请会议室</td>
<td style="width: 50%; height: 22px;">{}</td>
</tr>
<tr style="height: 22px;">
<td style="width: 50%; height: 22px;">申请理由</td>
<td style="width: 50%; height: 22px;">{}</td>
</tr>
</tbody>
</table>
</center>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="color: #7e8c8d;">清华大学计算机系会议室管理系统</span></p>
</body>
</html>
'''

PASS_EXAMINE_TEXT = '''
<html>
<head>
</head>
<body>
<h2 style="text-align: left;"><strong>{}：</strong></h2>
<p style="text-align: center;">&nbsp; &nbsp; 恭喜你！你申请在<strong><span style="color: #3598db;">{}</span></strong>使用<strong><span style="color: #3598db;">{}</span></strong>的请求已经通过审批。</p>
<p style="text-align: center;">&nbsp; &nbsp; 房间签到/签退码为<strong><span style="color: #e03e2d;">{}</span></strong>，请准时使用。</p>
<p style="text-align: right;"><span style="text-decoration: underline;">清华大学计算机系会议室管理系统</span></p>
<p>&nbsp;</p>
</body>
</html>
'''

FAIL_EXAMINE_TEXT = '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<h2 style="text-align: left;"><strong>{}：</strong></h2>
<p style="text-align: justify;">&nbsp; &nbsp; 很遗憾！你申请在<strong><span style="color: #3598db;">{}</span></strong>使用<strong><span style="color: #3598db;">{}</span></strong>的请求没有通过审批。以下是计算机系会议室管理系统工作人员对本次申请的审批意见：</p>
<p style="text-align: center;">&nbsp; &nbsp;&nbsp;<span style="color: #2dc26b;"><span style="color: #f1c40f;">{}</span></span></p>
<p style="text-align: right;"><span style="text-decoration: underline;">清华大学计算机系会议室管理系统</span></p>
<p>&nbsp;</p>
</body>
</html>
'''

ARRIVE_LATE_NOTICE_TEXT = '''
<html>
<head>
<style>
body {{{{
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
}}}}
</style>
</head>
<body>
<h2>{{}}：</h2>
<p>&nbsp;</p>
<p style="padding-left: 40px;"><span style="font-size: 12pt;">您预约的时间为 <strong><span style="color: #e67e23;">{}</span></strong> 的 <strong><span style="color: #3598db;">{}</span></strong> 开始{}分钟内未签到，预约自动取消。</span></p>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="color: #7e8c8d;">清华大学计算机系会议室管理系统</span></p>
</body>
</html>
'''

LEAVE_LATE_NOTICE_TEXT = '''
<html>
<head>
<style>
body {{{{
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica, "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
}}}}
</style>
</head>
<body>
<h2>{{}}：</h2>
<p>&nbsp;</p>
<p style="padding-left: 40px;"><span style="font-size: 12pt;">您预约的时间为 <strong><span style="color: #e67e23;">{}</span></strong> 的 <strong><span style="color: #3598db;">{}</span></strong> 结束超过{}分钟未签离，特此通知。</span></p>
<p>&nbsp;</p>
<p style="text-align: right;"><span style="color: #7e8c8d;">清华大学计算机系会议室管理系统</span></p>
</body>
</html>
'''
