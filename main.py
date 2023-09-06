from fighter import Fighter 

# Initialisation

number_of_simulations = 1 # Number of simulations (generations of participants) to take place
debug_feedback = False # Tells the program whether to print debug information to the test

fighter_list:list[Fighter] = [] # Create the first batch of competitors
for i in range(20):
    fighter_list.append(Fighter(str(i),1,10,1))


# Battle script

def battle(combatant1:Fighter,combatant2:Fighter):
    # Same code but one is if the fight is narrated or not
    if debug_feedback:
        if combatant2.initiative > combatant1.initiative:
            combatant1, combatant2 = combatant2, combatant1
            print(f"{combatant1.name} is fighting {combatant2.name}")
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
            if combatant2.health < 0:
                combatant1.wins+=1
                break
            combatant1.take_damage(combatant2_damage)
            if combatant1.health<0:
                combatant2.wins+=1
                break
        combatant1.health=combatant1.max_health
        combatant2.health=combatant2.max_health

# Matchmaking

for i in range(len(fighter_list)):
    for j in range(i,len(fighter_list)):
        if fighter_list[j] != fighter_list[i]:
            print(f"{fighter_list[i].name} VS {fighter_list[j].name}")
            battle(fighter_list[i],fighter_list[j])
for fighter in fighter_list:
    print(f"{fighter.name} has won {fighter.wins} times")
# Natural Selection
# Mutation

# Event Handler

