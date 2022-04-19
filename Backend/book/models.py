"""
Databases Models
"""

import datetime
import string
import random
import re
from django.db import models
from django.core.exceptions import ValidationError
from .constant import email_re, phone_re
from .type_trans import str_time_span, time_range_time_span


class Department(models.Model):
    """
    院系
    """
    name = models.CharField(max_length=32, unique=True)

    def info(self):
        return {'id': self.id, 'name': self.name}


class Institute(models.Model):
    """
    计算机系研究所
    """
    name = models.CharField(max_length=32, unique=True)

    def info(self):
        return {'id': self.id, 'name': self.name}


class User(models.Model):
    """
    所有用户，包括普通用户、管理员
    """
    uid = models.CharField(max_length=16, unique=True)  # 学号工号
    username = models.CharField(max_length=32, unique=True)  # 用户名
    fullname = models.CharField(max_length=32)  # 全名
    is_teacher = models.BooleanField(default=False)  # 是否有教师权限
    email = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)

    department = models.ForeignKey(Department, blank=True, null=True,
                                   on_delete=models.SET_NULL)  # 所属院系
    institute = models.ForeignKey(Institute, blank=True, null=True,
                                  on_delete=models.SET_NULL)  # 若为计算机系，所属研究所

    NORMAL_USER = 'U'
    ADMIN = 'A'
    ROOT = 'R'
    ROLES = [NORMAL_USER, ADMIN, ROOT]
    role = models.CharField(max_length=1, choices=(
        (NORMAL_USER, '普通用户'),
        (ADMIN, '管理员'),
        (ROOT, '超级管理员'),
    ))  # 用户权限

    token = models.CharField(max_length=32, unique=True)  # 登录验证token
    token_expire_time = models.DateTimeField()  # token过期时间

    unban_time = models.DateTimeField(blank=True, null=True)  # 解除封禁时间，null或早于当前时间为未封禁

    BASIC_PARAMS = ['uid', 'username', 'fullname', 'is_teacher',
                    'email', 'phone_number', 'role']
    OBJECT_PARAMS = ['department', 'institute']
    OBJECT_ID_PARAMS = [param + '_id' for param in OBJECT_PARAMS]
    SEARCHABLE_PARAMS = BASIC_PARAMS + OBJECT_PARAMS + OBJECT_ID_PARAMS + \
                        ['role__in', 'institute__in', 'banned'] + \
                        ['uid__contains', 'fullname__contains']
    SELF_EDITABLE_PARAMS = ['email', 'phone_number', 'institute_id']
    ROOT_EDITABLE_PARAMS = ['role', 'is_teacher', 'department_id', 'institute_id', 'ban_days']

    def simple_info(self):
        return {'id': self.id, 'fullname': self.fullname}

    def info(self):
        info = {'id': self.id}
        for key in User.BASIC_PARAMS:
            info[key] = getattr(self, key)
        for key in User.OBJECT_PARAMS:
            info[key] = getattr(self, key).info() if getattr(self, key) else None
        info['unban_time'] = None if self.unban_time is None else datetime.datetime.timestamp(self.unban_time) * 1000
        return info

    def full_clean(self, exclude=None, validate_unique=True):
        models.Model.full_clean(self, exclude, validate_unique)
        if self.email and not re.match(email_re, self.email):
            raise ValidationError('Email invalid')
        if self.phone_number and not re.match(phone_re, self.phone_number):
            raise ValidationError('Phone number invalid')


class Building(models.Model):
    """
    教学楼、系馆等建筑，用于 Room 表
    """
    name = models.CharField(max_length=32, unique=True)

    def info(self):
        return {'id': self.id, 'name': self.name}


class Room(models.Model):
    """
    会议室房间
    """
    name = models.CharField(max_length=32, unique=True)

    LARGE_SIZE = 'L'
    MEDIUM_SIZE = 'M'
    SMALL_SIZE = 'S'
    size = models.CharField(max_length=1, choices=(
        (LARGE_SIZE, '大型'),
        (MEDIUM_SIZE, '中型'),
        (SMALL_SIZE, '小型')
    ))
    capacity = models.IntegerField()  # 容纳人数

    building = models.ForeignKey(Building, on_delete=models.PROTECT)  # 楼
    floor = models.IntegerField()  # 楼层
    institute = models.ForeignKey(Institute, blank=True, null=True,
                                  on_delete=models.PROTECT)  # 归属的研究所，系属则为NULL

    teacher_only = models.BooleanField(default=False)
    cs_only = models.BooleanField(default=False)

    has_screen = models.BooleanField(default=False)
    has_projector = models.BooleanField(default=False)
    has_mic = models.BooleanField(default=False)
    note = models.CharField(max_length=256, blank=True, default='')  # 备注信息

    terminal_token = models.CharField(max_length=32, unique=True)  # 终端登录的密码

    BASIC_PARAMS = ['name', 'size', 'capacity', 'floor', 'teacher_only', 'cs_only',
                    'has_screen', 'has_projector', 'has_mic', 'note']
    OBJECT_PARAMS = ['building', 'institute']
    OBJECT_ID_PARAMS = [param + '_id' for param in OBJECT_PARAMS]
    EDITABLE_PARAMS = BASIC_PARAMS + OBJECT_ID_PARAMS

    def simple_info(self):
        return {'id': self.id, 'name': self.name}

    def info(self):
        info = {'id': self.id}
        for key in Room.BASIC_PARAMS:
            info[key] = getattr(self, key)
        for key in Room.OBJECT_PARAMS:
            info[key] = getattr(self, key).info() if getattr(self, key) else None
        return info


