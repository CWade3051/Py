"""

    SubCode Tutorial File
    ---------------------
    
    This file will show how to use the SubCode extension in IDLE.

    Make sure that "Enable Subcode" is checked under "SubCode".
    
    Follow the directions that are single-commented.

"""


## This is a SubCode marker. A double comment denotes it.
# Place the text cursor here.
# Press CTRL+Return to run this subcode.
# The active subcode region is highlighted.
# Then press CTRL+Shift+Return to run this subcode and
# proceed to the next.

print("Code being executed")
a = 0

print("Last line executed")
## This is another SubCode.
# Press CTRL+Return several times.
# You'll see the value of "a" increase. Go to the next subcode.

print("Count: a = %i" % a)
a += 1

## SubCodes may be indented
# Press CTRL+Return. Then move to the indented subcode by pressing
# Ctrl+Down.

print('Outer Subcode')
if True:
    ## This is an indented SubCode
    # Press CTRL+ENTER. Code will be dedented and executed
    # automatically.
    print("Indented Subcode")

    # The active subcode ends when encountering code at a
    # shallower depth.
    # Proceed to the next subcode by pressing Ctrl+Down
    print("End of Indented Subcode")
print('Part of the outer subcode')

## Uncommenting #: code
# Pressing CTRL+Return will display 0 through 4.
# Proceed to the indented subcode.

for i in range(5):
    ## Test the inner loop code
    # Press Ctrl+Return
    #:print('Uncommented code')
    #:i = 55;  # This is test value
    print(i)

    # The #: at the subcode's indentaiton depth will be uncommented.
    # This is useful for testing code.

print('Done with subcode')  # at depth=0

## Commenting out regions
# Using the "Comment Out Region" won't interfere with SubCode
# markers. Consecutive lines of "##" are treated as comments, with
# some caveats. SubCode markers may not be preceeded by unlabeled
# SubCode markers.

##
##print (123)
##print (456)
##print (789)
##

if True:
    ## Indented SubCode

    print ("Indented")
# comments at shallow depths are ignored. This allows
# "Comment Out Region" to comment out part of a subcode
# without truncating it.
##    print ("Blah")

##  Labeled SubCode markers can not have more than one space
##  between ## and the label.

    print ("Still Indented")
    # Press Ctrl+Return



## Caveats about indented SubCodes
# The indented subcode markers indicate how much dedenting is
# needed. The active subcode spans until a line has non-whitespace
# characters shallower than the active subcode's depth. This means
# that line-continuations or multiline arguments may truncate a
# subcode too early and lead to a syntax error. To avoid this,
# indent multi-line statements appropriately.

if 1:
    ## indent depth = 4. Execution leads to a syntax error
    print('depth=4')

    if 1:
        ## indent depth = 8 - This subcode works
        print('depth=8')

    print('code',  # bad subcode truncation here for depth=4
1)
    if 1: # this line is considered to be in subcode at depth=0
          # because of "1)"
        ## indent depth = 12 - This subcode works


# shallow comment
        print('depth=12')
        
    print('code')  # Ctrl+Return here will run the depth=0 subcode
                   # because of "1)"
                ## indent depth = 16
    
                # nothing will happen when pressing Ctrl+Return here.

## Summary

# SubCodes allow you to segment and execute parts of your script.
# Enjoy iterative development.

## Other Notes
"""

SubCode.py binds Ctrl+F6 in the editor so it restarts the shell.
The combination Ctrl+F6 and Ctrl+F5 are funcionally equivalent to F5.

The "Import Subcode" will import (and reload) the subcode as a module.
If you Click on "Import All Subcodes", you will see all the printing
in this module. In the shell, you can type the following to see the value
of "a":

 >>> SubCodeTutorial.a
 1
 
"""


