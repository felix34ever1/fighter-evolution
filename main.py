from fighter import Fighter 
from random import randint

# Initialisation

number_of_simulations = 500 # Number of simulations (generations of participants) to take place
debug_feedback = False # Tells the program whether to print debug information to the test

fighter_list:list[Fighter] = [] # Create the first batch of competitors
for i in range(100):
    fighter_list.append(Fighter(str(i),1,10,1,5,5))

# Battle script

def battle(combatant1:Fighter,combatant2:Fighter):
    # Same code but one is if the fight is narrated or not
    if debug_feedback:
        if combatant2.initiative > combatant1.initiative:
            combatant1, combatant2 = combatant2, combatant1
            print(f"{combatant1.name} VS {combatant2.name}")
        while True:
            combatant1_damage = combatant1.brain()
            combatant2_damage = combatant2.brain()
            combatant2.take_damage(combatant1_damage)
            print(f"{combatant2.name} takes {combatant1_damage} to be at {combatant2.health} health")
            if combatant2.health < 0:
                print(f"{combatant1.name} is victorious!")
                combatant1.wins+=1
                break
            combatant1.take_damage(combatant2_damage)
            print(f"{combatant1.name} takes {combatant2_damage} to be at {combatant1.health} health")
            if combatant1.health<0:
                combatant2.wins+=1
                print(f"{combatant2.name} is victorious!")
                break
        combatant1.health=combatant1.max_health
        combatant2.health=combatant2.max_health
    
    else:
        if combatant2.initiative > combatant1.initiative:
            combatant1, combatant2 = combatant2, combatant1
        while True:
            combatant1_damage = combatant1.brain()
            combatant2_damage = combatant2.brain()
            combatant2.take_damage(combatant1_damage)
            if combatant2.health <= 0:
                combatant1.wins+=1
                break
            combatant1.take_damage(combatant2_damage)
            if combatant1.health<=0:
                combatant2.wins+=1
                break
        combatant1.health=combatant1.max_health
        combatant2.health=combatant2.max_health

# Matchmaking
def match_making(fighter_list):
    for i in range(len(fighter_list)):
        for j in range(i,len(fighter_list)):
            if fighter_list[j] != fighter_list[i]:
                battle(fighter_list[i],fighter_list[j])


# Natural Selection

def natural_selection(fighter_list:list[Fighter])->fighter_list:    
    list_size = len(fighter_list)
    for i in range(0,list_size):
        for j in range(0,list_size-1):
            if fighter_list[j].wins > fighter_list[j+1].wins:
                fighter_list[j],fighter_list[j+1] = fighter_list[j+1],fighter_list[j]
    if debug_feedback:
        for fighter in fighter_list:
            print(f"{fighter.name} has won {fighter.wins} times")
    fighter_list = fighter_list[-10:100]
    file = open("logs/log.txt","a")
    for fighter in fighter_list:
        file.write(f"{fighter.name}: {fighter.wins} - DMG:{fighter.attack_damage} - Health:{fighter.max_health} - Initiative:{fighter.initiative} - Weights:|{fighter.attack_weight}:{fighter.idle_weight}|\n")
    file.write("========================\n\n")
    file.close()
    return(fighter_list)
            
# Mutation
def mutation(fighter_list:list[Fighter]) -> fighter_list:
    new_list = []
    for fighter in fighter_list:
        for i in range(10):
            new_fighter = Fighter(fighter.name+"."+str(i),fighter.attack_damage,fighter.max_health,fighter.initiative,fighter.attack_weight,fighter.idle_weight)
            if randint(1,5) == 1: # IF 1, a mutation occurs (therefore about 2 offspring per parent mutate, keeping a healthy baseline population)
                mutation = randint(1,5)
                match mutation:
                    case 1: # Damage (up or down by up to 1) 
                        new_fighter.attack_damage += randint(-1,1)
                        if new_fighter.attack_damage == 0:
                            new_fighter.attack_damage = 1
                    case 2: # Health (up or down by up to 3)
                        new_fighter.max_health += randint(-3,3)
                    case 3: # initiative (up or down by up to 1)
                        new_fighter.initiative += randint(-1,1)
                    case 4: # attack weight (up or down by up to 2)
                        new_fighter.attack_weight += randint(-2,2)
                        if new_fighter.attack_weight <= 0:
                            new_fighter.attack_weight = 1
                    case 5: # idle weight (up or down by up to 1) (Should be awful and anything with high idle should die off.)
                        new_fighter.idle_weight +=randint(-1,1)
                        if new_fighter.idle_weight <=0:
                            new_fighter.idle_weight = 1
            new_list.append(new_fighter)
    fighter_list = new_list
    return(fighter_list)
                

        

# Event Handler

match_making(fighter_list)
fighter_list = natural_selection(fighter_list)
fighter_list = mutation(fighter_list)
for i in range(number_of_simulations):
    match_making(fighter_list)
    fighter_list = natural_selection(fighter_list)
    fighter_list = mutation(fighter_list)