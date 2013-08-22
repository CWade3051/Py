"""
  Demo for EventLoop.py - interactive GUI development

  Make sure that you have enabled the Event Loop under "Shell"
  and "Use Tkinter".

  The "GUI: ON/OFF" button in the status bar is clickable.

  Note: This file also makes use of SubCodes, but is not required.

"""

## import needed libraries
import sys
if sys.version < '3':
    import Tkinter as tk
else:
    import tkinter as tk

root = None

## Make a GUI

try:
    root.destroy()
except:
    pass

root = tk.Tk()
root.geometry('300x200')
root.title('Idlex GUI Event Loop Demo')

def clicked():
    print('Click received.')

B = tk.Button(root, text='Click me', command=clicked)
B.pack()

# Clicking the "Click me" button will print to the shell.
# The shell is still interactive.

## Add more widgets

L = tk.Label(root, text='This is a label')
L.pack()


# Notice that calling mainloop is not needed.
#root.mainloop()
