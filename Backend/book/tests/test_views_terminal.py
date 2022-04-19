import mock
from datetime import date, datetime, time
from django.test import Client
from django.urls import reverse
from ..constant import GET, PUT
from ..models import Room, Building, Institute, Reservation, User
from ..views import views_response
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, ispan, type_json


class TestViewsTerminal(ViewsTestCase):
    @classmethod
    def setUpTestData(cls):
        basic_setup()
        # Room
        room = Room.objects.create(
            id=1,
            building=Building.objects.get(id=1),
            floor=1,
            name='会议室101',
            capacity=100,
            institute=Institute.objects.get(id=1),
            terminal_token='test_token'
        )
        # User
        TestUsers.setup()
        user = TestUsers.get(User.NORMAL_USER)
        # Reservation
        values_set = [
            [ispan(27, 28), True, None, 'before_arrival', None, None, Reservation.APPROVED],
            # 13:00 - 14:00
            [ispan(2, 3), True, None, 'token-1', None, datetime.now(), Reservation.CANCELED],
            # 0:30 - 1:30
            [ispan(2, 3), False, None, 'token-1', None, None, Reservation.REFUSED],
            [ispan(2, 3), True, datetime(2020, 1, 1, 0, 35), 'after_leave',
                datetime(2020, 1, 1, 1, 25), None, Reservation.FINISHED],
            [ispan(25, 26), True, datetime(2020, 1, 1, 12, 2), 'before_leave',
                None, None, Reservation.USING]
            # 12:00 - 13:00
        ]
        for values in values_set:
            Reservation.objects.create(
                date=date.today(),
                time_span=values[0],
                approval_result=values[1],
                arrival_time=values[2],
                token=values[3],
                leave_time=values[4],
                cancel_time=values[5],
                applicant=user,
                room=room,
                state=values[6]
            )

    def test_POST_login(self):
        client = Client()
        path = reverse('t_login')
        self.checkMethod(client, path, [GET, PUT])

        test_data = {
            'room_id': 1,
            'token': 'test_token'
        }

        # 正常登录
        response = client.post(path, data=test_data, content_type=type_json)
        self.assertEqual(response.status_code, 200)

        # 不是json
        response = client.post(path, data=test_data)
        self.assertResponse(response, views_response.invalid_format())

        # 缺参数
        for param in ['room_id', 'token']:
            data = test_data.copy()
            data.pop(param)
            response = client.post(path, data=data, content_type=type_json)
            self.assertResponse(response, views_response.missing_parameter(param))

        # id不是正常值
        data = test_data.copy()
        data['room_id'] = [1, 2]
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.type_error('room_id', int, list))

        data['room_id'] = 'dsfq'
        response = client.post(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.type_error('room_id', int, str))

        data['room_id'] = -1
        response = client.post(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 420)

        # 密码错误
        data = test_data.copy()
        data['token'] = 'wrong'
        response = client.post(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 420)

    def test_GET_room_info(self):
        client = Client()
        path = reverse('t_room_info')

        # 方法错误
        response = client.post(path)
        self.assertEqual(response.status_code, 405)

        # 没有cookie
        response = client.get(path)
        self.assertEqual(response.status_code, 401)
        # token错误
        client.cookies['terminal_token'] = 'wrong'
        response = client.get(path)
        self.assertEqual(response.status_code, 401)

        # 正常
        client.cookies['terminal_token'] = 'test_token'
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        keys = ['today', 'time_span']
        values = [str(date.today()), '000000000000000000000000111100000000000000000000']
        for num in range(len(keys)):
            self.assertEqual(response.json()['data'][keys[num]], values[num])

    def test_arrive(self):
        client = Client()
        path = reverse('t_arrive')
        self.checkMethod(client, path, [GET, PUT])

        test_data = {'token': 'before_arrival'}
        test_res = Reservation.objects.get(token=test_data['token'])

        # terminal_token 不对
        client.cookies['terminal_token'] = 'wrong'
        response = client.post(path, data=test_data, content_type=type_json)
        self.assertEqual(response.status_code, 401)

        # 使用正确terminal_token
        client.cookies['terminal_token'] = 'test_token'

        # json错误
        response = client.post(path, data=test_data)
        self.assertResponse(response, views_response.invalid_format())

        # 缺少参数
        for param in ['token']:
            data = test_data.copy()
            data.pop(param)
            response = client.post(path, data=data, content_type=type_json)
            self.assertResponse(response, views_response.missing_parameter(param))

        # token不对
        data = test_data.copy()
        data['token'] = 'wrong'
        response = client.post(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 420)

        # mock模拟时间进行测试
        class MockDatetime(datetime):
            mock_now = datetime.combine(date.today(), time(13, 1))

            @classmethod
            def now(cls):
                return cls.mock_now

        with mock.patch('book.views.terminal.datetime', MockDatetime):
            # 正常
            response = client.post(path, data=test_data, content_type=type_json)
            self.assertEqual(response.status_code, 200)
            res = Reservation.objects.get(token=test_data['token'])
            self.assertEqual(res.state, Reservation.USING)
            # 已签过到
            response = client.post(path, data=test_data, content_type=type_json)
            self.assertEqual(response.status_code, 212)
            res = Reservation.objects.get(token=test_data['token'])
            self.assertEqual(res.state, Reservation.USING)
            test_res.save()
            # 不在预约时间段
            MockDatetime.mock_now = datetime.combine(date.today(), time(12, 59))
            response = client.post(path, data=test_data, content_type=type_json)
            self.assertEqual(response.status_code, 210)
            res = Reservation.objects.get(token=test_data['token'])
            self.assertEqual(res.state, Reservation.APPROVED)

    def test_leave(self):
        client = Client()
        path = reverse('t_leave')
        self.checkMethod(client, path, [GET, PUT])

        test_data = {'token': 'before_leave'}
        test_res = Reservation.objects.get(token=test_data['token'])

        client.cookies['terminal_token'] = 'test_token'

        # mock模拟时间进行测试
        class MockDatetime(datetime):
            mock_now = datetime.combine(date.today(), time(12, 59))

            @classmethod
            def now(cls):
                return cls.mock_now

        with mock.patch('book.views.terminal.datetime', MockDatetime):
            # 正常
            response = client.post(path, data=test_data, content_type=type_json)
            self.assertEqual(response.status_code, 200)
            res = Reservation.objects.get(token=test_data['token'])
            self.assertEqual(res.state, Reservation.FINISHED)
            test_res.save()
            # 晚退
            MockDatetime.mock_now = datetime.combine(date.today(), time(13, 1))
            response = client.post(path, data=test_data, content_type=type_json)
            self.assertEqual(response.status_code, 211)
            res = Reservation.objects.get(token=test_data['token'])
            self.assertEqual(res.state, Reservation.FINISHED_LATE)
            test_res.save()
