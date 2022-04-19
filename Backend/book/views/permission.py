"""
预约、管理权限
"""

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..constant import CS_NAMES
from ..models import User, Room, RoomGroup
from . import views_response
from .request import get_body, get_params, GetParamsError
from .authentication import get_user


def permitted_admin(user: User, room: Room):
    """
    判断user是否有room的管理权限
    """
    if user.role == User.ROOT:
        return True
    if user.roomgroup_set.filter(rooms=room):
        return True

    return False


def permitted_reserving(user, room):
    """
    判断user是否有权限预约room
    """
    if permitted_admin(user, room):
        return True

    if room.teacher_only and not user.is_teacher:
        return False

    if room.cs_only and (not user.department or user.department.name not in CS_NAMES):
        return False

    return True


def get_admins(room):
    """
    获取拥有房间管理权限的用户列表
    """
    return [user for user in User.objects.all() if permitted_admin(user, room)]


def admin_rooms(user):
    """
    获取用户能管理的房间列表
    """
    return [room for room in Room.objects.all() if permitted_admin(user, room)]


def get_room_groups():
    """
    获取房间组列表
    返回：[{
            id: 组id
            name:
            rooms: [{id, name}]
            admins: [{id, fullname}]
        }]
    """
    res = [
        {
            'id': group.id,
            'name': group.name,
            'rooms': [room.simple_info() for room in group.rooms.all()],
            'admins': [user.simple_info() for user in group.admins.all()]
        }
        for group in RoomGroup.objects.all()
    ]
    return views_response.success(res)


def new_room_group(request):
    """
    创建一个空房间组
    参数：
        name: 组名
    返回：
        id: 新创建组的id
    """
    try:
        [name] = get_params(get_body(request), {'name': str})
    except GetParamsError as error:
        return error.response

    if RoomGroup.objects.filter(name=name):
        return views_response.gen_response(410, 'name already exists')
    group = RoomGroup(name=name)
    try:
        group.full_clean()
        group.save()
    except ValidationError:
        return views_response.invalid_value('name', name)
    return views_response.success({'id': group.id})


def set_admin_groups(body):
    """
    对管理员设置管理的房间组
    """
    try:
        [admin_id, group_ids] = get_params(body, {
            'admin_id': int,
            'groups': list
        })
        admin = User.objects.get(id=admin_id)
    except GetParamsError as error:
        return error.response
    except ObjectDoesNotExist:
        return views_response.invalid_value('admin_id', admin_id)
    if admin.role == User.NORMAL_USER:
        return views_response.bad_request('User{} is not admin'.format(admin.id))

    try:
        groups = [RoomGroup.objects.get(id=i) for i in group_ids]
    except (TypeError, ValueError):
        return views_response.invalid_value('groups', 'group id not valid')
    except ObjectDoesNotExist:
        return views_response.invalid_value('groups', 'group id not found')

    for group in RoomGroup.objects.all():
        if group in groups:
            group.admins.add(admin)
        else:
            group.admins.remove(admin)

    return views_response.success()


def modify_room_group(request):
    """
    修改房间组信息  name, rooms, admins均为要修改成的值
    参数：
        group_id: 要修改的组的id
        name: 房间组name
        rooms: [ Room.id ]
        admins: [ User.id ]
    对管理员设置房间组：
        admin_id: 管理员id
        groups: [ 房间组id ]
    """
    # 获取body参数
    try:
        body = get_body(request)
    except GetParamsError as error:
        return error.response

    # 对管理员设置的情况
    if 'admin_id' in body:
        return set_admin_groups(body)

    # 一般情况参数
    try:
        [group_id, name, room_ids, admin_ids] = get_params(body, {
            'group_id': int,
            'name': str,
            'rooms': list,
            'admins': list
        })
    except GetParamsError as error:
        return error.response
    # 获取Room对象
    try:
        rooms = [Room.objects.get(id=i) for i in room_ids]
    except (TypeError, ValueError):
        return views_response.invalid_value('rooms', 'room id not valid')
    except ObjectDoesNotExist:
        return views_response.invalid_value('rooms', 'room id not found')
    # 获取User对象
    try:
        admins = [User.objects.get(id=i) for i in admin_ids]
    except (TypeError, ValueError):
        return views_response.invalid_value('admins', 'admin id not valid')
    except ObjectDoesNotExist:
        return views_response.invalid_value('admins', 'admin id not found')
    for user in admins:
        if user.role == User.NORMAL_USER:
            return views_response.bad_request('User{} is not admin.'.format(user.id))
    # 获取group对象
    try:
        group = RoomGroup.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return views_response.invalid_value('group_id', 'group id not found')
    # 更新房间和管理员
    group.rooms.clear()
    group.rooms.add(*rooms)
    group.admins.clear()
    group.admins.add(*admins)
    # 更新name
    try:
        group.name = name
        group.full_clean()
        group.save()
    except ValidationError:
        return views_response.invalid_value('name', name)
    return views_response.success()


def delete_room_group(request):
    """
    删除房间组
    参数：
        id: 房间组id
    """
    try:
        [group_id] = get_params(get_body(request), {'id': int})
    except GetParamsError as error:
        return error.response
    try:
        group = RoomGroup.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return views_response.invalid_value('id', 'group id {} not found'.format(group_id))
    group.delete()
    return views_response.success()


def room_group(request):
    """
    接受以下请求（均需root权限）
    GET 获取房间组信息
    POST 创建空房间组
    PUT 修改房间组
    DELETE 删除房间组
    """
    user = get_user(request)
    if not user:
        return views_response.not_logged_in()
    if user.role != User.ROOT:
        return views_response.no_permission()

    if request.method == 'GET':
        return get_room_groups()
    if request.method == 'POST':
        return new_room_group(request)
    if request.method == 'PUT':
        return modify_room_group(request)
    if request.method == 'DELETE':
        return delete_room_group(request)

    return views_response.method_not_allowed(request.method)
