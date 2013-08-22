# Instructions
# Demonstrates programmer-created functions

def instructions():
    """Display game instructions."""  
    print(
    """
    Welcome to the greatest intellectual challenge of all time: Tic-Tac-Toe.  
    This will be a showdown between your human brain and my silicon processor.  

    You will make your move known by entering a number, 0 - 8.  The number 
    will correspond to the board position as illustrated:
    
                    0 | 1 | 2
                    ---------
                    3 | 4 | 5
                    ---------
                    6 | 7 | 8

    Prepare yourself, human.  The ultimate battle is about to begin. \n
    """
    )

# main
print("Here are the instructions to the Tic-Tac-Toe game:")
instructions()
print("Here they are again:")
instructions()
print("You probably understand the game by now.")

input("\n\nPress the enter key to exit.")
