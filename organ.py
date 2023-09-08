import action
from random import randint
class Organ():

    def __init__(self,name):
        self.name = name
        self.actions: list[action.Action] = []

    def check_prerequisites(self,fighter)->bool:
        pass
    
    def on_combat(self,fighter,enemy):
        pass

    def on_turn(self,fighter,enemy):
        pass
    
    def on_damage_taken(self,fighter):
        pass

    def on_mutate(self,fighter):
        pass

    def on_devolution(self,fighter):
        pass

    def display_organ(self)->str:
        pass

class Heart(Organ):

    def __init__(self, name, health_bonus,energy_cost):
        super().__init__(name)
        self.health_bonus = health_bonus
        self.energy_cost = energy_cost
    
    def check_prerequisites(self,fighter)->bool:
        if fighter.max_energy>self.energy_cost:
            fighter.max_health += self.health_bonus
            fighter.max_energy-=self.energy_cost
            return True
        else:
            return False

    def on_mutate(self,fighter):
        healthgain = randint(-5,5)
        fighter.max_health += healthgain
        self.health_bonus += healthgain
    
    def on_devolution(self, fighter):
        fighter.max_health -= self.health_bonus
        fighter.max_energy += self.energy_cost

    def display_organ(self) -> str:
        return(f"{self.name} - HP:{self.health_bonus} - EC:{self.energy_cost}")

class CoagulatoryGland(Organ):

    def __init__(self, name, health_regen,starting_weight, passive_energy_cost,energy_per_health,max_uses):
        super().__init__(name)
        self.actions: list[action.Heal] = [action.Heal("HEAL",starting_weight,health_regen,energy_per_health,max_uses)]
        self.passive_energy_cost = passive_energy_cost
        self.energy_per_health = energy_per_health
        self.max_uses = max_uses

    def check_prerequisites(self, fighter) -> bool:
        if fighter.max_energy <= self.passive_energy_cost:
            return False
        else:
            fighter.max_energy -= self.passive_energy_cost
            fighter.action_pool.append(self.actions[0])

    def on_combat(self, fighter, enemy):
        self.actions[0].uses = self.actions[0].max_uses

        
    def on_devolution(self, fighter):
        fighter.max_energy+=self.passive_energy_cost
        fighter.action: list[action.Action].remove(self.actions[0])

    def on_mutate(self,fighter):
        match randint(1,4):
            case 1: # health regen
                self.actions[0].health_regen+=randint(-2,2)
            case 2: # weight
                self.actions[0].weight +=randint(-1,1)
            case 3: # energy per health
                self.energy_per_health += randint(-1,1)
            case 4: # Max uses
                self.max_uses += randint(-1,1)
                self.actions[0].max_uses = self.max_uses

    def display_organ(self) -> str:
        return(f"{self.name} - REGEN:{self.actions[0].health_regen} - WEIGHT:{self.actions[0].weight} - EPH:{self.actions[0].energy_per_health}")