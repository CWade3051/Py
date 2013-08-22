#! /usr/bin/python
# Count
# Demonstrates the range() function

print("""
		Welcome to Chuck's counting app!
		
	You will start by entering a number to start from,
	then enter a number to finsh to, and last enter how
	many you want to count by!
"""
)
start = int(input("\nYour starting number: "))
end = int(input("\nYour ending number: "))
howMany = int(input("\nHow many you want counted by: "))

print("\nCounting by", howMany, ":")
for i in range(start, end, howMany):
    print(i, end=" ")


input("\n\nPress the enter key to exit.\n")