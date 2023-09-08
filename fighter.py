from random import randint
import action
import organ

class Fighter():
    
    def __init__(self,name,attack_damage,max_health,initiative,action_pool,max_energy,energy_regain,energy_damage_ratio,organs) -> None:
        
        self.name:str = name
        self.attack_damage:int = attack_damage
        self.max_health:int = max_health
        self.health:int = self.max_health
        
        self.max_energy:int = max_energy
        self.energy:int = self.max_energy
        self.energy_regain:int = energy_regain
        self.energy_damage_ratio:int = energy_damage_ratio

        self.initiative:int = initiative

        self.organs:list[organ.Organ] = organs
        
        self.action_pool:list[action.Action] = action_pool
        

        self.wins = 0

    def brain(self,enemy)->int: # Returns the damage dealt by the attacker, called each player's turn
        pool:int = 0
        for organ in self.organs:
            organ.on_turn(self,enemy)
        for action in self.action_pool:
            pool += action.weight
        selected_item = randint(1,pool)
        selected_pool = 0
        for action in self.action_pool:
            selected_pool += action.weight
            if selected_item <= selected_pool:
                damage = action.used(self,enemy)
                return(damage)
        else:
            return 0
                
    
    def take_damage(self,damage_taken):
        for organ in self.organs:
            organ.on_damage_taken(self)
        self.health -= damage_taken