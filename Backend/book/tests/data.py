import datetime
from book.models import Building, Department, Institute
from book.views.authentication import new_token
from ..constant import token_expire_timedelta
from ..models import User, Room, Reservation


# 用于PUT和POST请求
type_json = 'application/json'

# 测试用 不存在的uid
not_existed_uid = '9999011299'


def basic_setup():
    # Building
    Building.objects.create(id=1, name='NewBuilding')
    Building.objects.create(id=2, name='EastPrime')

    # Department
    departments = ['计算机科学与技术系']
    for index, department in enumerate(departments):
        Department.objects.create(id=index+1, name=department)

    # Institute
    institutes = ['智能技术与系统国家重点实验室', '人机交互与媒体集成研究所', '计算机网络技术研究所', '高性能计算研究所', '计算机软件研究所']
    for index, institute in enumerate(institutes):
        Institute.objects.create(id=index+1, name=institute)


class TestUsers:

    @staticmethod
    def setup():
        user_num = 15
        user_num_role = [1, 4, 10]
        uid = [str(2019000000 + i) for i in range(user_num)]
        username = ['n' + str(i) for i in range(user_num)]
        fullname = ['张' + str(i) for i in range(user_num)]
        role = [User.ROOT] * user_num_role[0] + \
               [User.ADMIN] * user_num_role[1] + \
               [User.NORMAL_USER] * user_num_role[2]
        email = ['zhangsan{}@mails.tsinghua.edu.cn'.format(i) for i in range(user_num)]
        phone_number = ['188112233' + str(i).rjust(2, '0') for i in range(user_num)]
        institutes = Institute.objects.all()
        institute = [None] * (user_num_role[0] + user_num_role[1]) + \
                    [institutes[i] if i < len(institutes) else None for i in range(user_num_role[2])]
        for i in range(user_num):
            User.objects.create(
                uid=uid[i],
                username=username[i],
                fullname=fullname[i],
                email=email[i],
                phone_number=phone_number[i],
                token=new_token(),
                token_expire_time=datetime.datetime.now() + token_expire_timedelta,
                role=role[i],
                department=Department.objects.all().first(),
                institute=institute[i]
            )

    @staticmethod
    def get(role='U', index=0):
        return User.objects.filter(role=role)[index]

    @staticmethod
    def use(client, role='U'):
        """
        以role身份登录测试
        """
        user = TestUsers.get(role)
        client.cookies['api_token'] = user.token
        return user


def simple_room_setup():
    for room_id in range(1, 6):
        Room.objects.create(
            name='room' + str(room_id),
            size=Room.SMALL_SIZE,
            capacity=50,
            building=Building.objects.all()[0],
            floor=room_id,
            terminal_token='room' + str(room_id)
        )


def room_setup():
    simple_room_setup()
    Room.objects.create(
        name='no_stu',
        size=Room.SMALL_SIZE,
        capacity=20,
        building=Building.objects.all()[0],
        floor=1,
        terminal_token='no_stu',
        teacher_only=True
    )
    for i, ins in enumerate(Institute.objects.all()):
        Room.objects.create(
            name='lab'+str(i+1),
            size=Room.SMALL_SIZE,
            capacity=30,
            building=Building.objects.all()[0],
            floor=2,
            institute=ins,
            terminal_token='lab'+str(i+1)
        )


def reservation_setup():
    # 一个会议室多个时间段
    Reservation.objects.create(
        id=1,
        date=datetime.date.today() + datetime.timedelta(days=1),
        time_span=ispan(17, 20),
        applicant=TestUsers.get(User.ROOT),
        room=Room.objects.all()[0],
        approval_result=True,
        state=Reservation.APPROVED
    )
    Reservation.objects.create(
        id=2,
        date=datetime.date.today() + datetime.timedelta(days=1),
        time_span=ispan(36, 37),
        applicant=TestUsers.get(User.NORMAL_USER),
        room=Room.objects.all()[0],
        approval_result=True,
        state=Reservation.APPROVED
    )
    # 不同天
    Reservation.objects.create(
        id=3,
        date=datetime.date.today() + datetime.timedelta(days=5),
        time_span=ispan(21, 23),
        applicant=TestUsers.get(User.ADMIN),
        room=Room.objects.all()[0],
        approval_result=True,
        state=Reservation.APPROVED
    )
    # 正在申请的
    Reservation.objects.create(
        id=4,
        date=datetime.date.today() + datetime.timedelta(days=1),
        time_span=ispan(17, 20),
        applicant=TestUsers.get(User.NORMAL_USER),
        room=Room.objects.all()[4],
        approval_result=None,
        state=Reservation.WAITING
    )
    Reservation.objects.create(
        id=5,
        date=datetime.date.today() + datetime.timedelta(days=1),
        time_span=ispan(18, 21),
        applicant=TestUsers.get(User.NORMAL_USER, 1),
        room=Room.objects.all()[4],
        approval_result=None,
        state=Reservation.WAITING
    )


def span(a, b):
    """
    输出二进制字符串

    span(2, 3)
    011000000000000000000000000000000000000000000000
    span(47, 48)
    000000000000000000000000000000000000000000000011
    """
    return '0'*(a-1) + '1'*(b-a+1) + '0'*(48-b)


def ispan(a, b):
    """
    输出二进制字符串的int形式

    span(2, 3)
    011000000000000000000000000000000000000000000000 的十进制
    span(47, 48)
    000000000000000000000000000000000000000000000011 的十进制
    """
    return int(span(a, b), 2)
