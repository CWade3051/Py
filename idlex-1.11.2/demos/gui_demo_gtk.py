"""
  Demo for EventLoop.py - interactive GUI development

  This assumes you have PyGTK installed on your system.

  Make sure that you have enabled the Event Loop under "Shell"
  and "Use GTK".

  The "GUI: ON/OFF" button in the status bar is clickable.

"""

## import
import pygtk
pygtk.require('2.0')
import gtk
# If you receive the following warning, this demo will still work:
# "RuntimeWarning: PyOS_InputHook is not available for interactive use of PyGTK"

## make simple interface
def clicked(widget, data=None):
    print('Click received.')

w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.resize(300, 200)
w.set_title('IdleX GUI Event Loop Demo')
b = gtk.Button("Click Me")
b.connect("clicked", clicked, None)
w.add(b)
b.show()
w.show()

#gtk.main()
