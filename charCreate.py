# Character Creator written by Charles Wade in August of 2013

# Write a Character Creator program for a role-playing game. The player should be given a pool of 30 points to spend
# on four attributes: Strength, Health, Wisdom, and Dexterity. The player should be able to spend points from the
# pool on any attribute and should also be able to take points from an attribute and put them back into the pool.

# import statements

import pickle

# initialize variables

choice = None
chars = {}

# constants

POOL = 30

# do the deed

while choice != "0":

    print("""
    Character Creator
    =================
    Written by Charles Wade in August of 2013
    
    Please choose your option below:

    0 - Quit
    1 - Create New Character
    2 - Edit Attributes of Existing Character
    3 - Delete Character
    4 - List All Characters and Attributes
    5 - Save All Characters
    6 - Load All Characters
    7 - Erase All Characters
    """)
    
    choice = input("Choice: ")
    print()

    # exit
    if choice == "0":
        print("Good-bye.")

    # create new char
    elif choice == "1":
        pool = POOL
        name = input("What name do you want your character to have?: ")
        while name == "":
            name = input("What name do you want your character to have?: ")
        cname = name.capitalize()
        if cname not in chars:
            print("\nYou have ", pool, " points to spend on Strength, Health, Wisdom, and Dexterity!")
            strn = input("How much strength do you want them to have?: ")
            try:
                cstr = int(strn)
            except ValueError:
                print("\nThat is not a number, made strength 0 and moving on! You can edit after if it was a mistake.")
                cstr = 0
            while cstr > pool:
                print("Not enough points left in pool, you have ", pool, " points available, try again!")
                cstr = int(input("How much strength do you want them to have?: "))
            else:
                pool -= cstr                
            print("\nYou have ", pool, " points to spend!")
            hlth = input("How much health do you want them to have?: ")
            try:
                chlth = int(hlth)
            except ValueError:
                print("\nThat is not a number, making health 0 and moving on! You can edit after if it was a mistake.")
                chlth = 0
            while chlth > pool:
                print("Not enough points left in pool, you have ", pool, " points available, try again!")
                chlth = int(input("How much health do you want them to have?: "))
            else:
                pool -= chlth
            print("\nYou have ", pool, " points to spend!")
            wis = input("How much wisdom do you want them to have?: ")
            try:
                cwis = int(wis)
            except ValueError:
                print("\nThat is not a number, making wisdom 0 and moving on! You can edit after if it was a mistake.")
                cwis = 0
            while cwis > pool:
                print("Not enough points left in pool, you have ", pool, " points available, try again!")
                cwis = int(input("How much wisdom do you want them to have?: "))
            else:
                pool -= cwis
            print("\nYou have ", pool, " points to spend!")
            dex = input("How much dexterity do you want them to have?: ")
            try:
                cdex = int(dex)
            except ValueError:
                print("\nThat is not a number, made dexterity 0 and moving on! You can edit after if it was a mistake"
                      ".")
                cdex = 0
            while cdex > pool:
                print("Not enough points left in pool, you have ", pool, " points available, try again!")
                cdex = int(input("How much dexterity do you want them to have?: "))
            else:
                pool -= cdex
            cdic = {"Strength": cstr, "Health": chlth, "Wisdom": cwis, "Dexterity": cdex}
            chars.update({cname: cdic})
            print("\n")
            print(cname, "\n")
            for key in cdic:
                print(key)
                print(cdic.get(key))
        else:
            print("\nCharacter already exsists! Try editing it or deleting it!")

    # edit chars
    elif choice == "2":
        print("\nHere are all of your characters you can currently edit:\n")
        for key in chars:
            print(key)
            print(chars.get(key), "\n")
        editchar = input("Which character would you like to edit?: ")
        editcharCap = editchar.capitalize()
        if editcharCap in chars:
            pool2 = POOL
            print("\nYou have ", pool2, " points to spend on Strength, Health, Wisdom, and Dexterity!")
            strn2 = input("How much strength do you want them to have?: ")
            try:
                cstr2 = int(strn2)
            except ValueError:
                print("\nThat is not a number, made strength 0 and moving on! You can edit after if it was a mistake.")
                cstr2 = 0
            while cstr2 > pool2:
                print("Not enough points left in pool, you have ", pool2, " points available, try again!")
                cstr2 = int(input("How much strength do you want them to have?: "))
            else:
                pool2 -= cstr2
            print("\nYou have ", pool2, " points to spend!")
            hlth2 = input("How much health do you want them to have?: ")
            try:
                chlth2 = int(hlth2)
            except ValueError:
                print("\nThat is not a number, making health 0 and moving on! You can edit after if it was a mistake.")
                chlth2 = 0
            while chlth2 > pool2:
                print("Not enough points left in pool, you have ", pool2, " points available, try again!")
                chlth2 = int(input("How much health do you want them to have?: "))
            else:
                pool2 -= chlth2
            print("\nYou have ", pool2, " points to spend!")
            wis2 = input("How much wisdom do you want them to have?: ")
            try:
                cwis2 = int(wis2)
            except ValueError:
                print("\nThat is not a number, making wisdom 0 and moving on! You can edit after if it was a mistake.")
                cwis2 = 0
            while cwis2 > pool2:
                print("Not enough points left in pool, you have ", pool2, " points available, try again!")
                cwis2 = int(input("How much wisdom do you want them to have?: "))
            else:
                pool2 -= cwis2
            print("\nYou have ", pool2, " points to spend!")
            dex2 = input("How much dexterity do you want them to have?: ")
            try:
                cdex2 = int(dex2)
            except ValueError:
                print("\nThat is not a number, made dexterity 0 and moving on! You can edit after if it was a mistake"
                      ".")
                cdex2 = 0
            while cdex2 > pool2:
                print("Not enough points left in pool, you have ", pool2, " points available, try again!")
                cdex2 = int(input("How much dexterity do you want them to have?: "))
            else:
                pool2 -= cdex2
            cdic2 = {"Strength": cstr2, "Health": chlth2, "Wisdom": cwis2, "Dexterity": cdex2}
            chars.update({editcharCap: cdic2})
            print("\n")
            print(editcharCap, "\n")
