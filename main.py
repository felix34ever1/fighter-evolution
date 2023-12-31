from fighter import Fighter 
from random import randint
from datetime import datetime
import action
import organ
import copy

# Initialisation

number_of_simulations = 500 # Number of simulations (generations of participants) to take place
debug_feedback = False # Tells the program whether to print debug information to the test

fighter_list:list[Fighter] = [] # Create the first batch of competitors
for i in range(100):
    fighter_list.append(Fighter(str(i),1,30,1,[action.Attack("ATK",5),action.Idle("IDLE",5)],180,5,10,[])) 

# Battle script

def battle(combatant1:Fighter,combatant2:Fighter):
    # Same code but one is if the fight is narrated or not
    if debug_feedback:
        if combatant2.initiative > combatant1.initiative:
            combatant1, combatant2 = combatant2, combatant1
            print(f"{combatant1.name} VS {combatant2.name}")
        while True:
            combatant1_damage = combatant1.brain(combatant2)
            combatant2_damage = combatant2.brain(combatant1)
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
            combatant1_damage = combatant1.brain(combatant2)
            combatant2_damage = combatant2.brain(combatant1)
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

def check_letters(fighter_list:list[Fighter],removed_string:str)->str:
    ''' Cuts down fighter names and returns the ex generation that has dominated the field.'''
    letter = fighter_list[0].name[0]
    same_letter = True
    for fighter in fighter_list:
        if fighter.name[0] != letter:
            same_letter = False
    if same_letter == False:
        return removed_string
    else:
        for fighter in fighter_list:
            fighter.name = fighter.name[1:]
        return check_letters(fighter_list,removed_string+letter)

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
    bloodline = check_letters(fighter_list,"")
    if len(bloodline) != 0:
        file.write(f"Fighter '{bloodline}'s children dominate the arena!\n")
    for fighter in fighter_list:
        string = f"{fighter.name}: {fighter.wins} - DMG:{fighter.attack_damage} - Health:{fighter.max_health} - Initiative:{fighter.initiative} - Priorities:|{fighter.action_pool[0].weight}:{fighter.action_pool[1].weight}| - Energy(Max,Regen,EPDMG):|{fighter.max_energy}:{fighter.energy_regain}:{fighter.energy_damage_ratio}|"
        for _organ in fighter.organs:
            string+=" "+_organ.display_organ()
        file.write(f"{string}\n")
    file.write("========================\n\n")
    file.close()
    return(fighter_list)
            
# Mutation
def mutation(fighter_list:list[Fighter]) -> fighter_list:
    organ_list:list[organ.Organ] = [
#        organ.Heart("HRT",3,15),
        organ.CoagulatoryGland("CGLND",10,2,10,1,3),
        organ.SapGland("SGLND",5,5,40,1)
    ]
    new_list = []
    for fighter in fighter_list:
        for i in range(10):
            new_fighter = Fighter(fighter.name+"."+str(i),fighter.attack_damage,fighter.max_health,fighter.initiative,copy.deepcopy(fighter.action_pool),fighter.max_energy,fighter.energy_regain,fighter.energy_damage_ratio,copy.deepcopy(fighter.organs))
            if randint(1,5) == 1: # IF 1, a mutation occurs (therefore about 2 offspring per parent mutate, keeping a healthy baseline population)
                mutation = randint(1,15)
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
                        for action in new_fighter.action_pool:
                            if action.name == "ATK":
                                action.weight +=randint(-1,1)
                                if action.weight <=0:
                                    action.weight = 1
                    case 5: # idle weight (up or down by up to 1) (Should be awful and anything with high idle should die off.)
                        for action in new_fighter.action_pool:
                            if action.name == "IDLE":
                                action.weight +=randint(-1,1)
                                if action.weight <=0:
                                    action.weight = 1
                    case 6: # Max energy
                        new_fighter.max_energy+=randint(-15,15)
                        if new_fighter.max_energy <=0:
                            new_fighter.max_energy = 1
                    case 7: # Energy Regain
                        new_fighter.energy_regain+=randint(-3,3)
                        if new_fighter.energy_regain<=0:
                            new_fighter.energy_regain = 1
                    case 8: # Energy to Damage ratio 
                        new_fighter.energy_damage_ratio+=randint(-1,1)
                        if new_fighter.energy_damage_ratio<=0:
                            new_fighter.energy_damage_ratio=1
                    case 9: # Change a mutation
                        if len(new_fighter.organs)!=0:
                            new_fighter.organs[randint(0,len(new_fighter.organs)-1)].on_mutate(new_fighter)
                    case 10,11,12,13,14,15: # Get a new mutation!
                        organ_index = randint(0,len(organ_list)-1)
                        new_organ:organ.Organ = copy.deepcopy(organ_list[organ_index])
                        has_organ = False
                        for _organ in new_fighter.organs:
                            if _organ.name==new_organ.name:
                                has_organ = True
                        if has_organ:
                            pass
                        else:
                            if new_organ.check_prerequisites(new_fighter):
                                new_fighter.organs.append(new_organ)
            new_list.append(new_fighter)
    fighter_list = new_list
    return(fighter_list)
                

        

# Event Handler

file = open("logs/log.txt","a")
file.write("Round 0\n")
file.close()
match_making(fighter_list)
fighter_list = natural_selection(fighter_list)
fighter_list = mutation(fighter_list)
for i in range(number_of_simulations):
    file = open("logs/log.txt","a")
    file.write(f"Round {i+1}\n")
    file.close()
    match_making(fighter_list)
    fighter_list = natural_selection(fighter_list)
    #if i == 10:
    #    for fighter in fighter_list:
    #        fighter.energy_damage_ratio = fighter.energy_damage_ratio*5
    fighter_list = mutation(fighter_list)