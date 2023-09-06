from random import randint

class Fighter():
    
    def __init__(self,name,attack_damage,max_health,initiative) -> None:
        
        self.name:str = name
        self.attack_damage:int = attack_damage
        self.max_health:int = max_health
        self.health:int = self.max_health
        self.initiative:int = initiative
        
        self.attack_percent = 1
        self.idle_percent = 1

        self.wins = 0

    def brain(self)->int: # Returns the damage dealt by the attacker, called each player's turn
        pool = self.attack_percent+self.idle_percent
        selection = randint(1,pool)
        if selection<=self.attack_percent:
            return(self.attack_damage)
        else:
            return(0)
    
    def take_damage(self,damage_taken):
        self.health -= damage_taken