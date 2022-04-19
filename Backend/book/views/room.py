"""
会议室相关：获取会议室列表
"""

from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..models import Room, Reservation, User
from ..constant import DAY_RANGE, STUDENT_DAY_RANGE, TIME_SPAN_LENGTH
from . import views_response
from .request import get_params, GetParamsError, get_body, trans_dict
from .authentication import get_user
from .permission import permitted_reserving, permitted_admin


def gen_time_span(reservations_list, today, day_range):
    """
    用reservations_list中的预约信息生成日期在[today, today + day_range - 1]内的time_span
    如果传入预约列表，会在对应时间填1；如果传入预约列表的列表，会在对应时间填index+1
    """
    if not isinstance(reservations_list, list):
        reservations_list = [reservations_list]

    time_span = [['0'] * TIME_SPAN_LENGTH for _ in range(day_range)]
    for index, reservations in enumerate(reservations_list):
        for res in reservations:
            days = (res.date - today).days
            if days not in range(day_range):
                continue
            for time in range(TIME_SPAN_LENGTH):
                if res.time_span & 1 << (TIME_SPAN_LENGTH - 1 - time):
                    time_span[days][time] = str(index+1)

    return [''.join(i) for i in time_span]


def reserving_room_list(user, rooms):
    """
    获取预约模式下的房间信息列表
    """
    today = date.today()
    day_range = DAY_RANGE if user.is_teacher else STUDENT_DAY_RANGE
    date_range = [today, today + timedelta(days=day_range - 1)]

    reservations = Reservation.objects.filter(date__range=date_range)
    reservations_active = reservations.filter(Reservation.Q_ACTIVE)
    reservations_active_self = reservations_active.filter(applicant=user)
    reservations_waiting_self = reservations.filter(state=Reservation.WAITING, applicant=user)
    reservations_used_self = reservations.filter(Reservation.Q_USER_RESERVING, applicant=user)

    reservations_list = [reservations_active, reservations_active_self, reservations_waiting_self]

    infos = []
    for room in rooms:
        info = room.info()
        room_reservations_list = [res.filter(room=room) for res in reservations_list]
        info['time_span'] = gen_time_span(room_reservations_list, today, day_range)
        info['admin'] = permitted_admin(user, room)
        infos.append(info)

    return {
        'today': str(today),
        'day_range': day_range,
        'waiting_time_span': gen_time_span(reservations_used_self, today, day_range),
        'room_list': infos
    }


def room_list(request):
    """
    接受GET请求，返回当前用户有预约权限的房间的信息列表
    可选参数： only: only=room:1 表示只看id为1的房间
    如果输入参数reserving: True，则会以以下格式返回信息：
        today: 当前日期 string 用于前后端统一日期
        day_range: 表示当前用户能申请的天数范围
        waiting_time_span: 当前用户已申请的时间信息
        room_list: 可预约房间信息组成的列表，每个房间除了基本信息还会给出time_span和admin
                   time_span中1代表已被他人预约，2代表当前用户已预约，3代表当前用户申请中
                   admin表示当前用户是否有该房间的管理权限
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    all_rooms = Room.objects.all()

    if 'only' in request.GET:
        try:
            only_dict = trans_dict(request.GET['only'], ['id'])
            all_rooms = all_rooms.filter(**only_dict)
        except GetParamsError as error:
            return error.response
        except (TypeError, ValueError) as error:
            return views_response.bad_request(str(error))

    rooms = [room for room in all_rooms if permitted_reserving(user, room)]

    if request.GET.get('reserving') == 'True':
        return views_response.success(reserving_room_list(user, rooms))

    return views_response.success([room.info() for room in rooms])


def put_room_info(room, data):
    """
    用于room_info的PUT请求
    """
    edited_keys = []

    for key, val in data.items():
        if key in Room.EDITABLE_PARAMS:
            edited_keys.append(key)
            setattr(room, key, val)

    try:
        room.full_clean()
    except ValidationError as error:
        return views_response.bad_request('ValidationError:'+str(error))

    room.save()
    return views_response.success('Success for keys:'+str(edited_keys))


def add_room_info(data):
    """
    用于room_info的POST请求
    """
    params = {}
    for key in Room.EDITABLE_PARAMS:
        if key not in data:
            return views_response.missing_parameter(key)
        params[key] = data[key]
    room = Room(**params)
    room.terminal_token = 'new_room'

    try:
        room.full_clean()
    except ValidationError as error:
        return views_response.bad_request('ValidationError:'+str(error))

    room.save()
    room.terminal_token = 't' + str(room.id).rjust(2, '0')
    room.save()
    return views_response.success()


def room_info(request):
    """
    接受以下请求：
        GET请求: 获取房间信息，参数：
            id 房间id
    以下请求需要root权限：
        PUT请求，更改房间信息，参数：
            id 房间id
            需要更改的信息（可选项见models Room.EDITABLE_PARAMS）
        DELETE请求，删除房间，参数：
            id 房间id
        POST请求，添加房间，参数：
            房间基本信息（见models Room.EDITABLE_PARAMS）
    """
    if request.method not in ['GET', 'PUT', 'DELETE', 'POST']:
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    if request.method in ['PUT', 'DELETE', 'POST'] and user.role != User.ROOT:
        return views_response.no_permission()

    try:
        data = request.GET if request.method == 'GET' else get_body(request)
        if request.method != 'POST':
            [room_id] = get_params(data, {'id': int})
            room = Room.objects.get(id=room_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return views_response.invalid_value('id', room_id)

    if request.method == 'GET':
        return views_response.success(room.info())

    if request.method == 'PUT':
        return put_room_info(room, data)

    if request.method == 'DELETE':
        room.delete()
        return views_response.success()

    if request.method == 'POST':
        return add_room_info(data)
