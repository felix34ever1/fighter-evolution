import action
from random import randint
class Organ():

    def __init__(self,name):
        self.name = name
        self.actions: list[action.Action] = []

    def check_prerequisites(self,fighter)->bool:
        '''Returns a True if the organ can grow, also applies the costs on the fighter, actions should also be appended to fighter here.'''
        pass
    
    def on_combat(self,fighter,enemy):
        '''Triggers at the start of combat.'''
        pass

    def on_turn(self,fighter,enemy):
        '''Triggers on the fighter's turn '''
        pass
    
    def on_damage_taken(self,fighter):
        '''Triggers when damage is taken ''' #Should probably take the actual damage being taken
        pass

    def on_mutate(self,fighter):
        '''Triggers when the organ is mutated'''
        pass

    def on_devolution(self,fighter):
        '''Triggers when the organ is removed'''
        pass

    def display_organ(self)->str:
        '''Returns a string to be displayed next to the fighter info'''
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
            return True

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
    
class SapGland(Organ):

        def __init__(self, name,starting_weight,evolution_energy_cost, sap_per_energy, used_energy):
            super().__init__(name)
            self.evolution_energy_cost = evolution_energy_cost
            self.sap_per_energy = sap_per_energy
            self.used_energy = used_energy
            self.weight = starting_weight
            self.actions: list[action.Sap] = [action.Sap("SAP",starting_weight,sap_per_energy,used_energy)]

        def check_prerequisites(self, fighter) -> bool:
            if fighter.max_energy >= self.used_energy and fighter.max_energy > self.evolution_energy_cost:
                fighter.max_energy -= self.evolution_energy_cost
                fighter.action_pool.append(self.actions[0])
                return True
            return False
        
        def on_mutate(self, fighter):
            choice = randint(0,1)
            if choice == 0: # Change sap per energy
                self.sap_per_energy += randint(-1,1)
                self.actions[0].sap_per_energy = self.sap_per_energy
            else: # Change energy spent
                self.used_energy += randint(-1,1)
                self.actions[0].used_energy = self.used_energy
        
        def on_devolution(self, fighter):
            fighter.max_energy += self.evolution_energy_cost
        
        def display_organ(self) -> str:
            return(f"{self.name}|SAPS:{self.sap_per_energy*self.used_energy}|E_USE:{self.used_energy}")
        