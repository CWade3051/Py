# Who's Your Grand Daddy Program, Written by Charles Wade in August of 2013

# Write a Who's Your Daddy? program that lets the user enter the name of a male
# and produces the name of his father. (You can use celebrities, fictional characters,
# or even historical figures for fun.) Allow the user to add, replace, and delete father-son pairs.

# Improve the Who’s Your Daddy program by adding a choice that
# lets the user enter a name and get back a grandfather. Your
# program should still only use one dictionary of son-father
# pairs. Make sure to include several generations in your
# dictionary so that a match can be found.

import pickle
choice = None
wydd = {"Bobby Cave":{"Greg Cave": "Ernie Cave"},"Charles Wade Sr":{"Charles Wade": "Charlie Wade"},
		"Newton Waldron":{"Brian Waldron": "Dennis Waldron"}}

while choice != "0":
	print("""
		Who's Your Daddy?
		=================
		Created by Charles Wade in August of 2013

		Welcome to the only program that will tell who a persons
		daddy is! Select an option below to find out all about
		who someone's daddy is!

		0 - Quit
		1 - Find out who's your daddy
		2 - Add a daddy
		3 - List daddys
		4 - Replace a daddy
		5 - Delete a daddy
		6 - Save daddys
		7 - Load daddys
		8 - Erase all daddys

		Note: To restore default daddys (if you accidently delete them) just restart the program.

	""")
	choice = input("Choice: ")
	print()

	# exit
	if choice == "0":
		print("Good-bye.")

	# find out whos your daddy
	elif choice == "1":
		print("\nHere are all of your people you can currently find out who their daddy is:\n")
		for key in wydd:
			print(key)
		whoRU = input("\nWhats your name (or the persons name that you want to know who their daddy is)? ")
		whoRUCap = whoRU.title()
		if whoRUCap in wydd:
			print("\nWho's your daddy ", whoRUCap, "? ", wydd[whoRUCap], sep='')
		else:
			print("\nI dont know who your daddy is :( You can add him from the main menu!")

	# add a daddy
	elif choice == "2":
		addDad = input("What is the name of the daddy? ")
		addDadCap = addDad.title()
		print("What is the name of ", addDadCap, "'s son? ", sep='')
		addSon = input(">")
		addSonCap = addSon.title()
		wydd.update({addSonCap: addDadCap})
		print("\nYou added ", addDadCap, " as the daddy of ", addSonCap, "!", sep='')

	# list daddys
	elif choice == "3":
		if wydd:
			for key in wydd:
				print("Who's your daddy", key, "?")
				print("  ", wydd.get(key), "\n")
		else:
			print("\nYou have no daddys! Try creating some!")

	# replace a daddy
	elif choice == "4":
		print("\nHere are all of the sons you can currently replace daddys for:\n")
		if wydd:
			for key in wydd:
				print("  ", key, "\n")
			dadRep = input("Which son would you like the daddy to be replaced for? ")
			dadRepCap = dadRep.title()
			if dadRepCap in wydd:
				print("\nCurrently ", dadRepCap, "'s daddy is ", wydd[dadRepCap], "!", sep='')
				newDad = input("What daddy would you like to replace them with? ")
				newDadCap = newDad.title()
				wydd[dadRepCap] = newDadCap
				print("\n", dadRepCap, "'s new daddy is now ", newDadCap, "!", sep='')
			else:
				print("\nThat daddy doesnt exsist! Try adding him!")
		else:
			print("\nYou have no daddys! Try adding some!")

	# delete a daddy
	elif choice == "5":
		dadDel = input("Which daddy would you like to delete?: ")
		dadDelCap = dadDel.title()
		if dadDelCap in wydd:
			areusure = input("\nAre you sure you want to delete this daddy? 'Y' for YES, 'N' for NO: ")
			areusureCap = areusure.upper()
			if areusureCap == "Y":
				del wydd[dadDelCap]
				print("\nDaddy WAS deleted!")
			else:
				print("\nDaddy NOT deleted!")
		else:
			print("\nThat Daddy doesnt exist! Try adding him.")

	# save daddys
	elif choice == "6":
		pickle.dump(wydd, open("save.p", "wb"))
		print("\nAll your daddys have been saved! Choose option 7 to reload them on next launch!")

	# load daddys
	elif choice == "7":
		wydd = pickle.load(open("save.p", "rb"))
		print("\nAll the following daddys have been loaded from your last save:\n")
		if wydd:
			for key in wydd:
				print("Who's your daddy", key, "?")
				print("  ", wydd.get(key), "\n")
		else:
			print("\nYou have no daddys! Try creating some!")

	# erase daddys
	elif choice == "8":
		areusure2 = input("\nAre you sure you want to erase ALL daddys? 'Y' for YES, 'N' for NO: ")
		areusureCap2 = areusure2.upper()
		if areusureCap2 == "Y":
			wydd = {}
			print("\nAll daddys have been erased!")
		else:
			print("\nDaddys NOT erased!")

	# some unknown choice
	else:
		print("\nSorry, but", choice, "isn't a valid choice.")
