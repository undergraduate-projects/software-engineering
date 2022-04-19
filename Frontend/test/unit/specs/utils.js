
export async function triggerTextButton (wrapper, text) { // 点击特定文本的按钮
  let allbuttons = wrapper.findAll('button')
  for (let i = 0; i < allbuttons.length; i++) {
    if (allbuttons.at(i).text() === text) {
      await allbuttons.at(i).trigger('click')
      return
    }
  }
}
