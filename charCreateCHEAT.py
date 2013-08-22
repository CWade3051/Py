# Character creator program
 
skills = {"Strength":0, "Wisdom":0, "Health":0, "Dextarity":0}
points=int(30)
player=""
 
while player != "e":
    print("Welcome to your character\n")
    print("You have ",points," avaliable.")
    print("1. Add points.")
    print("2. Remove Points")
    print("3. Show current status")
    print("Type exit to quit")
    print("------------------")
    selection = input(">")
    if selection == "1":
        pts2 = 0
        pts=int(input("how many points would you like to apply?"))
        if pts > points:
            pts = 0
            print("ha, nice try")
        else:  
            pts2=input("To what attribute would you like to apply? 1. Strength 2. Health 3. Dextarty, or 4. Wisdom?")
            if pts2 == "1":
                skills["Strength"] += pts
                points -= pts
            if pts2 == "2":            
                skills["Health"] += pts
                points -= pts
            if pts2 == "3":
                skills["Dextarity"] += pts
                points -= pts            
            if pts2 == "4":
                skills["Wisdom"] += pts
                points -= pts
    if selection == "2":
        rmv = int(input("How many points would you like back?"))
        rmv2 = input("From where? 1. Strength 2. Health 3. Dextarty, or 4. Wisdom?")
        if rmv2 == "1":
            if rmv < skills["Strength"]:
                skills["Strength"] -= rmv
                points += rmv
            else:
                print("no")
        if rmv2 == "2":
            if rmv < skills["Health"]:
                skills["Health"] -= rmv
                points += rmv
            else:
                print("no")
        if rmv2 == "3":
            if rmv < skills[Dextarity]:
                skills["Dextarity"] -= rmv
                points += rmv
            else:
                print("No")
        if rmv2 == "4":
            if rmv < skills[Wisdom]:
                skills["Wisdom"] -= rmv
                points += rmv
            else:
                print("No")
 
 
    if selection == "3":
          print (skills)