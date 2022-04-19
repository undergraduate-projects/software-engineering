"""
发送邮件
"""

import smtplib
from ..models import Reservation
from email.mime.text import MIMEText
from email.utils import formataddr
from book.type_trans import time_range_time_span
from book.views.permission import get_admins
from .text import PASS_EXAMINE_TEXT, FAIL_EXAMINE_TEXT, RES_REMIND_TEXT, APPROVE_REMIND_TEXT, \
                  ARRIVE_LATE_NOTICE_TEXT, LEAVE_LATE_NOTICE_TEXT
from ..constant import ARRIVAL_LATENCY, LEAVE_LATENCY

HOST = 'smtp.qq.com'
PASSWORD = 'uqlzlbcbhyjyfdgj'
SENDER = '1097186112@qq.com'


def send_email(receiver, subject, content):
    """
    发送提醒邮件
    """
    try:
        client = smtplib.SMTP_SSL(HOST, smtplib.SMTP_SSL_PORT)
        client.login(SENDER, PASSWORD)

        if not isinstance(receiver, list):
            receiver = [receiver]

        for user in receiver:
            email = user.email
            if not email:
                continue
            final_content = content.format(user.fullname + '老师' if user.is_teacher else user.fullname + '同学')
            message = MIMEText(final_content, 'html')
            message['From'] = formataddr(('THUCST', SENDER))  # 发件人
            message['Subject'] = subject  # 主题
            message['To'] = email  # 收件人
            client.sendmail(SENDER, email, message.as_string())  # 发邮件

    except Exception as ex:
        print(ex)


def send_examine_email(res: Reservation):
    """
    预约审批后通知用户
    """
    tar_user = res.applicant
    raw_date = str(res.date).split('-')
    use_date = raw_date[0] + '年' + raw_date[1].lstrip('0') + '月' + raw_date[2] + '日'
    (start_time, end_time) = time_range_time_span(res.time_span)
    time = use_date + ' ' + str(start_time) + '——' + str(end_time)
    room_name = res.room.building.name + ' ' + res.room.name

    if res.approval_result:  # 通过审批
        subject = '会议室申请成功'
        content = PASS_EXAMINE_TEXT.format('{}', time, room_name, res.token)
    else:
        subject = '会议室申请失败'
        content = FAIL_EXAMINE_TEXT.format('{}', time, room_name, res.refuse_reason)

    send_email(tar_user, subject, content)


def send_remind_start_email(res: Reservation):
    """
    提醒用户所预约时间将到
    """
    start_time, end_time = time_range_time_span(res.time_span)
    time_str = start_time.strftime('%H:%M') + ' - ' + end_time.strftime('%H:%M')
    mail_text = RES_REMIND_TEXT.format(time_str, res.room.name, res.token)

    send_email(res.applicant, '会议即将开始提醒', mail_text)


def send_remind_approve_email(res: Reservation, waited_hours):
    """
    提醒管理员进行审批
    """
    admins = get_admins(res.room)  # 有权限管理的管理员
    begin_time, end_time = time_range_time_span(res.time_span)
    time_str = (res.date.strftime(r'%Y-%m-%d') + '  ' +
                begin_time.strftime('%H:%M') + ' - ' + end_time.strftime('%H:%M'))

    applicant = res.applicant
    apllicant_info = '{}  {}  {} {}'.format(
        applicant.fullname,
        '老师' if applicant.is_teacher else '学生',
        applicant.department.name,
        applicant.institute.name if applicant.institute else ''
    )
    mail_text = APPROVE_REMIND_TEXT.format(
        waited_hours, apllicant_info, res.submit_time.strftime(r'%Y-%m-%d %H:%M'),
        time_str, res.room.name, res.apply_reason if res.apply_reason else '无')
    send_email(admins, '会议室审批提醒', mail_text)


def send_arrive_late_notice_email(res: Reservation):
    """
    通知用户已迟到
    """
    start_time, end_time = time_range_time_span(res.time_span)
    time_str = start_time.strftime('%H:%M') + ' - ' + end_time.strftime('%H:%M')
    mail_text = ARRIVE_LATE_NOTICE_TEXT.format(
        time_str, res.room.name, ARRIVAL_LATENCY.seconds/60
    )
    send_email(res.applicant, '会议室迟到通知', mail_text)


def send_leave_late_notice_email(res: Reservation):
    """
    通知用户晚退
    """
    start_time, end_time = time_range_time_span(res.time_span)
    time_str = start_time.strftime('%H:%M') + ' - ' + end_time.strftime('%H:%M')
    mail_text = LEAVE_LATE_NOTICE_TEXT.format(
        time_str, res.room.name, LEAVE_LATENCY.seconds/60
    )
    send_email(res.applicant, '会议室晚退通知', mail_text)
