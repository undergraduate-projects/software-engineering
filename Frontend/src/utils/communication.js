// 与后端接口函数

import API from '@/utils/API.js'

/**
 *
 * @author wangtz
 * @export
 * @param {string} authCode OAuth验证第一步从重定向url中得到的授权码，传递给后端进行下一步OAuth验证
 * @return {object} 返回{'result': 'sucess/failure', 'api_token': 'a_token'}。其中result值为success表示后端获取令牌成功，为failure表示失败；api_token为验证成功后，前端用于与后端进行通信的令牌，建议将此令牌存储于cookie中，存储的名称即为api_token。
 */
export async function Login (authCode, path) {
  const response = await fetch(API.LOGIN.path, {
    method: API.LOGIN.method,
    body: JSON.stringify({
      'auth_code': authCode,
      'path': path
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function CheckToken () { // 检查用户是否有效登录
  const response = await fetch(API.CHECK_TOKEN.path, {
    method: API.CHECK_TOKEN.method
  })
  const res = await response.json()
  return res
}

export async function GetUserInfo () { // 如果用户登录，获取其基本信息并返回
  const response = await fetch(API.USER_INFO.path, {
    method: API.USER_INFO.method
  })
  const res = await response.json()
  return res
}

export async function Logout () { // 用户登出
  const response = await fetch(API.LOGOUT.path, {
    method: API.LOGOUT.method
  })
  const res = await response.json()
  return res
}

export async function GetUserList (pagenum, orderBy, only) { // 最多十个用户的信息列表
  let strOnly = ''

  if (only.role.length !== 0) {
    strOnly += `role__in:${only.role.join('')}`
  }
  if (only.institute.length !== 0) {
    if (only.role.length !== 0) {
      strOnly += ','
    }
    strOnly += `institute__in:${only.institute.join('|')}`
  }
  if (only.role.length !== 0 || only.institute.length !== 0) {
    strOnly += ','
  }
  strOnly += only.name_uid_contain

  const response = await fetch(API.USER_LIST.path + '?page_num=' + pagenum + '&order_by=' + orderBy + '&only=' + strOnly, {
    method: API.USER_LIST.method
  })
  const res = await response.json()
  return res
}

export async function SetRole (uid, role, isTeacher, instituteId, banDays) { // 用户权限变更
  const response = await fetch(API.SET_ROLE.path, {

    method: API.SET_ROLE.method,
    body: JSON.stringify({
      'id': uid,
      'role': role,
      'is_teacher': isTeacher,
      'institute_id': instituteId,
      'ban_days': parseInt(banDays)
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  console.log(uid)
  console.log(role)
  console.log(isTeacher)
  console.log(instituteId)
  console.log(banDays)
  const res = await response.json()
  return res
}

export async function Save (email, phonenumber, institute) {
  const response = await fetch(API.SAVE.path, {
    method: API.SAVE.method,
    body: JSON.stringify({
      'email': email,
      'phone_number': phonenumber,
      'institute_id': institute
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function GetRoomList () { // 房间简要信息列表
  const response = await fetch(API.ROOM_LIST.path + '?reserving=True', {
    method: API.ROOM_LIST.method
  })
  const res = await response.json()
  return res
}

export async function GetRoomInfo (roomId) { // 房间详细信息
  const response = await fetch(API.ROOM_INFO.path + '?only=id:' + roomId + '&reserving=True', {
    method: API.ROOM_INFO.method
  })
  const res = await response.json()
  return res
}

export async function RoomReserve (roomId, date, timeSpan, reason) { // 预约
  const response = await fetch(API.ROOM_RESERVE.path, {
    method: API.ROOM_RESERVE.method,
    body: JSON.stringify({
      'room_id': roomId,
      'date': date,
      'time_span': timeSpan,
      'reason': reason
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function GetUserReservation () {
  console.log('GetUserReservation')
  const response = await fetch(API.USER_RESERVATION.path + '?page_num=1', {
    method: API.USER_RESERVATION.method
  })
  const res = await response.json()
  console.log(res)
  return res
}

export async function GetConflictList (id) {
  const response = await fetch(API.RESERVATION_CONFLICT.path + '?res_id=' + id, {
    method: API.RESERVATION_CONFLICT.method
  })
  const res = await response.json()
  return res
}

export async function CancelUserReservation (reservationId) {
  console.log(CancelUserReservation)
  const response = await fetch(API.CANCEL_RESERVATION.path, {
    method: API.CANCEL_RESERVATION.method,
    body: JSON.stringify({
      'id': reservationId
    })
  })
  const res = await response.json()
  console.log(res)
  return res
}

export async function GetReservationList (pagenum, only) {
  // console.log('GetReservationList')
  const response = await fetch(API.RESERVATION_LIST.path + '?page_num=' + pagenum + '&only=' + only, {
    method: API.RESERVATION_LIST.method
  })
  const res = await response.json()
  // console.log(res)
  return res
}

export async function GetExamResList (pagenum, only, orderBy) {
  let path = ''
  if (orderBy) {
    path = API.RESERVATION_LIST.path + '?page_num=' + pagenum + '&only=' + only + '&order_by=-approval_time'
  } else {
    path = API.RESERVATION_LIST.path + '?page_num=' + pagenum + '&only=' + only
  }
  const response = await fetch(path, {
    method: API.RESERVATION_LIST.method
  })
  const res = await response.json()
  return res
}

export async function ExamineReservation (result, reason, id) {
  const response = await fetch(API.RESERVATION_EXAMINE.path, {
    method: API.RESERVATION_EXAMINE.method,
    body: JSON.stringify({
      'result': result,
      'reason': reason,
      'id': id
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  console.log(res)
  return res
}
export async function TerminalLogin (roomId, Token) { // 公共终端登录
  const response = await fetch(API.TERMINAL_LOGIN.path, {
    method: API.TERMINAL_LOGIN.method,
    body: JSON.stringify({
      'room_id': roomId,
      'token': Token
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function Room () {}

export async function TerminalRoomInfo () { // 公共终端所对应房间信息
  const response = await fetch(API.TERMINAL_ROOMINFO.path, {
    method: API.TERMINAL_ROOMINFO.method
  })
  const res = await response.json()
  return res
}

export async function TerminalArrive (token) { // 签到
  const response = await fetch(API.TERMINAL_ARRIVE.path, {
    method: API.TERMINAL_ARRIVE.method,
    body: JSON.stringify({
      'token': token
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function TerminalLeave (token) { // 签退
  const response = await fetch(API.TERMINAL_LEAVE.path, {
    method: API.TERMINAL_LEAVE.method,
    body: JSON.stringify({
      'token': token
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const res = await response.json()
  return res
}

export async function GetRootRoomList () { // 房间信息列表
  const response = await fetch(API.ROOM_LIST.path + '?root=true', {
    method: API.ROOM_LIST.method
  })
  const res = await response.json()
  return res
}

export async function ModifyRootRoomInfo (roomDic) { // 修改房间信息
  const response = await fetch(API.MODIFY_ROOM_INFO.path, {
    method: API.MODIFY_ROOM_INFO.method,
    body: JSON.stringify(roomDic)
  })
  const res = await response.json()
  return res
}

export async function DeleteRootRoom (roomDic) { // 删除会议室
  const response = await fetch(API.DELETE_ROOM.path, {
    method: API.DELETE_ROOM.method,
    body: JSON.stringify(roomDic)
  })
  const res = await response.json()
  return res
}

export async function AddRootRoom (roomDic) { // 新增会议室
  const response = await fetch(API.ADD_ROOM.path, {
    method: API.ADD_ROOM.method,
    body: JSON.stringify(roomDic)
  })
  const res = await response.json()
  console.log(res)
  return res
}

export async function AddGroup (groupDic) {
  const response = await fetch(API.ADD_GROUP.path, {
    method: API.ADD_GROUP.method,
    body: JSON.stringify(groupDic)
  })
  const res = await response.json()
  return res
}

export async function DeleteGroup (groupDic) {
  const response = await fetch(API.DELETE_GROUP.path, {
    method: API.DELETE_GROUP.method,
    body: JSON.stringify(groupDic)
  })
  const res = await response.json()
  return res
}

export async function GetGroup () {
  const response = await fetch(API.GET_GROUP.path, {
    method: API.GET_GROUP.method
  })
  const res = await response.json()
  return res
}

export async function ModifyGroup (groupDic) {
  const response = await fetch(API.MODIFY_GROUP.path, {
    method: API.MODIFY_GROUP.method,
    body: JSON.stringify(groupDic)
  })
  const res = await response.json()
  return res
}

export async function GetAdminList () {
  const response = await fetch(API.USER_LIST.path + '?order_by=&only=role__in:AR', {
    method: API.USER_LIST.method
  })
  const res = await response.json()
  return res
}

export async function GetRoomReservation (roomId, pageNum) {
  const response = await fetch(API.RESERVATION_LIST.path + '?&only=state__in:UFLB&room=' + roomId +
    '&page_num=' + pageNum, {
    method: API.RESERVATION_LIST.method
  })
  const res = await response.json()
  return res
}
