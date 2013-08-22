# COIN FLIP
# Demonstrates the while clause

import random

count = 0
while count < 100:
    coin = random.randint(1, 2)
    if coin == 1:
        # HEADS
        print("HEADS")
    elif coin == 2:
        # TAILS  
        print("TAILS")
    else:
        print("Illegal coin value!  (You must have a fake coin).")
    count += 1

input("\n\nPress the enter key to exit.")





