"""
预约和审批
"""

import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from ..constant import TIME_SPAN_LENGTH, START_TIME, END_TIME, RES_PER_PAGE
from ..constant import DAY_RANGE, STUDENT_DAY_RANGE
from ..type_trans import range_time_span, time_range_time_span
from ..models import Room, Reservation
from ..email.send import send_examine_email
from . import views_response
from .request import get_body, get_params, GetParamsError, trans_dict
from .info import info_page
from .authentication import get_user
from .permission import permitted_reserving, permitted_admin, admin_rooms


def get_conflict_reservations(res: Reservation):
    """
    获取与一个预约时间冲突的等待审核的预约
    """
    check_res = res.room.reservations.filter(date=res.date, state=Reservation.WAITING)
    return [item for item in check_res if item != res and item.time_span & res.time_span]


def conflict(request):
    """
    接受GET请求，获取与一个预约时间冲突的预约信息列表，需要对应房间的管理权限，参数：
        res_id
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    try:
        [res_id] = get_params(request.GET, {'res_id': int})
        res = Reservation.objects.get(id=res_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return views_response.invalid_value('res_id', res_id)

    if not permitted_admin(user, res.room):
        return views_response.no_permission()

    data = [item.info() for item in get_conflict_reservations(res)]
    return views_response.success(data)


def time_span_valid(time_span):
    """
    检验time_span是否合法
    """
    if not (isinstance(time_span, str)) or len(time_span) != TIME_SPAN_LENGTH:
        return False
    for char in time_span:
        if char not in ['0', '1']:
            return False

    # 判断time_span中有且仅有一段连续1
    first_one = time_span.find('1')
    if first_one == -1:
        return False
    remains = time_span[first_one:]
    second_zeros = remains.find('0')
    if second_zeros >= 0 and remains[second_zeros:].find('1') >= 0:
        return False

    return True


def submit_params(request):
    """
    获取submit需要的参数
    """
    try:
        [room_id, date_str, time_span, reason] = get_params(get_body(request), {
            'room_id': int,
            'date': str,
            'time_span': str,
            'reason': str
        })
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        room = Room.objects.get(id=room_id)
    except GetParamsError as error:
        return error.response
    except ValueError:
        return views_response.invalid_value('date', date_str)
    except ObjectDoesNotExist:
        return views_response.invalid_value('room_id', room_id)

    if not time_span_valid(time_span):
        return views_response.invalid_value('time_span', time_span)
    time_span = int(time_span, 2)

    return room, date, time_span, reason


def check_datetime_valid(date, time_span, now, user, room):
    """
    检查申请时间是否合法
    """
    # 检查日期在申请范围内
    days = (date - now.date()).days
    if days < 0 or days >= DAY_RANGE:
        return views_response.bad_request('Can not reserve date {}'.format(date))
    if not user.is_teacher and days >= STUDENT_DAY_RANGE:
        return views_response.bad_request('Student can not reserve date {}'.format(date))

    # 判断预约时间在允许范围内
    start_index, end_index = range_time_span(time_span)
    if start_index < START_TIME or end_index > END_TIME:
        return views_response.bad_request('This time is too early or too late')

    # 判断不能预约之前的时间
    start_time = time_range_time_span(time_span)[0]
    if date == now.date() and start_time < now.time():
        return views_response.bad_request('Can not reserve time before now')

    # 检查不能预约已被预约的时间
    check_reservations = Reservation.objects.filter(date=date)
    for reservation in check_reservations.filter(Reservation.Q_ACTIVE, room=room):
        if reservation.time_span & time_span:
            return views_response.gen_response(431, 'This time is already reserved by someone')

    # 检查不能与自己的其他预约时间冲突
    check_q = Reservation.Q_ACTIVE | Q(state=Reservation.WAITING)
    for reservation in check_reservations.filter(check_q, applicant=user):
        if reservation.time_span & time_span:
            ret_text = 'You already reserved this time in other reservations'
            return views_response.gen_response(432, ret_text)

    return None


def submit(request):
    """
    接收POST请求，用于提交预约申请，参数：
        room_id：预约的房间id
        date: 预约日期（例：2021-04-06）
        time_span: 48位01字符串，1为要预约的时间
        reason: 最大长度为255的字符串，预约理由
    以下几种请求失败会给响应码：
        431: 所选时间已被预约
        432: 与自己的其他预约时间冲突
        433: 已被封禁
    """
    if request.method != 'POST':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    # check是否被封禁
    if user.unban_time is not None and user.unban_time > datetime.datetime.now():
        return views_response.gen_response(433, 'You have been banned.')

    params = submit_params(request)
    if not isinstance(params, tuple):
        return params
    (room, date, time_span, reason) = params

    if not permitted_reserving(user=user, room=room):
        return views_response.no_permission()

    now = datetime.datetime.now()

    check_result = check_datetime_valid(date, time_span, now, user, room)
    if check_result is not None:
        return check_result

    reservation = Reservation(
        applicant=user,
        room=room,
        date=date,
        time_span=time_span,
        apply_reason=reason,
        state=Reservation.WAITING
    )
    try:
        reservation.full_clean()
        reservation.save()
    except ValidationError:  # 理由过长
        return views_response.invalid_value('reason', reason)

    return views_response.success()


def examine_params(request):
    """
    获取examine需要的参数
    """
    try:
        [res_id, result] = get_params(get_body(request), {
            'id': int,
            'result': bool
        })
        res = Reservation.objects.get(id=res_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return views_response.invalid_value('id', res_id)

    if result:
        reason = None
    else:
        try:
            [reason] = get_params(get_body(request), {'reason': str})
        except GetParamsError as error:
            return error.response

    return res, result, reason


def examine(request):
    """
    接受PUT请求，用于管理员审批预约，参数：
        result: True/False
        reason: 字符串，拒绝理由，仅需在result为False时填写，True时为空即可
        id: 预约记录的id
    """
    if request.method != 'PUT':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    params = examine_params(request)
    if not isinstance(params, tuple):
        return params
    (res, result, reason) = params

    if not permitted_admin(user, res.room):
        return views_response.no_permission()

    try:
        if result:
            res.approve(user)
            for refuse_res in get_conflict_reservations(res):
                refuse_res.refuse(user, '与他人预约时间冲突')
                send_examine_email(refuse_res)
        else:
            res.refuse(user, reason)
    except Reservation.StateError:
        return views_response.bad_request('The reservation is not waiting for examining')
    except ValidationError:  # reason过长
        return views_response.invalid_value('reason', reason)

    send_examine_email(res)

    return views_response.success()


def cancel(request):
    """
    接收PUT请求，用于取消预约，参数：
        id: 预约记录的id
    """
    if request.method != 'PUT':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    try:
        [res_id] = get_params(get_body(request), {'id': int})
        res = Reservation.objects.get(id=res_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return views_response.invalid_value('id', res_id)

    if res.applicant != user:
        return views_response.no_permission()

    if res.state == Reservation.CANCELED:
        return views_response.bad_request('Duplicated cancelling operation')

    if res.state not in Reservation.CANCELABLE_STATES:
        return views_response.bad_request('This reservation can not be canceled')

    res.cancel_time = datetime.datetime.now()
    res.state = Reservation.CANCELED
    res.save()

    return views_response.success()


def reservation_list(request):
    """
    接受GET请求，用于管理员分页获取预约信息列表，默认返回当前用户拥有管理权的所有房间的所有预约信息，按提交时间从新到旧排序

    参数：
        page_num: 列表页数
        only: 格式同user_list，可选参数：
            state, state__in: 预约状态（见models）
            applicant：申请人id
            room: 房间id，需要该房间的管理权限
            examined:true 是否被审批过
    可选参数：
        order_by: submit_time / -submit_time / approval_time / -approval_time
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()
    reservations = Reservation.objects.filter(room__in=admin_rooms(user))

    try:
        [only] = get_params(request.GET, {'only': str})
        only_dict = trans_dict(only, Reservation.SEARCHABLE_PARAMS)
    except GetParamsError as error:
        return error.response

    order_by = '-submit_time'

    if 'order_by' in request.GET:
        order_by = request.GET['order_by']
        if order_by not in ['submit_time', '-submit_time', 'approval_time', '-approval_time']:
            return views_response.invalid_value('order_by', order_by)

    if 'examined' in only_dict:
        if only_dict['examined'] != 'true':
            return views_response.invalid_value('only.examined', only_dict['examined'])
        only_dict.pop('examined')
        only_dict['approval_time__isnull'] = False

    try:
        res = reservations.filter(**only_dict).order_by(order_by)
    except (TypeError, ValueError) as error:
        return views_response.bad_request(str(error))

    return info_page(request, res, RES_PER_PAGE)
