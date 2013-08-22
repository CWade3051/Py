# Character Creator
#
# Write a Character Creator program for a role-playing game. The player should be given a pool of 30 points to spend
# on four attributes: Strength, Health, Wisdom, and Dexterity. The player should be able to spend points from the
# pool on any attribute and should also be able to take points from an attribute and put them back into the pool.

# imports

import pprint

# initialize variables

choice = None
strg = 0
hlth = 0
wis = 0
dex = 0
pused = 0
chars = []

# constants

POOL = 30
ATRIB = {"Strength": strg,
         "Health": hlth,
         "Wisdom": wis,
         "Dexterity": dex}
ATRIB2 = [("Wisdom", wis), ("Health", hlth), ("Dexterity", dex), ("Stregth", strg)]

# do the deed

while choice != "0":

    print(
        """
        Character Creator

        0 - Quit
        1 - Create New Character
        2 - Edit Attributes of Existing Character
        3 - Delete Character
        4 - List All Characters and Attributes
        """
    )

    choice = input("Choice: ")
    print()

    # exit
    if choice == "0":
        print("Good-bye.")

    # create new char
    elif choice == "1":
        cname = input("What name do you want your char to have?: ")
        if cname not in chars:
            cstr = input("How much strength do you want them to have?: ")
            chlth = input("How much health do you want them to have?: ")
            cwis = input("How much wisdom do you want them to have?: ")
            cdex = input("How much dexterity do you want them to have?: ")
            cdic = [["Strength", cstr], ["Health", chlth], ["Wisdom", cwis], ["Dexterity", cdex]]
            chars.append([cname, cdic])
            print(cname)
            for key1, value1 in cdic:
                print("  ", key1, value1)
        else:
            print("\nCharacter already exsists! Try editing it or deleting it!")

    # del char
    elif choice == "3":
        term = input("What term do you want me to redefine?: ")
        if term in chars:
            definition = input("What's the new definition?: ")
            chars[term] = definition
            print("\n", term, "has been redefined.")
        else:
            print("\nThat term doesn't exist!  Try adding it.")

    # list chars
    elif choice == "4":
    #        for key in chars[0]:
    #            print(key)
        pprint.pprint(chars, width=5)

    elif choice == "5":
        for key, value in ATRIB.items():
            print(key, value)
        for key2, value2 in ATRIB2:
            print(key2, value2)

# [['bobby', [['Strength', '1'], ['Health', '2'], ['Wisdom', '3'], ['Dexterity', '4']]], ['stacy', [['Strength', '9'], ['Health', '8'], ['Wisdom', '7'], ['Dexterity', '6']]]]

    elif choice == "6":
        print(chars)

    # some unknown choice
    else:
        print("\nSorry, but", choice, "isn't a valid choice.")

input("\n\nPress the enter key to exit.")
