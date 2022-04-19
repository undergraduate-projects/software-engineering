"""
用户相关：用户信息、用户列表、设置用户角色
"""

from datetime import datetime, timedelta
from django.db.models import Func
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..constant import USER_PER_PAGE
from ..models import User, Institute
from . import views_response
from .request import get_body, get_params, GetParamsError, trans_dict
from .info import info_page
from .authentication import get_user


def edit_user_info(user, body, editable_params):
    """
    根据body里的信息修改user，返回edited_keys（错误则返回response）
    """
    edited_keys = []

    for key, val in body.items():
        if key not in editable_params:
            continue

        edited_keys.append(key)

        # 不能修改超管，也不能把用户设置为超管
        if key == 'role' and (user.role == User.ROOT or val == User.ROOT):
            return views_response.invalid_value(key, val)

        # 封禁
        if key == 'ban_days':
            if not isinstance(val, int):  # 应为整数
                return views_response.type_error('ban_days', int, type(val))
            if val < 0:  # 应当大于等于0
                return views_response.invalid_value('ban_days', val)
            key = 'unban_time'
            val = datetime.now() + timedelta(days=val)

        setattr(user, key, val)

    return edited_keys


def put_user_info(request, user):
    """
    处理user_info的PUT请求
    """
    try:
        body = get_body(request)
    except GetParamsError as error:
        return error.response

    if 'id' in body:
        try:
            [user_id] = get_params(body, {'id': int})
        except GetParamsError as error:
            return error.response
        if user.role != User.ROOT:
            return views_response.no_permission()
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return views_response.invalid_value('id', user_id)
        editable_params = User.ROOT_EDITABLE_PARAMS
    else:
        editable_params = User.SELF_EDITABLE_PARAMS

    edited_keys = edit_user_info(user, body, editable_params)
    if not isinstance(edited_keys, list):
        return edited_keys

    try:
        user.full_clean()
    except ValidationError as error:
        return views_response.bad_request('ValidationError:'+str(error))

    user.save()
    return views_response.success('Success for keys:'+str(edited_keys))


def user_info(request):
    """
    接受GET请求，返回当前用户信息
    接受PUT请求，参数：
        用户更改自己信息：
            可选参数（不改则不传）：
                email: 邮箱，需要符合格式
                phone_number: 电话，需要符合格式
                institute_id: 研究所id
        管理员更改用户信息，需要ROOT权限：
            id: 用户id
            可选参数：
                role: 用户权限
                is_teacher: 是否有教师权限
                department_id: 院系id
                institute_id
                ban_days: 封禁天数，若为0代表取消封禁
    """
    if request.method not in ['GET', 'PUT']:
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    if request.method == 'GET':
        return views_response.success(user.info())
    if request.method == 'PUT':
        return put_user_info(request, user)


# 数据库按汉字拼音排序
# pylint: disable = W0223, C0116
class Convert(Func):
    """
    作为函数order_by的参数，用于按汉字拼音排序

    等价于SQL语句的 ORDER BY CONVERT (field_name USING gbk) ASC
    """

    def __init__(self, expression, transcoding_name, **extra):
        super().__init__(
            expression, transcoding_name=transcoding_name, **extra)

    def as_mysql(self, compiler, connection):
        self.function = 'CONVERT'
        self.template = '%(function)s(%(expressions)s USING %(transcoding_name)s)'
        return super().as_sql(compiler, connection)


def user_list_order_by(order_by):
    """
    处理user_list的order_by参数
    """
    # 处理降序
    descending = False
    if order_by and order_by[0] == '-':
        descending = True
        order_by = order_by[1:]

    if order_by == '':  # 默认按学号排序
        order_by = 'uid'

    if order_by not in User.BASIC_PARAMS and order_by not in User.OBJECT_PARAMS:
        raise GetParamsError(views_response.invalid_value('order_by', order_by))

    if order_by == 'fullname':  # 按汉语拼音排序
        order_by = Convert('fullname', 'gbk')
        order_by = order_by.desc() if descending else order_by.asc()
    elif descending:
        order_by = '-' + order_by

    return order_by


def user_list_only_dict(only_dict):
    """
    处理user_list的only参数
    """
    # 处理institute__in
    if 'institute__in' in only_dict:
        val = only_dict['institute__in']
        institute__in = []
        for id_str in val.split('|'):
            try:
                institute_id = str(id_str)
                institute__in.append(Institute.objects.get(id=institute_id))
            except (TypeError, ValueError) as error:
                raise GetParamsError(views_response.invalid_value(
                    'only.institute__in', val)) from error
            except ObjectDoesNotExist as error:
                raise GetParamsError(views_response.bad_request(
                    'Institute{} does not exist'.format(institute_id))) from error
        only_dict['institute__in'] = institute__in
    # 处理banned
    if 'banned' in only_dict:
        if only_dict['banned'] != 'true':
            raise GetParamsError(views_response.invalid_value('only.banned', only_dict['banned']))
        only_dict.pop('banned')
        only_dict['unban_time__gte'] = datetime.now()

    return only_dict


def user_list(request):
    """
    接受GET请求，用于分页获取用户列表，需要root权限，参数：
        page_num: 列表页数，不传入则不分页
        order_by: 按某种用户信息排序（可用参数同返回的用户信息中的参数），为''则默认按学号，fullname按汉语拼音排序
                  参数前加减号'-'可以按降序排序
        only: 包含参数信息的字符串（注意中间不加空格），用于只看部分用户
              例："fullname:张三,role:U" 表示只看名为张三的普通用户
              可用参数与返回的用户信息中的参数相同（除了unban_time）
              特殊参数：'role__in:AR'查看管理员列表 'institute__in:1|2|3'筛选研究所 'banned:true'被封禁用户
                      uid__contains fullname__contains 部分搜索
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    if user.role != User.ROOT:
        return views_response.no_permission()

    try:
        [order_by, only] = get_params(request.GET, {
            'order_by': str,
            'only': str
        })
        only_dict = user_list_only_dict(trans_dict(only, User.SEARCHABLE_PARAMS))
        order_by = user_list_order_by(order_by)
    except GetParamsError as error:
        return error.response

    try:
        tar_users = User.objects.filter(**only_dict).order_by(order_by)
    except (TypeError, ValueError) as error:
        return views_response.bad_request(str(error))

    if 'page_num' not in request.GET:
        return views_response.success([user.info() for user in tar_users])

    return info_page(request, tar_users, USER_PER_PAGE)


def user_reservation(request):
    """
    接受GET请求，获取当前用户的全部历史预约记录，按提交时间从新到旧排序
    返回值：
        list: 预约信息列表
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    reservations = user.applied_reservations.all().order_by('-submit_time')

    return views_response.success({'list': [res.info() for res in reservations]})


def institutes(request):
    """
    接受GET请求，获取全部研究所信息
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    if not user:
        return views_response.not_logged_in()

    return views_response.success([institute.info() for institute in Institute.objects.all()])
