"""
用于从request中获取参数
"""

import json
from . import views_response
from .views_response import invalid_format, missing_parameter, type_error


class GetParamsError(Exception):
    """
    get_body和get_params错误时抛出该异常，可通过response属性获取应该返回的错误信息
    """
    def __init__(self, response):
        Exception.__init__(self)
        self.response = response


def get_body(request):
    """
    PUT或POST方法获取body，错误则返回response
    """
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError as error:
        raise GetParamsError(invalid_format()) from error

    return body


def get_params(params_dict, param_type_dict: dict) -> list:
    """
    从字典中获取指定类型的参数，例：get_params(['val': 1], {'val': int}) = [1]，错误则返回response
    需要类型为int时，若传入参数为str但能转换为int，会自动进行转换
    如果是GET方法，只能获得str或int
    """
    ret = []
    for param, param_type in param_type_dict.items():
        if param not in params_dict:
            raise GetParamsError(missing_parameter(param))
        val = params_dict[param]

        # 由于GET方法中直接获得参数都是str，特判如果是str且需要int，尝试转成int
        if isinstance(val, str) and param_type == int:
            try:
                val = int(val)
            except ValueError:
                pass

        if not isinstance(val, param_type):
            raise GetParamsError(type_error(param, param_type, type(val)))
        ret.append(val)

    return ret


def trans_dict(only, keys):
    """
    用于将筛选功能的only参数转为字典
    """
    only_dict = {}
    for param in only.split(','):
        if param == '':
            continue
        pos = param.find(':')
        if pos < 0:
            raise GetParamsError(views_response.invalid_value('only', only))
        key = param[:pos]
        value = param[pos + 1:]

        # 非法键值
        if key not in keys:
            raise GetParamsError(views_response.bad_request(
                'key `{}` in `only` is invalid'.format(key)))

        only_dict[key] = value

    return only_dict
