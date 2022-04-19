import mock
from django.test import Client
from django.urls import reverse
from requests import RequestException
from book.models import User
from book.views.authentication import new_token
from book.views import views_response
from book.views.authentication import get_user
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, type_json, not_existed_uid


class TestViewsAuthentication(ViewsTestCase):

    @classmethod
    def setUpTestData(cls):
        basic_setup()
        TestUsers.setup()

    def test_GET_check_token(self):
        client = Client()
        path = reverse('check_token')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证用户登陆有效返回True
        for user_role in User.ROLES:
            TestUsers.use(client, user_role)
            response = client.get(path)
            self.assertResponse(response, views_response.success('True'))

        # 验证用户登陆失效时返回False
        client.cookies['api_token'] = new_token()
        response = client.get(path)
        self.assertResponse(response, views_response.success('False'))

    def test_POST_login(self):
        client = Client()
        path = reverse('login')
        self.checkMethod(client, path, ['GET', 'PUT'])

        # 验证没有auth_code等信息时报错
        response = client.post(path)
        self.assertResponse(response, views_response.invalid_format())

        # 验证auth_code错误时登录失败
        params = {
            'auth_code': '',
            'path': ''
        }
        response = client.post(path, params, content_type=type_json)
        self.assertEqual(response.json()['result'], 'fail')

        # 用mock测试通过auth_code验证的情况
        with mock.patch('requests.post') as mock_post:
            with mock.patch('requests.get') as mock_get:
                class MockResponse:
                    data = {}

                    def __init__(self, _data):
                        self.data = _data

                    def json(self):
                        return self.data

                mock_post.return_value = MockResponse({'access_token': ''})

                user = TestUsers.get('U')
                data = {'user': {
                    'name': user.username,
                    'fullname': user.fullname,
                    'email': user.email,
                    'student_id': user.uid,
                    'mobile': user.phone_number
                }}
                mock_get.return_value = MockResponse(data)

                # 测试成功登录
                response = client.post(path, params, content_type=type_json)
                self.assertEqual(response.json()['result'], 'success')

                # 测试新用户登录
                data['user']['student_id'] = not_existed_uid
                data['user']['name'] = 'new_user'

                mock_get.return_value = MockResponse(data)
                count = User.objects.count()
                response = client.post(path, params, content_type=type_json)
                self.assertEqual(response.json()['result'], 'success')
                self.assertEqual(User.objects.count(), count+1)

                # 测试验证服务器给出错误信息
                data['user']['student_id'] = '0'*100
                mock_get.return_value = MockResponse(data)
                response = client.post(path, params, content_type=type_json)
                self.assertEqual(response.json()['result'], 'fail')

                # 测试向验证服务器获取用户信息失败
                mock_get.side_effect = RequestException()
                response = client.post(path, params, content_type=type_json)
                self.assertEqual(response.json()['result'], 'fail')
                self.assertEqual(response.json()['error'], 'failed in getting user_info')

                # 测试向验证服务器获取access_token失败
                mock_post.side_effect = RequestException()
                response = client.post(path, params, content_type=type_json)
                self.assertEqual(response.json()['result'], 'fail')
                self.assertEqual(response.json()['error'], 'failed in getting access_token')

    def test_GET_logout(self):
        client = Client()
        path = reverse('logout')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证非登陆状态时提示
        response = client.get(path)
        self.assertResponse(response, views_response.success('Login timeout or not logged in'))

        # 验证用户成功下线
        user = TestUsers.use(client, 'U')
        response = client.get(path)
        self.assertResponse(response, views_response.success('Logout OK'))

        # 虚拟请求，用于调用get_user
        class VirtualRequest:
            COOKIES = {'api_token': ''}

            def __init__(self, token):
                self.COOKIES['api_token'] = token

        # 确认用户已下线
        request = VirtualRequest(user.token)
        self.assertEqual(get_user(request), None)
