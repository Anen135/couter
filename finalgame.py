from random import choice
class FinalGame:
    def __init__(self):
        self.bomb_holder = None      
        self.bomb_status = None      
        self.swap_used = False     
        self.game_active = False

    def start_game(self, players):
        self.game_active = True
        self.swap_used = False
        self.bomb_holder = choice(players)
        self.bomb_status = choice(["bomb", "empty"])
    def end_game(self):
        self.bomb_holder = None      
        self.bomb_status = None      
        self.swap_used = False     
        self.game_active = False