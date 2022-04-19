from datetime import datetime
from django.test import Client
from django.urls import reverse
from book.models import User, Department, Institute, Reservation
from book.views import views_response
from .case import ViewsTestCase
from .data import basic_setup, TestUsers, type_json, not_existed_uid


class TestViewsUser(ViewsTestCase):

    @classmethod
    def setUpTestData(cls):
        basic_setup()
        TestUsers.setup()

    def test_GET_user_info(self):
        client = Client()
        path = reverse('user_info')

        # 验证COOKIE没有加入api_token时，提示登陆
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 验证以不同身份登陆时，都能得到自己的用户信息
        for user_role in User.ROLES:
            TestUsers.use(client, user_role)
            response = client.get(path)
            self.assertEqual(response.status_code, 200)

    def test_PUT_user_info(self):
        client = Client()
        path = reverse('user_info')
        self.checkMethod(client, path, ['POST'])

        # 验证COOKIE没有加入api_token时，提示登陆
        response = client.put(path)
        self.assertResponse(response, views_response.not_logged_in())

        for user_role in User.ROLES:
            TestUsers.use(client, user_role)

            test_data = {
                'email': 'zhansan19@mails.tsinghua.edu.cn',
                'phone_number': '18811556666',
                'institute_id': 2,
            }

            # 验证未设置content_type时json解析body失败时报错
            response = client.put(path, test_data)
            self.assertResponse(response, views_response.invalid_format())

            # 验证email格式错误时报错
            data = test_data.copy()
            data['email'] = 'invalid_email_address'
            response = client.put(path, data=data, content_type=type_json)
            self.assertResponse(response, views_response.bad_request("ValidationError:['Email invalid']"))

            # 验证phone_number格式错误时报错
            data = test_data.copy()
            data['phone_number'] = '1122334455'
            response = client.put(path, data=data, content_type=type_json)
            self.assertResponse(response, views_response.bad_request("ValidationError:['Phone number invalid']"))

            # 验证institute非整数时报错
            data = test_data.copy()
            data['institute_id'] = 'X'
            response = client.put(path, data=data, content_type=type_json)
            self.assertEqual(response.status_code, 400)

            # 验证institute不存在时报错
            data = test_data.copy()
            data['institute_id'] = -1
            response = client.put(path, data=data, content_type=type_json)
            self.assertEqual(response.status_code, 400)

            # 验证修改成功
            response = client.put(path, data=test_data, content_type=type_json)
            self.assertEqual(response.json()['data'], 'Success for keys:'+str(list(test_data.keys())))

        # 以下测试超管修改用户信息

        test_data = {'id': TestUsers.get(User.NORMAL_USER).id}

        # 无权限
        TestUsers.use(client, User.NORMAL_USER)
        response = client.put(path, data=test_data, content_type=type_json)
        self.assertResponse(response, views_response.no_permission())

        # 超管权限
        TestUsers.use(client, User.ROOT)

        # 错误id
        response = client.put(path, data={'id': 'X'}, content_type=type_json)
        self.assertResponse(response, views_response.type_error('id', int, str))
        response = client.put(path, data={'id': -1}, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('id', -1))

        # 测试修改role
        data = test_data.copy()
        data['role'] = User.ADMIN
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=data['id']).role, User.ADMIN)
        # 非法修改role
        data['role'] = User.ROOT
        response = client.put(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('role', User.ROOT))

        # 测试修改department和institute
        data = test_data.copy()
        data['department_id'] = None
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=data['id']).department, None)
        data = test_data.copy()
        data['institute_id'] = Institute.objects.all()[1].id
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=data['id']).institute, Institute.objects.all()[1])

        # 测试封禁功能
        data = test_data.copy()
        data['ban_days'] = 1
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(User.objects.get(id=data['id']).unban_time), True)
        data['ban_days'] = 0
        response = client.put(path, data=data, content_type=type_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=data['id']).unban_time <= datetime.now(), True)
        # 非法参数
        data['ban_days'] = -1
        response = client.put(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.invalid_value('ban_days', -1))
        data['ban_days'] = 'X'
        response = client.put(path, data=data, content_type=type_json)
        self.assertResponse(response, views_response.type_error('ban_days', int, str))

    def test_GET_user_list(self):
        client = Client()
        path = reverse('user_list')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证COOKIE没有加入api_token时，提示登陆
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 验证非Root身份时报错
        for user_role in User.ROLES:
            if user_role != 'R':
                TestUsers.use(client, user_role)
                response = client.get(path)
                self.assertResponse(response, views_response.no_permission())

        # 以下测试均使用Root身份
        TestUsers.use(client, 'R')

        test_data = {
            'page_num': 1,
            'order_by': '',
            'only': '',
        }

        # 验证无参数page_num时返回全部用户
        data = test_data.copy()
        data.pop('page_num')
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)

        # 验证参数page_num类型不是数字时报错
        data = test_data.copy()
        data['page_num'] = 'one'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.type_error('page_num', int, str))

        # 验证参数page_num非法时报错
        data = test_data.copy()
        data['page_num'] = 233
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('page_num', 233))

        # 验证无参数order_by时报错
        data = test_data.copy()
        data.pop('order_by')
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.missing_parameter('order_by'))

        # 验证传入错误only参数时报错
        data = test_data.copy()
        data['only'] = 'U'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('only', 'U'))

        # 验证传入非法only键值时报错
        data = test_data.copy()
        data['only'] = 'gpa:4.0'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.bad_request('key `gpa` in `only` is invalid'))

        # 验证搜索不存在的身份时返回列表为空
        data = test_data.copy()
        data['only'] = 'role:B'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], 0)
        self.assertEqual(response.json()['data']['list'], [])

        # 验证输入错误院系id报错
        data = test_data.copy()
        data['only'] = 'department:CS'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.bad_request("Field 'id' expected a number but got 'CS'."))

        # 验证输入不存在的研究所id无返回值
        data = test_data.copy()
        data['only'] = 'institute:-1'
        response = client.get(path, data=data)
        self.assertEqual(response.json()['data']['total'], 0)

        # 验证成功返回全部数据
        response = client.get(path, data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], User.objects.count())

        # 验证只看某种用户
        data = test_data.copy()
        for user_role in User.ROLES:
            data['only'] = 'role:'+user_role
            response = client.get(path, data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['data']['total'],
                             User.objects.filter(role=user_role).count())

        # 验证只看某个院系
        data = test_data.copy()
        data['only'] = 'department:'+str(Department.objects.all().first().id)
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'],
                         User.objects.filter(department=Department.objects.all().first()).count())

        # 验证只看某个研究所
        data['only'] = 'institute:'+str(Institute.objects.all().first().id)
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'],
                         User.objects.filter(institute=Institute.objects.all().first()).count())

        # 验证多个参数
        user = TestUsers.get('U')
        data['only'] = 'fullname:'+user.fullname+',role:U'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'],
                         User.objects.filter(fullname=user.fullname, role='U').count())

        data['only'] = 'fullname:'+user.fullname+',role:R'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'],
                         User.objects.filter(fullname=user.fullname, role='R').count())

        user = TestUsers.get('U')
        data['only'] = 'role:U,department:{},institute:{},'\
            .format(user.department.id, user.institute.id)
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'],
                         User.objects.filter(role='U', department=user.department,
                                             institute=user.institute).count())

        # 验证按名字拼音排序
        data = test_data.copy()
        data['order_by'] = 'fullname'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)

        # 验证倒序
        data = test_data.copy()
        data['order_by'] = '-'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        data['order_by'] = '-fullname'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)

        # only特殊参数
        data = test_data.copy()
        # role__in
        data['only'] = 'role__in:AR'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], User.objects.filter(role__in='AR').count())
        # institute__in
        data['only'] = 'institute__in:1|2|3'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['total'], User.objects.filter(institute_id__in=[1,2,3]).count())
        # institute__in 非法
        data['only'] = 'institute__in:1|i'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('only.institute__in', '1|i'))
        data['only'] = 'institute__in:1|-1'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.bad_request('Institute-1 does not exist'))
        # banned
        data['only'] = 'banned:true'
        response = client.get(path, data=data)
        self.assertEqual(response.status_code, 200)
        # banned 非法
        data['only'] = 'banned:false'
        response = client.get(path, data=data)
        self.assertResponse(response, views_response.invalid_value('only.banned', 'false'))

    def test_user_reservation(self):
        client = Client()
        path = reverse('user_reservation')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 验证未登陆时报错
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        user = TestUsers.use(client, 'U')

        # 验证正常获取预约信息
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']['list']), Reservation.objects.filter(applicant=user).count())

    def test_institutes(self):
        client = Client()
        path = reverse('institutes')
        self.checkMethod(client, path, ['PUT', 'POST'])

        # 未登录
        response = client.get(path)
        self.assertResponse(response, views_response.not_logged_in())

        # 正常获取
        TestUsers.use(client, User.NORMAL_USER)
        response = client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), Institute.objects.count())
