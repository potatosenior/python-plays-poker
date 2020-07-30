import win32api, win32con
from time import sleep

def click(data, btn):
  # clicks on one of the 3 buttons
  # 1 fold
  # 2 call/check
  # 3 call/raise
  l, t, w, h = data.window.left, data.window.top, data.window.width, data.window.height

  if btn == 1:
    x = l + int(w/2 + w/2/3 * 0.5)
    y = t + int(h * 0.95)
  elif btn == 2:
    x = l + int(w/2 + w/2/3 * 1.5)
    y = t + int(h * 0.95)
  elif btn == 3:
    x = l + int(w/2 + w/2/3 * 2.5)
    y = t + int(h * 0.95)
  
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  win32api.SetCursorPos((int(w/2),int(h/2)))
  sleep(1)

if __name__ == "__main__":
  click(40,5)