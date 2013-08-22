# This is example code for use with the Wing IDE tutorial, which
# is accessible from the Help menu of the IDE

import os

print("Starting up...")
print("This code runs outside of the debugger")

# A breakpoint on the following line will not be reached
x = "test value"

print("Now starting the debugger and attaching to the IDE")
import wingdbstub

if 'WINGDB_ACTIVE' in os.environ:
    print("Success starting debug")
else:
    print("Failed to start debug... continuing without debug")

# Set a breakpoint on the following line; it should be reached
# if debugging started successfully
print x

print("Done")

