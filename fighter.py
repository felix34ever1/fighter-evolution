from random import randint

class Fighter():
    
    def __init__(self,name,attack_damage,max_health,initiative,attack_weight,idle_weight,max_energy,energy_regain,energy_damage_ratio) -> None:
        
        self.name:str = name
        self.attack_damage:int = attack_damage
        self.max_health:int = max_health
        self.health:int = self.max_health
        
        self.max_energy:int = max_energy
        self.energy:int = self.max_energy
        self.energy_regain:int = energy_regain
        self.energy_damage_ratio:int = energy_damage_ratio

        self.initiative:int = initiative
        
        self.attack_weight = attack_weight
        self.idle_weight = idle_weight

        self.wins = 0

    def brain(self)->int: # Returns the damage dealt by the attacker, called each player's turn
        pool = self.attack_weight+self.idle_weight
        selection = randint(1,pool)
        if selection<=self.attack_weight:
            if self.energy>0:
                self.energy-=self.attack_damage*self.energy_damage_ratio
                return(self.attack_damage)
            else:
                return(0)
        else:
            self.energy += self.energy_regain
            if self.energy>self.max_energy:
                self.energy = self.max_energy
            return(0)
    
    def take_damage(self,damage_taken):
        self.health -= damage_taken