#            print(cdic.items())
            for key in cdic2:
                print(key)
                print(cdic2.get(key))
        else:
            print("\nThat character doesnt exsist, try creating them!")

    # del char
    elif choice == "3":
        chardel = input("Which character would you like to delete?: ")
        chardelCap = chardel.capitalize()
        if chardelCap in chars:
            areusure = input("\nAre you sure you want to delete this character? 'Y' for YES, 'N' for NO: ")
            areusureCap = areusure.upper()
            if areusureCap == "Y":
                del chars[chardelCap]
                print("\nCharacter WAS deleted!")
            else:
                print("\nCharacter NOT deleted!")
        else:
            print("\nThat character doesnt exist!  Try adding it.")
       
    # list chars
    elif choice == "4":
        if chars:
            for key in chars:
                print(key)
                print(chars.get(key))
        else:
            print("\nYou have no characters! Try creating some!")

    # save chars
    elif choice == "5":
        pickle.dump(chars, open("save.p", "wb"))
        print("\nAll your characters have been saved! Choose option 6 to reload them on next launch!")

    # load chars
    elif choice == "6":
        chars = pickle.load(open("save.p", "rb"))
        print("\nAll the following characters have been loaded from your last save:\n")
        if chars:
            for key in chars:
                print(key)
                print(chars.get(key))
        else:
            print("\nYou have no characters! Try creating some!")

    # wipe all chars
    elif choice == "7":
        areusure2 = input("\nAre you sure you want to erase ALL characters? 'Y' for YES, 'N' for NO: ")
        areusureCap2 = areusure2.upper()
        if areusureCap2 == "Y":
            chars = {}
            print("\nAll characters have been erased!")
        else:
            print("\nCharacters NOT erased!")

    # some unknown choice
    else:
        print("\nSorry, but", choice, "isn't a valid choice.")
  
input("\n\nPress the enter key to exit.")