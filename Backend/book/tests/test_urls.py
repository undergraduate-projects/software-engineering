from django.test import SimpleTestCase
from django.urls import reverse, resolve
from book.views import authentication, permission, reservation, room, terminal, user


class TestUrls(SimpleTestCase):

    def check_url(self, url, func):
        url = reverse(url)
        self.assertEqual(resolve(url).func, func)

    def test_authentication_urls(self):
        self.check_url('check_token', authentication.check_token)
        self.check_url('login', authentication.login)
        self.check_url('logout', authentication.logout)

    def test_permission_urls(self):
        self.check_url('room_group', permission.room_group)

    def test_reservation_urls(self):
        self.check_url('r_conflict', reservation.conflict)
        self.check_url('r_submit', reservation.submit)
        self.check_url('r_examine', reservation.examine)
        self.check_url('r_cancel', reservation.cancel)
        self.check_url('r_list', reservation.reservation_list)

    def test_room_urls(self):
        self.check_url('room_list', room.room_list)
        self.check_url('room_info', room.room_info)

    def test_terminal_urls(self):
        self.check_url('t_login', terminal.login)
        self.check_url('t_room_info', terminal.room_info)
        self.check_url('t_arrive', terminal.arrive)
        self.check_url('t_leave', terminal.leave)

    def test_user_urls(self):
        self.check_url('user_info', user.user_info)
        self.check_url('user_list', user.user_list)
        self.check_url('user_reservation', user.user_reservation)
        self.check_url('institutes', user.institutes)
