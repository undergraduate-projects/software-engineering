
import datetime
from .constant import TIME_SPAN_LENGTH


def str_time_span(time_span):
    """
    将数据库中二进制的time_span转为字符串
    """
    return bin(time_span)[2:].rjust(TIME_SPAN_LENGTH, '0')


def range_time_span(time_span):
    """
    将二进制或字符串的time_span转为[start_index, end_index)的格式
    """
    if isinstance(time_span, int):
        time_span = str_time_span(time_span)
    start_time = time_span.find('1')
    remains = time_span[start_time:]
    end_pos = remains.find('0')
    end_time = TIME_SPAN_LENGTH if end_pos < 0 else start_time + end_pos
    return start_time, end_time


def time_range_time_span(time_span):
    """
    将time_span（二进制、字符串或数字区间）中转成datetime.time区间的格式
    例：[16, 20) -> [datetime.time(8,0,0), datetime.time(10,0,0))
    """
    if isinstance(time_span, (int, str)):
        time_span = range_time_span(time_span)
    start_time = datetime.time(time_span[0] // 2, time_span[0] % 2 * 30, 0)
    end_time = datetime.time(time_span[1] // 2, time_span[1] % 2 * 30, 0)
    return start_time, end_time
