// 前后端接口

const API = {
  LOGIN: {
    path: '/api/login',
    method: 'post'
  },
  CHECK_TOKEN: {
    path: '/api/check_token',
    method: 'get'
  },
  USER_INFO: {
    path: '/api/user/info',
    method: 'get'
  },
  LOGOUT: {
    path: '/api/logout',
    method: 'get'
  },
  SET_ROLE: {
    path: '/api/user/info',
    method: 'put'
  },
  ROOM: {
    path: '/api/room',
    method: 'post'
  },
  ORDERLIST: {
    path: '/api/orderlist',
    method: 'post'
  },
  INFO: {
    path: '/api/info',
    method: 'post'
  },
  MANAGE: {
    path: '/api/manage',
    method: 'post'
  },
  USER_LIST: {
    path: '/api/user/list',
    method: 'get'
  },
  SAVE: {
    path: '/api/user/info',
    method: 'put'
  },
  ROOM_LIST: {
    path: '/api/room/list',
    method: 'get'
  },
  ROOM_INFO: {
    path: '/api/room/list',
    method: 'get'
  },
  ROOM_RESERVE: {
    path: '/api/reservation/submit',
    method: 'post'
  },
  USER_RESERVATION: {
    path: '/api/user/reservation',
    method: 'get'
  },
  CANCEL_RESERVATION: {
    path: '/api/reservation/cancel',
    method: 'put'
  },
  RESERVATION_LIST: {
    path: '/api/reservation/list',
    method: 'get'
  },
  RESERVATION_EXAMINE: {
    path: 'api/reservation/examine',
    method: 'put'
  },
  RESERVATION_CONFLICT: {
    path: 'api/reservation/conflict',
    method: 'get'
  },
  TERMINAL_LOGIN: {
    path: '/api/terminal/login',
    method: 'post'
  },
  TERMINAL_ROOMINFO: {
    path: '/api/terminal/room_info',
    method: 'get'
  },
  TERMINAL_ARRIVE: {
    path: '/api/terminal/arrive',
    method: 'post'
  },
  TERMINAL_LEAVE: {
    path: '/api/terminal/leave',
    method: 'post'
  },
  MODIFY_ROOM_INFO: {
    path: '/api/room/info',
    method: 'put'
  },
  DELETE_ROOM: {
    path: '/api/room/info',
    method: 'delete'
  },
  ADD_ROOM: {
    path: '/api/room/info',
    method: 'post'
  },
  ADD_GROUP: {
    path: '/api/room_group',
    method: 'post'
  },
  DELETE_GROUP: {
    path: '/api/room_group',
    method: 'delete'
  },
  GET_GROUP: {
    path: '/api/room_group',
    method: 'get'
  },
  MODIFY_GROUP: {
    path: '/api/room_group',
    method: 'put'
  }
}

export default API