class RoomGroup(models.Model):
    """
    用于设置管理权限的房间组
    """
    name = models.CharField(max_length=32, unique=True)
    rooms = models.ManyToManyField(Room)
    admins = models.ManyToManyField(User)  # 拥有该房间组管理权限的用户列表


class Reservation(models.Model):
    """
    预约记录
    """
    applicant = models.ForeignKey(User, related_name='applied_reservations',
                                  on_delete=models.CASCADE)  # 申请人
    room = models.ForeignKey(Room, related_name='reservations',
                             on_delete=models.CASCADE)  # 申请的房间
    date = models.DateField()  # 申请日期

    time_span = models.BigIntegerField()  # 申请时间段 48-bit 二进制 从高到低
    apply_reason = models.CharField(max_length=256, blank=True, null=True)  # 申请理由
    submit_time = models.DateTimeField(auto_now_add=True)  # 提交申请的时间

    approval_result = models.BooleanField(blank=True, null=True)  # 审核结果
    approval_person = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT,
                                        related_name='approved_reservations')  # 审核人
    refuse_reason = models.CharField(max_length=256, blank=True, null=True)  # 拒绝申请的理由
    approval_time = models.DateTimeField(blank=True, null=True)  # 管理员审核的时间

    token = models.CharField(max_length=16, blank=True, null=True)  # 确认token
    arrival_time = models.DateTimeField(blank=True, null=True)  # 到达确认时间
    leave_time = models.DateTimeField(blank=True, null=True)  # 离开时间

    cancel_time = models.DateTimeField(blank=True, null=True)  # 取消时间

    WAITING = 'W'
    APPROVED = 'A'
    REFUSED = 'R'
    CANCELED = 'C'
    EXPIRED = 'E'
    USING = 'U'
    FINISHED = 'F'
    FINISHED_LATE = 'L'
    ABSENT = 'B'
    ACTIVE_STATES = [APPROVED, USING]
    CANCELABLE_STATES = [WAITING, APPROVED]
    state = models.CharField(max_length=1, choices=(
        (WAITING, '等待审批'),
        (APPROVED, '审批通过'),
        (REFUSED, '已被拒绝'),
        (CANCELED, '已撤销'),
        (EXPIRED, '已过期'),
        (USING, '正在使用'),  # 正常签到后正在使用会议室的状态
        (FINISHED, '已完成'),
        (FINISHED_LATE, '已完成（晚退）'),
        (ABSENT, '签到超时')  # 过了使用时间仍未签到
    ))
    Q_ACTIVE = models.Q(state__in=ACTIVE_STATES)
    Q_USER_RESERVING = models.Q(state__in=ACTIVE_STATES + [WAITING])

    BASIC_PARAMS = ['date', 'apply_reason', 'submit_time',
                    'approval_result', 'refuse_reason', 'approval_time',
                    'token', 'arrival_time', 'leave_time', 'cancel_time']
    OBJECT_PARAMS = ['applicant', 'room']
    SEARCHABLE_PARAMS = ['state', 'state__in'] + OBJECT_PARAMS + ['examined']

    def info(self):
        info = {'id': self.id}
        for key in Reservation.BASIC_PARAMS:
            info[key] = getattr(self, key)
        for key in Reservation.OBJECT_PARAMS:
            info[key] = getattr(self, key).info()
        info['time_span'] = str_time_span(self.time_span)
        info['approval_person'] = \
            self.approval_person.fullname if self.approval_person else '暂未审批'
        info['state'] = self.get_state_display()
        return info

    def datetime_range(self):
        (start_time, end_time) = time_range_time_span(self.time_span)
        start_time = datetime.datetime.combine(self.date, start_time)
        end_time = datetime.datetime.combine(self.date, end_time)
        return start_time, end_time

    def __new_terminal_token(self):
        """
        生成用于终端验证的不冲突的随机token
        """
        while True:
            str_from = string.digits
            length = 6
            token = ''
            for _ in range(length):
                token += random.choice(str_from)
            if not Reservation.objects.filter(Reservation.Q_ACTIVE, room=self.room, token=token):
                break

        return token

    class StateError(Exception):
        def __init__(self):
            Exception.__init__(self)

    def approve(self, approval_person):
        """
        通过预约请求
        """
        if self.state != Reservation.WAITING:
            raise Reservation.StateError
        self.approval_result = True
        self.approval_person = approval_person
        self.approval_time = datetime.datetime.now()
        self.token = self.__new_terminal_token()
        self.state = Reservation.APPROVED
        self.save()

    def refuse(self, approval_person, reason):
        """
        拒绝预约请求
        """
        if self.state != Reservation.WAITING:
            raise Reservation.StateError
        self.approval_result = False
        self.approval_person = approval_person
        self.refuse_reason = reason
        self.approval_time = datetime.datetime.now()
        self.full_clean()
        self.state = Reservation.REFUSED
        self.save()
