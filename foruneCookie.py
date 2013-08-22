# Fortune cookie
# Demonstrates the elif clause

import random

print("Give me a quater and I'll tell you your fortune!")
print("You are going to...")

fortune = random.randint(1, 5)

if fortune == 1:
    # fortune1
    print("DIE")
elif fortune == 2:
    # fortune 2  
    print("turn GAY")
elif fortune == 3:
    # fortune 3
    print("get ARRESTED")
elif fortune == 4:
    # fortune 4
    print("commit SUICIDE")
elif fortune == 5:
    # fortune 5
    print("suck a COCK")
else:
    print("Illegal fortune value!  (You must have a really bad fortune).")

print("...today!")

input("\n\nPress the enter key to exit.")








