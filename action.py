from random import randint
class Action():

    def __init__(self,name,weight) -> None:
        self.name = name
        self.weight = weight

    def used(self,fighter,enemy) -> int:
        ''' Takes in enemy as an optional input, returns the damage value and might do other stuff'''
        return 0
    
class Attack(Action):
    def __init__(self,name,weight)-> None:
        super().__init__(name,weight)

    def used(self,fighter,enemy) -> int:
        if fighter.energy <= 0:
            return 0
        else:
            fighter.energy -= fighter.attack_damage*fighter.energy_damage_ratio
            return fighter.attack_damage
        

class Idle(Action):
    def __init__(self, name, weight) -> None:
        super().__init__(name, weight)

    def used(self,fighter,enemy) -> int:
        fighter.energy += fighter.energy_regain
        if fighter.energy>fighter.max_energy:
            fighter.energy = fighter.max_energy
        return(0)
    
class Heal(Action):
    def __init__(self, name, weight, health_regen,energy_per_health, max_uses) -> None:
        super().__init__(name, weight)
        self.health_regen = health_regen
        self.energy_per_health = energy_per_health
        self.max_uses = max_uses
        self.uses = max_uses

    def used(self, fighter,enemy)-> int:
        if fighter.energy < self.energy_per_health * self.health_regen:
            if self.uses > 0 and fighter.health != fighter.max_health:
                self.uses-= 1    
                fighter.health+=self.health_regen
                fighter.energy -= self.energy_per_health * self.health_regen
                if fighter.health > fighter.max_health:
                    fighter.health = fighter.max_health
        return 0
