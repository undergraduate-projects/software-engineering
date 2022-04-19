"""
定时检查所有预约记录，进行邮件提醒和状态变更
"""

from time import sleep
from datetime import datetime, timedelta
from .constant import START_REMIND_TIME, APPROVE_REMIND_TIME, ARRIVAL_LATENCY, LEAVE_LATENCY
from .models import Reservation
from .email.send import send_remind_start_email, send_remind_approve_email, \
                        send_arrive_late_notice_email, send_leave_late_notice_email


def whole_minutes(date_time: datetime):
    """
    将时间取整为整分钟
    """
    ret = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute)
    if date_time.second >= 30:
        ret = ret + timedelta(minutes=1)
    return ret


def time_in(start, end):
    """
    计算两个时间之间相差的分钟数
    """
    return whole_minutes(end) - whole_minutes(start)


def check_waiting(res, now):
    """
    检查处于Waiting状态的预约
    """
    # 提醒审批
    if time_in(res.submit_time, now) in APPROVE_REMIND_TIME:
        hours = time_in(res.submit_time, now).seconds // 3600
        send_remind_approve_email(res, hours)
        print('check: send_remind_approve_email for res{}, hours={}'
              .format(res.id, hours))

    # 预约申请过期
    start_time = res.datetime_range()[0]
    if now >= start_time:
        res.state = Reservation.EXPIRED
        res.save()
        print('check: res{} expired'.format(res.id))


def check_approved(res, now):
    """
    检查处于Approved状态的预约
    """
    # 开始前提醒
    start_time = res.datetime_range()[0]
    if time_in(now, start_time) in START_REMIND_TIME:
        send_remind_start_email(res)
        print('check: send_remind_start_email for res{}'.format(res.id))

    # 迟到
    if now >= start_time + ARRIVAL_LATENCY:
        res.state = Reservation.ABSENT
        res.save()
        send_arrive_late_notice_email(res)
        print('check: res{} absent'.format(res.id))


def check_using(res, now):
    """
    检查处于Using状态的预约
    """
    # 晚退
    end_time = res.datetime_range()[1]
    if now >= end_time + LEAVE_LATENCY:
        res.state = Reservation.FINISHED_LATE
        res.save()
        send_leave_late_notice_email(res)
        print('check: res{} late_finished'.format(res.id))


def solve():
    """
    检测函数，每分钟进行一次检测
    """
    last_minute = -1
    while True:
        now = datetime.now()
        now_minute = whole_minutes(now).minute
        while now_minute == last_minute:
            sleep(60 - now.second)
            now = datetime.now()
            now_minute = whole_minutes(now).minute
        last_minute = now.minute

        check_dict = {
            Reservation.WAITING: check_waiting,
            Reservation.APPROVED: check_approved,
            Reservation.USING: check_using
        }
        for res in Reservation.objects.filter(state__in=check_dict.keys()):
            check_dict[res.state](res, now)
