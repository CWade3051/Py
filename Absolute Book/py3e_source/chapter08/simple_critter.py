# Simple Critter
# Demonstrates a basic class and object 

class Critter(object):
    """A virtual pet"""
    def talk(self):
        print("Hi.  I'm an instance of class Critter.")

# main
crit = Critter()
crit.talk()

input("\n\nPress the enter key to exit.")
