"""
    Squeezer Demo

    This will generate a lot of text. With Squeezer, this text
    will be captured and displayed as a box, similar to

    [ Squeezed text (about 188 lines).
      Double-click to expand, middle-click to copy, right-click to preview ]

    This will prevent IDLE from locking up when displaying a lot of
    text to the shell.

"""

## [subcode]

import random
L = []
for i in range(5000):
    L.append(random.randint(0, 9))

print(L)  # print a lot of text



