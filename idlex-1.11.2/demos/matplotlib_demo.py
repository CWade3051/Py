"""

Demo of Matplotlib interaction
==============================

Make sure that you have "Enable GUI Event Loop" checked
under the "Shell" menu, as well as the proper toolkit
selected.

Run this code. You'll have an interactive figure.
Click on the figure to see feedback in the shell.

The shell is still usable. If you are missing the ">>>" prompt,
press enter to create a new one.

If you want, change the backend to different toolkits, and then
select the appropriate one under the "Shell" menu.

"""


## code for interaction
from matplotlib import pyplot as plt
import numpy as np

print('You are using the %s backend.' % plt.rcParams['backend'])

plt.interactive(True)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))
plt.title('Click on the plot')

def onclick(event):
    try:
        print ('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata))
        plt.plot(event.xdata, event.ydata, 'o')

        
    except TypeError as e:
        print('Click event received, but outside of plot.', e)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

