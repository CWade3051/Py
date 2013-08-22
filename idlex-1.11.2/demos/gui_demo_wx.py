"""
  Demo for EventLoop.py - interactive GUI development

  This assumes you have "wx" installed on your system.

  Make sure that you have enabled the Event Loop under "Shell"
  and "Use wx".

  The "GUI: ON/OFF" button in the status bar is clickable.

"""
import wx

app = wx.App(redirect=False)

def clicked(ev=None):
    print('Click received.')

top = wx.Frame(None, title="IdleX GUI Event Loop Demo", size=(300,200))
top.Show()
btn = wx.Button(top, label='Click Me')
btn.Bind(wx.EVT_BUTTON, clicked)

#app.MainLoop()

