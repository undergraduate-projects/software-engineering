from django.test import Client
from django.urls import reverse
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, room_setup, type_json
from book.views import views_response
from book.models import RoomGroup, Room

class TestViewsRoomGroup(ViewsTestCase):

    @classmethod
    def setUpTestData(cls):
        basic_setup()
        TestUsers.setup()
        room_setup()

        g = RoomGroup.objects.create(name='test1')
        g.rooms.add(Room.objects.all().first())
        g.admins.add(TestUsers.get('A'))
    
    def test_POST_room_group(self):
        client = Client()
        path = reverse('room_group')

        #######################################################################
        # 只需测一遍

        # 未登录
        response = client.post(path)
        self.assertResponse(response, views_response.not_logged_in())
        # 不是root
        TestUsers.use(client, 'U')
        response = client.post(path)
        self.assertResponse(response, views_response.no_permission())

        TestUsers.use(client, 'R')
        self.checkMethod(client, path, ['PATCH'])

        #######################################################################

        # json
        response = client.post(path, data={'name': 'n'})
        self.assertResponse(response, views_response.invalid_format())
        # 确少参数
        response = client.post(path, data={'wrong': 'w'}, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('name'))
        # 参数type error
        response = client.post(path, data={'name': 12}, content_type=type_json)
        self.assertResponse(response, views_response.type_error('name', str, int))
        # name过长
        response = client.post(path, data={'name': '1'*260}, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('name', '1'*260))
        # name重复
        response = client.post(path, data={'name': 'test1'}, content_type=type_json)
        self.assertEqual(response.status_code, 410)
        # 成功
        response = client.post(path, data={'name': 'test2'}, content_type=type_json)
        self.assertResponse(response, views_response.success({'id': 2}))

    def test_DELETE_room_group(self):
        client = Client()
        path = reverse('room_group')
        TestUsers.use(client, 'R')

        # json
        response = client.delete(path)
        self.assertResponse(response, views_response.invalid_format())
        # 确少参数
        response = client.delete(path, data={'wrong': 'w'}, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('id'))
        # 参数type error
        response = client.delete(path, data={'id': 'dsf'}, content_type=type_json)
        self.assertResponse(response, views_response.type_error('id', int, str))
        # 房间不存在
        response = client.delete(path, data={'id': -1}, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('id', 'group id -1 not found'))
        # 成功删除
        response = client.delete(path, data={'id': 1}, content_type=type_json)
        self.assertResponse(response, views_response.success())

    def test_GET_room_group(self):
        client = Client()
        path = reverse('room_group')
        TestUsers.use(client, 'R')

        response = client.get(path)
        self.assertEqual(response.json()['data'], [{
            'id': 1,
            'name': 'test1',
            'rooms': [{
                'id': Room.objects.all().first().id,
                'name': Room.objects.all().first().name
            }],
            'admins': [{
                'id': TestUsers.get('A').id,
                'fullname': TestUsers.get('A').fullname
            }]
        }])
    
    def test_PUT_room_group(self):
        client = Client()
        path = reverse('room_group')
        TestUsers.use(client, 'R')

        # json
        response = client.put(path, data={'name': 'n'})
        self.assertResponse(response, views_response.invalid_format())
        # 确少参数
        response = client.put(path, data={
            'name': 'www',
            'rooms': [1, 2],
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('group_id'))
        response = client.put(path, data={
            'group_id': 1,
            'rooms': [1, 2],
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('name'))
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('rooms'))
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [1, 2],
        }, content_type=type_json)
        self.assertResponse(response, views_response.missing_parameter('admins'))
        # 参数type error
        response = client.put(path, data={
            'group_id': [],
            'name': 'www',
            'rooms': [1, 2],
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('group_id', int, list))
        response = client.put(path, data={
            'group_id': 1,
            'name': 233,
            'rooms': [1, 2],
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('name', str, int))
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': 233,
            'admins': [3, 4]
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('rooms', list, int))
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [1, 2],
            'admins': 233
        }, content_type=type_json)
        self.assertResponse(response, views_response.type_error('admins', list, int))

        # room id not valid
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [[]],
            'admins': []
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('rooms', 'room id not valid'))
        # room not found
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [-1],
            'admins': []
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('rooms', 'room id not found'))
        # admin id not valid
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [1],
            'admins': [[]]
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('admins', 'admin id not valid'))
        # admin not found
        response = client.put(path, data={
            'group_id': 1,
            'name': 'www',
            'rooms': [1],
            'admins': [-1]
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('admins', 'admin id not found'))
        # group not found
        response = client.put(path, data={
            'group_id': -1,
            'name': 'www',
            'rooms': [1],
            'admins': [TestUsers.get('A').id]
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('group_id', 'group id not found'))
        # name not valid
        response = client.put(path, data={
            'group_id': 1,
            'name': 'w'*260,
            'rooms': [1],
            'admins': [TestUsers.get('A').id]
        }, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('name', 'w'*260))
        # success
        response = client.put(path, data={
            'group_id': 1,
            'name': 'w',
            'rooms': [1],
            'admins': [TestUsers.get('A').id]
        }, content_type=type_json)
        self.assertResponse(response, views_response.success())

        # 以下测试修改管理员的房间组
        response = client.put(path, data={
            'admin_id': TestUsers.get('A').id,
            'groups': [1]
        }, content_type=type_json)
        self.assertResponse(response, views_response.success())
