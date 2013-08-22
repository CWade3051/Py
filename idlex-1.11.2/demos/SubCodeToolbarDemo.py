"""
    SubCode Toolbar Demo

    This file will show how to use the SubCodeToolbar extension in IDLE.

    Make sure that "Enable Subcode" and "Show Subcode Toolbar"
    are checked under Options.

    About:

    [>] - list of subcode labels
    [##] - insert a subcode marker

    [-] 1.0 [+]  - add or subtract from number by cursor
    [/] 1.1 [*]  - divide or multiply number by cursor

    [RS] - Run SubCode
    [RSP] - Run SubCode and Proceed
    [RA] - Run All subcodes
    
"""

## Introduction

# The [>] button will show a menu of all subcodes in the source code.
# Clicking one will jump to it

# The [##] button will insert a subcode into the source near
# the cursor, like this one:

## [subcode]



## Numerical Adjustments (addition and subtraction)

# Demo for [-] 1.0 [+]

a = 50  # place the cursor on the number "50"
        # and click [-] or [+] in the toolbar

# You can change "1.0" to any number you want.

print('Displaying Number: %i' % a)
for i in range(4):
    print('-' * (i+2))


## Numerical Adjustments (multiplication and division)

# Demo for [/] 1.1 [*]

b = 110.0  # place the curson on the number "110.0"
           # and click [/] or [*] in the toolbar

# You can change "1.1" to any number you want.

print('Displaying Number: %f' % b)
for i in range(4):
    print('-' * (i+2))


## The Run Subcode Buttons

# These are shortcuts to the menu items under the "Run" menu.

