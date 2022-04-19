"""
url路由
"""

from django.urls import path
from . import views

urlpatterns = [
    # authentication
    path('check_token',          views.authentication.check_token,      name="check_token"),
    path('login',                views.authentication.login,            name='login'),
    path('logout',               views.authentication.logout,           name='logout'),
    # permission
    path('room_group',           views.permission.room_group,           name='room_group'),
    # reservation
    path('reservation/conflict', views.reservation.conflict,            name='r_conflict'),
    path('reservation/submit',   views.reservation.submit,              name='r_submit'),
    path('reservation/examine',  views.reservation.examine,             name='r_examine'),
    path('reservation/cancel',   views.reservation.cancel,              name='r_cancel'),
    path('reservation/list',     views.reservation.reservation_list,    name='r_list'),
    # room
    path('room/list',            views.room.room_list,                  name='room_list'),
    path('room/info',            views.room.room_info,                  name='room_info'),
    # terminal
    path('terminal/login',       views.terminal.login,                  name='t_login'),
    path('terminal/room_info',   views.terminal.room_info,              name='t_room_info'),
    path('terminal/arrive',      views.terminal.arrive,                 name='t_arrive'),
    path('terminal/leave',       views.terminal.leave,                  name='t_leave'),
    # user
    path('user/info',            views.user.user_info,                  name="user_info"),
    path('user/list',            views.user.user_list,                  name='user_list'),
    path('user/reservation',     views.user.user_reservation,           name='user_reservation'),
    path('institutes',           views.user.institutes,                 name='institutes')
]
