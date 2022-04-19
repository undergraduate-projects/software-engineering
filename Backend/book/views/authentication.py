"""
认证相关：登入，登出，token
"""

import datetime
import random
import string
import requests
from requests.exceptions import RequestException
from django.core.exceptions import ValidationError
from ..constant import token_expire_timedelta, CS_NAMES
from ..models import User, Department
from . import views_response
from .request import get_body, get_params, GetParamsError


def get_user(request) -> User:
    """
    用cookie中的token检查用户是否登录，是则返回models.User并更新token有效时间，否则返回None
    """
    if 'api_token' in request.COOKIES:
        token = request.COOKIES['api_token']
        user = User.objects.filter(token=token).first()
        if user and datetime.datetime.now() < user.token_expire_time:
            user.token_expire_time = datetime.datetime.now() + token_expire_timedelta
            user.save()
            return user
        else:
            return None
    else:
        return None


def check_token(request):
    """
    接受GET请求，返回'True'或'False'表示用户是否有效登录
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    if not get_user(request):
        return views_response.success('False')
    else:
        return views_response.success('True')


def new_token():
    """
    生成未在数据库中出现的随机token
    """
    while True:
        str_from = string.ascii_letters + string.digits
        length = 20
        token = ''
        for _ in range(length):
            token += random.choice(str_from)
        if not User.objects.filter(token=token):
            break

    return token


def get_access_token(auth_code, redirect_uri):
    """
    用通过OAuth验证获得的参数向验证服务器请求access_token
    """
    params = {
        "grant_type": "authorization_code",
        "client_id": "N5SC-Ys13UYQ0hpEVP75L3p6VTg",
        "client_secret": "k85VIylTi6vYmPLfSK7Z",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }
    access_url = "https://stu.cs.tsinghua.edu.cn/api/v2/access_token"
    try:
        response = requests.post(access_url, data=params)
    except RequestException:
        return None
    res = response.json()
    # 格式为{
    # 'access_token': 'g3xcl774cv',
    # 'refresh_token': '0nhd247u290n',
    # 'expires_in': 2591999
    # }
    return res.get('access_token')


def login(request):
    """
    接受POST请求，参数：
        auth_code: 通过OAuth验证获得的auth_code
        path: redirect_uri
    返回格式：JsonResponse({'result': '', 'api_token': ''}, status=200)
        result: 'success'/'fail'
        api_token: 成功登录则返回该token，用于验证登录
        若失败还会返回error: 表示错误信息
    """

    if request.method != 'POST':
        return views_response.method_not_allowed(request.method)

    try:
        [auth_code, redirect_uri] = get_params(get_body(request), {
            'auth_code': object,
            'path': object
        })
    except GetParamsError as error:
        return error.response

    feedback = {'result': 'fail', 'api_token': ''}

    access_token = get_access_token(auth_code, redirect_uri)
    if access_token is None:
        feedback['error'] = 'failed in getting access_token'
        return views_response.login_response(feedback)

    # 向酒井请求用户信息
    params = {'access_token': access_token}
    access_url = "https://stu.cs.tsinghua.edu.cn/api/user/user_info"
    try:
        response = requests.get(access_url, params)
    except RequestException:
        feedback['error'] = 'failed in getting user_info'
        return views_response.login_response(feedback)
    res = response.json()['user']
    uid = res['student_id']

    token = new_token()
    token_expire_time = datetime.datetime.now() + token_expire_timedelta
    user = User.objects.filter(uid=uid).first()
    if not user:
        cs_department = Department.objects.filter(name__in=CS_NAMES).first()
        if not cs_department:
            feedback['error'] = 'Database error: Department of CS not found'
            return views_response.login_response(feedback)

        user = User(uid=uid,
                    username=res['name'],
                    fullname=res['fullname'],
                    email=res['email'],
                    phone_number=res['mobile'],
                    department=cs_department,  # 酒井登录默认为计算机系
                    role=User.NORMAL_USER,
                    token=token,
                    token_expire_time=token_expire_time)
    else:
        user.token = token
        user.token_expire_time = token_expire_time
    try:
        user.full_clean()
        user.save()
    except ValidationError:
        feedback['error'] = 'Save user error'
        return views_response.login_response(feedback)

    feedback['result'] = 'success'
    feedback['api_token'] = token
    return views_response.login_response(feedback)


def logout(request):
    """
    接受GET请求，退出登录
    """
    if request.method != 'GET':
        return views_response.method_not_allowed(request.method)

    user = get_user(request)
    # 有可能是登录过期，故未登录时登出也认为登出成功，给出另外的提示说明
    if not user:
        return views_response.success('Login timeout or not logged in')

    user.token_expire_time = datetime.datetime.now()
    user.save()

    return views_response.success('Logout OK')
