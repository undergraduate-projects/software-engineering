from django.test import Client
from django.urls import reverse
from book.models import User, Room
from book.views import views_response
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, room_setup, reservation_setup, type_json


class TestViewsRoom(ViewsTestCase):

    @classmethod
    def setUpTestData(cls):
        basic_setup()
        TestUsers.setup()
        room_setup()
        reservation_setup()

    def test_GET_room_list(self):
        client = Client()
        path = reverse('room_list')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证未登录时提示登录
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 验证正常获取房间列表
        TestUsers.use(client, 'U')
        response = client.get(path, {'reserving': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['day_range'], 7)
        waiting_time_span = ['0'*48]*7
        waiting_time_span[1] = '000000000000000011110000000000000001100000000000'
        self.assertEqual(response.json()['data']['waiting_time_span'], waiting_time_span)
        expected_time_span = [['0'*48]*7 for _ in range(5)]
        expected_time_span[0][1] = '000000000000000011110000000000000002200000000000'
        expected_time_span[0][5] = '000000000000000000001110000000000000000000000000'
        expected_time_span[4][1] = '000000000000000033330000000000000000000000000000'
        for num in range(len(expected_time_span)):
            self.assertEqual(response.json()['data']['room_list'][num]['time_span'], expected_time_span[num])

        # 验证只看单个房间
        room = Room.objects.filter(teacher_only=False).first()
        response = client.get(path, {'reserving': True, 'only': 'id:{}'.format(room.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']['room_list']), 1)
        # only参数错误
        response = client.get(path, {'reserving': True, 'only': 'id1'})
        self.assertResponse(response, views_response.invalid_value('only', 'id1'))
        response = client.get(path, {'reserving': True, 'only': 'id:x'})
        self.assertResponse(response, views_response.bad_request("Field 'id' expected a number but got 'x'."))
        # 验证学生看不到教师限定房间
        room = Room.objects.filter(teacher_only=True).first()
        response = client.get(path, {'reserving': True, 'only': 'id:{}'.format(room.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']['room_list']), 0)

        # 只获取房间信息
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), Room.objects.filter(teacher_only=False).count())

    def test_GET_room_info(self):
        client = Client()
        path = reverse('room_info')
        self.checkMethod(client, path, ['PATCH'])

        # 验证未登录时提示登录
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 以普通用户身份测试
        TestUsers.use(client, 'U')

        # 验证未给出room id时提示
        response = client.get(path)
        self.assertResponse(response, views_response.missing_parameter('id'))

        # 验证给出非法room id时提示
        response = client.get(path, data={'id': 'A'})
        self.assertResponse(response, views_response.type_error('id', int, str))

        # 验证给出不存在的room_id时提示
        response = client.get(path, data={'id': -1})
        self.assertResponse(response, views_response.invalid_value('id', -1))

        # 测试普通用户正常获取房间信息
        room = Room.objects.all()[0]
        response = client.get(path, data={'id': room.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], room.info())

    def test_PUT_room_info(self):
        client = Client()
        path = reverse('room_info')

        # 验证未登录时提示登录
        response = client.put(path)
        self.assertResponse(response, views_response.not_logged_in())

        test_data = {'id': Room.objects.all()[0].id}

        # 权限不足
        TestUsers.use(client, User.ADMIN)
        response = client.put(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 超管权限
        TestUsers.use(client, User.ROOT)

        # 正常修改
        data = test_data.copy()
        data['name'] = 'new_room_name'
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Room.objects.get(id=data['id']).name, 'new_room_name')
        # 非法修改
        data['name'] = 'name' * 1000
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 400)

    def test_DELETE_room_info(self):
        client = Client()
        path = reverse('room_info')

        # 验证未登录时提示登录
        response = client.delete(path)
        self.assertResponse(response, views_response.not_logged_in())

        test_data = {'id': Room.objects.all()[0].id}

        # 权限不足
        TestUsers.use(client, User.ADMIN)
        response = client.delete(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 超管权限
        TestUsers.use(client, User.ROOT)

        # 正常删除
        count = Room.objects.count()
        response = client.delete(path, data=test_data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Room.objects.count(), count - 1)

    def test_POST_room_info(self):
        client = Client()
        path = reverse('room_info')

        # 验证未登录时提示登录
        response = client.post(path)
        self.assertResponse(response, views_response.not_logged_in())

        test_data = {
            'name': 'new_room',
            'size': Room.SMALL_SIZE,
            'capacity': 1,
            'floor': 1,
            'teacher_only': True,
            'cs_only': True,
            'has_screen': True,
            'has_projector': True,
            'has_mic': True,
            'note': '',
            'building_id': 1,
            'institute_id': None
        }

        # 权限不足
        TestUsers.use(client, User.ADMIN)
        response = client.post(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 超管权限
        TestUsers.use(client, User.ROOT)

        # 正常添加
        count = Room.objects.count()
        response = client.post(path, data=test_data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Room.objects.count(), count + 1)
        # 非法参数
        data = test_data.copy()
        data['size'] = 100
        response = client.post(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 400)
