"""
共用信息接口
"""
from django.core.paginator import Paginator, EmptyPage
from . import views_response
from .request import get_params, GetParamsError


def info_page(request, objects, per_page, info_func=None):
    """
    从GET请求的request中获取page_num参数，对objects进行分页并返回page_num页的信息
    如果传入info_func则信息为info_func(object)，否则为object.info()

    返回格式：
        total: 总数
        page_count: 总页数
        list: 对应页的信息列表
    """
    try:
        [page_num] = get_params(request.GET, {'page_num': int})
        pages = Paginator(objects, per_page)
        page = pages.page(page_num)
    except GetParamsError as error:
        return error.response
    except EmptyPage:
        return views_response.invalid_value('page_num', page_num)

    return views_response.success({
        'total': pages.count,
        'page_count': pages.num_pages,
        'list': [info_func(obj) if info_func else obj.info() for obj in page.object_list]
    })
