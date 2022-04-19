"""
生成HTTP请求返回值
"""

from django.http import JsonResponse


def gen_response(code: int, data):
    """
    生成通用返回值
    """
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def success(data: object = 'Success'):
    """
    请求成功，返回data
    """
    return gen_response(200, data)


def not_logged_in():
    """
    登录过期或未登录
    """
    return gen_response(401, 'Login timeout or not logged in')


def method_not_allowed(method):
    """
    请求的方法不被允许
    参数：request.method
    """
    return gen_response(405, 'Method {} not allowed'.format(method))


def bad_request(info):
    """
    请求的格式或参数错误
    """
    return gen_response(400, info)


def invalid_format():
    """
    请求的格式错误
    """
    return bad_request('Invalid format')


def missing_parameter(param):
    """
    缺少参数
    """
    return bad_request('Missing required parameter `{}`'.format(param))


def type_error(param, expected_type, param_type):
    """
    参数类型错误
    """
    return bad_request('Parameter `{}` expected type `{}` but found `{}`'
                       .format(param, expected_type, param_type))


def invalid_value(param='', value=''):
    """
    输入的参数不合法
    """
    text = 'Invalid value'
    if param != '':
        text += ' for parameter `{}`: {}'.format(param, value)
    return bad_request(text)


def login_response(data):
    """
    为不改动已有接口，登录请求的返回值特殊处理
    """
    return JsonResponse(data, status=200)


def no_permission():
    """
    该用户无权访问
    """
    return gen_response(403, "No permission")
