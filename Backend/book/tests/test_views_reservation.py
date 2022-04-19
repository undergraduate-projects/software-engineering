import datetime
from django.test import Client
from django.urls import reverse
from django.db.models import Q
from book.models import User, Room, Reservation
from book.views import views_response
from datetime import date
from ..constant import STUDENT_DAY_RANGE, GET, PUT, POST
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, room_setup, reservation_setup, span, type_json


class TestViewsReservation(ViewsTestCase):

    @classmethod
    def setUpTestData(cls):
        basic_setup()
        TestUsers.setup()
        room_setup()
        reservation_setup()

    def test_GET_conflict(self):
        client = Client()
        path = reverse('r_conflict')
        self.checkMethod(client, path, [PUT, POST])

        # 验证未登录
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 缺参数
        TestUsers.use(client, User.ROOT)
        response = client.get(path)
        self.assertResponse(response, views_response.missing_parameter('res_id'))

        # 参数错误
        response = client.get(path, {'res_id': -1})
        self.assertResponse(response, views_response.invalid_value('res_id', -1))

        # 无权限
        TestUsers.use(client, User.NORMAL_USER)
        response = client.get(path, {'res_id': 4})
        self.assertResponse(response, views_response.no_permission())

        # 正常获取
        TestUsers.use(client, User.ROOT)
        response = client.get(path, {'res_id': 4})
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 5)

    def test_POST_submit(self):
        client = Client()
        path = reverse('r_submit')
        self.checkMethod(client, path, ['GET', 'PUT'])

        # 验证未登录
        response = client.post(path)
        self.assertResponse(response, views_response.not_logged_in())

        TestUsers.use(client, 'U')
        test_data = {
            'room_id': Room.objects.all().first().id,
            'date': str(date.today()+datetime.timedelta(days=1)),
            'time_span': span(21, 23),
            'reason': 'meeting'
        }

        # 验证json解析失败报错
        response = client.post(path, data=test_data)
        self.assertResponse(response, views_response.invalid_format())

        # 验证缺少参数报错
        for param in ['room_id', 'date', 'time_span', 'reason']:
            data = test_data.copy()
            data.pop(param)
            response = client.post(path, data=data, content_type=type_json)
            self.assertResponse(response, views_response.missing_parameter(param))

        # 验证room_id错误时报错
        data = test_data.copy()
        data['room_id'] = 'A'
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.type_error('room_id', int, str))

        # 验证date错误时报错
        data = test_data.copy()
        data['date'] = '20210408'
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('date', '20210408'))

        # 验证不存在对应room_id的房间时报错
        data = test_data.copy()
        data['room_id'] = -1
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('room_id', -1))

        # 验证预约不允许学生预约的房间时报错
        data = test_data.copy()
        data['room_id'] = Room.objects.filter(teacher_only=True).first().id
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 验证预约非法时间报错
        data = test_data.copy()
        data['date'] = str(date.today() + datetime.timedelta(days=-1))
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.bad_request(
            'Can not reserve date {}'.format(data['date'])))

        # 验证学生预约时间限制
        data = test_data.copy()
        data['date'] = str(date.today() + datetime.timedelta(days=STUDENT_DAY_RANGE))
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.bad_request(
            'Student can not reserve date {}'.format(data['date'])))

        # 验证time_span非法时报错
        data = test_data.copy()
        data['time_span'] = '001100'
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('time_span', data['time_span']))

        data['time_span'] = '0'*10+'1'*10+'2'*28
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('time_span', data['time_span']))

        data['time_span'] = '0'*48
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('time_span', data['time_span']))

        data['time_span'] = '00110011'+'0'*40
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('time_span', data['time_span']))

        # 验证预约已被预约的时间时报错
        data = test_data.copy()
        data['time_span'] = span(20, 23)
        response = client.post(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 431)

        # 验证理由过长时报错
        data = test_data.copy()
        data['reason'] = '?'*1000
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('reason', data['reason']))

        # 验证申请成功
        count = Reservation.objects.count()
        response = client.post(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.success())
        self.assertEqual(Reservation.objects.count(), count+1)
    
    def test_examine(self):
        client = Client()
        path = reverse('r_examine')
        self.checkMethod(client, path, [GET, POST])

        # 验证未登录
        response = client.put(path)
        self.assertResponse(response, views_response.not_logged_in())

        test_data = {
            'result': False,
            'id': 1,
            'reason': ''
        }

        TestUsers.use(client, 'R')
        # 验证json解析失败报错
        response = client.put(path, data=test_data)
        self.assertResponse(response, views_response.invalid_format())

        # 参数不合法
        response = client.put(path, data={
            'result': True,
            'reason': ''
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('id'))
        response = client.put(path, data={
            'result': True,
            'reason': '',
            'id': 'invalid'
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('id', int, str))
        response = client.put(path, data={
            'result': True,
            'reason': '',
            'id': -1
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('id', '-1'))

        response = client.put(path, data={
            'id': 4,
            'reason': ''
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('result'))
        response = client.put(path, data={
            'id': 4,
            'result': 'invalid',
            'reason': ''
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('result', bool, str))

        response = client.put(path, data={
            'result': False,
            'id': 4
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('reason'))
        response = client.put(path, data={
            'result': False,
            'id': 4,
            'reason': 1
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('reason', str, int))

        # 验证无权
        TestUsers.use(client, 'U')
        response = client.put(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 不是待审核的
        TestUsers.use(client, User.ROOT)
        response = client.put(path, data={
            'result': True,
            'id': 2,
            'reason': ''
        }, content_type=type_json)
        self.assertEqual(response.status_code, 400)

        # 审核通过
        res4_bak = Reservation.objects.get(id=4)
        res5_bak = Reservation.objects.get(id=5)
        response = client.put(path, data={
            'result': True,
            'id': 4,
            'reason': ''
        }, content_type=type_json)
        self.assertResponse(response, views_response.success())
        self.assertEqual(Reservation.objects.get(id=4).state, Reservation.APPROVED)
        self.assertEqual(Reservation.objects.get(id=5).state, Reservation.REFUSED)  # 冲突申请被拒绝
        res4_bak.save()  # 复原res
        res5_bak.save()

        # 审核拒绝
        res = Reservation.objects.get(id=4)
        response = client.put(path, data={
            'result': False,
            'id': 4,
            'reason': ''
        }, content_type=type_json)
        self.assertResponse(response, views_response.success())
        res.save()  # 复原res

        # 审核拒绝原因过长
        response = client.put(path, data={
            'result': False,
            'id': 4,
            'reason': 'w'*260
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('reason', 'w'*260))
    
    def test_cancel(self):
        client = Client()
        path = reverse('r_cancel')
        self.checkMethod(client, path, ['GET', 'POST'])

        # 验证未登录
        response = client.put(path)
        self.assertResponse(response, views_response.not_logged_in())

        TestUsers.use(client, 'U')

        # json不合法
        response = client.put(path, data={'id': 4})
        self.assertResponse(response, views_response.invalid_format())

        # 没有参数
        response = client.put(path, data={}, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('id'))

        # id不合法
        response = client.put(path, data={'id': 'invalid'}, content_type=type_json)
        self.assertResponse(response, views_response.type_error('id', int, str))
        response = client.put(path, data={'id': 9}, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('id', 9))

        # 不是自己
        TestUsers.use(client, User.ADMIN)
        response = client.put(path, data={'id': 4}, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 成功取消
        TestUsers.use(client, 'U')
        response = client.put(path, data={'id': 4}, content_type=type_json)
        self.assertResponse(response, views_response.success())

        # 已经取消
        response = client.put(path, data={'id': 4}, content_type=type_json)
        self.assertEqual(response.status_code, 400)

        # 不能被取消
        res = Reservation.objects.get(id=4)
        res.state = Reservation.FINISHED
        res.save()

        response = client.put(path, data={'id': 4}, content_type=type_json)
        self.assertEqual(response.status_code, 400)

        res = Reservation.objects.get(id=4)
        res.state = Reservation.WAITING
        res.save()

    def test_list(self):
        client = Client()
        path = reverse('r_list')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证未登录
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        TestUsers.use(client, 'R')

        test_data = {
            'page_num': 1,
            'only': ''
        }

        # 测试正常获取预约信息
        response = client.get(path, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], Reservation.objects.count())

        # 测试只看某个房间
        room = Room.objects.all()[0]
        data = test_data.copy()
        data['only'] = 'room:{}'.format(room.id)
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], Reservation.objects.filter(room=room).count())

        # 测试只看等待审批
        data = test_data.copy()
        data['only'] = 'state:W'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], Reservation.objects.filter(state=Reservation.WAITING).count())

        # 测试排序功能
        data = test_data.copy()
        data['order_by'] = '-approval_time'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        # 非法参数
        data = test_data.copy()
        data['order_by'] = 'id'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('order_by', 'id'))

        # 测试只看审批过的记录
        data = test_data.copy()
        data['only'] = 'examined:true'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], Reservation.objects.filter(approval_time__isnull=False).count())
        # 非法参数
        data['only'] = 'examined:1'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('only.examined', 1))
