export function readCookie (name) { // 通用函数，读取某个cookie
  let fullname = name + '='
  let cookies = document.cookie.split(';')
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i]
    while (c.charAt(0) === ' ') c = c.substring(1)
    if (c.indexOf(fullname) !== -1) return c.substring(fullname.length, c.length)
  }
  return ''
}

export function deleteCookie (name) { // 通用函数，删除某个cookie
  setCookie(name, '', -100)
}

export function setCookie (name, value, minutes) { // 通用函数，设置某个cookie
  let d = new Date()
  d.setTime(d.getTime() + (minutes * 60 * 1000))
  document.cookie = name + '=' + value + ';expires=' + d.toUTCString() + ';path=/'
}
