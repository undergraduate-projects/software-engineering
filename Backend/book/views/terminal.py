"""
终端相关
"""

from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from ..type_trans import str_time_span
from ..models import Room, Reservation
from . import views_response
from .request import get_body, get_params, GetParamsError
from .room import gen_time_span


def login(request):
    """
    接收POST请求，用于终端登录，检查token是否正确

    接受参数
        room_id
        token

    返回状态码
        200: 成功
        420: room_id或token错误
    """

    if request.method != 'POST':
        return views_response.method_not_allowed(request.method)

    # 安全性：给出统一错误信息，减少信息透露
    fail_response = views_response.gen_response(420, 'Wrong room_id or token')

    try:
        [room_id, password] = get_params(get_body(request), {
            'room_id': int,
            'token': str
        })
        room = Room.objects.get(id=room_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return fail_response

    if room.terminal_token != password:
        return fail_response

    return views_response.success('Login success')


def get_room(request):
    """
    获得会议室对象，供下面视图函数调用，获取失败直接返回401
    """
    token = request.COOKIES.get('terminal_token')
    if not token:
        return views_response.gen_response(401, 'No token')

    room = Room.objects.filter(terminal_token=token).first()
    if not room:
        return views_response.gen_response(401, 'Wrong token')

    return room


def room_info(request):
    """
    接受GET请求，用于查看当前会议室信息

    返回值：
        房间基本信息
        today: 当前日期 string
        time_span: 当天已被预约的时间信息
    """

    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    room = get_room(request)
    if not isinstance(room, Room):
        return room

    today = date.today()
    reservations = Reservation.objects.filter(Reservation.Q_ACTIVE, room=room, date=today)
    time_span = gen_time_span(reservations, today, 1)

    info = room.info()
    info.update({
        'today': str(today),
        'time_span': time_span[0]
    })
    return views_response.success(info)


def get_sign_params(request):
    """
    获取签到签退需要的参数
    """
    room = get_room(request)
    if not isinstance(room, Room):
        return room

    try:
        [token] = get_params(get_body(request), {'token': str})
    except GetParamsError as error:
        return error.response

    # 获取预约记录
    reservations = Reservation.objects.filter(Reservation.Q_ACTIVE, room=room, token=token)
    if not reservations:
        return views_response.gen_response(420, 'Token not valid')
    if len(reservations) > 1:
        return views_response.gen_response(520, 'Database conflict: multiple identical tokens')

    sign_time = datetime.now()

    return reservations.first(), sign_time


def arrive(request):
    """
    接受POST请求，用于到达确认

    接收参数
        token: 预约审批通过后获得的token

    返回状态码
        200: 成功
        210: 不在预约时间段内
        212: 已签过到
        420: token错误

    若状态码为2开头，返回该预约01串格式的time_span
    """

    if request.method != 'POST':
        return views_response.method_not_allowed(request.method)

    params = get_sign_params(request)
    if not isinstance(params, tuple):
        return params
    reservation, arrival_time = params

    begin_time = reservation.datetime_range()[0]
    dict_timespan = {'time_span': str_time_span(reservation.time_span)}

    if reservation.state == Reservation.USING:  # 已签到
        return views_response.gen_response(212, dict_timespan)

    if arrival_time < begin_time:  # 过早签到
        return views_response.gen_response(210, dict_timespan)

    reservation.arrival_time = arrival_time
    reservation.state = Reservation.USING
    reservation.save()
    return views_response.gen_response(200, dict_timespan)


def leave(request):
    """
    接受POST请求，用于离开确认

    接受参数
        token: 预约审批通过后获得的token

    返回状态码
        200: 成功
        210: 还未签到
        211: 晚退
        420: token错误

    若状态码为2开头，返回该预约01串格式的time_span
    """

    if request.method != 'POST':
        return views_response.method_not_allowed(request.method)

    params = get_sign_params(request)
    if not isinstance(params, tuple):
        return params
    reservation, leave_time = params

    end_time = reservation.datetime_range()[1]
    dict_timespan = {'time_span': str_time_span(reservation.time_span)}

    if reservation.state != Reservation.USING:  # 未签到
        return views_response.gen_response(210, dict_timespan)

    reservation.leave_time = leave_time

    if leave_time >= end_time:  # 晚退
        reservation.state = Reservation.FINISHED_LATE
        reservation.save()
        return views_response.gen_response(211, dict_timespan)

    reservation.state = Reservation.FINISHED
    reservation.save()
    return views_response.gen_response(200, dict_timespan)
