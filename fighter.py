from random import randint

class Fighter():
    
    def __init__(self,name,attack_damage,max_health,initiative,attack_weight,idle_weight) -> None:
        
        self.name:str = name
        self.attack_damage:int = attack_damage
        self.max_health:int = max_health
        self.health:int = self.max_health
        self.initiative:int = initiative
        
        self.attack_weight = attack_weight
        self.idle_weight = idle_weight

        self.wins = 0

    def brain(self)->int: # Returns the damage dealt by the attacker, called each player's turn
        pool = self.attack_weight+self.idle_weight
        selection = randint(1,pool)
        if selection<=self.attack_weight:
            return(self.attack_damage)
        else:
            return(0)
    
    def take_damage(self,damage_taken):
        self.health -= damage_taken