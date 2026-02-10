from random import choice
from quiz import quiz
class Game:
    def __init__(self):
        self.game_players = set()
        self.game_started = False
        self.init_hp = 4
        self.question = choice(quiz)
    
    def start_game(self):
        self.game_started = True
        self.damage_random_player()
    
    def end_game(self):
        self.game_started = False
        self.game_players.clear()
    
    def handle_answers(self):
        if not self.game_players:
            return
        answers = [p.answer for p in self.game_players]
        answers_set = {}
        for player in self.game_players:
            answers_set[player.answer] = answers_set.get(player.answer, 0) + 1
        if len(set(answers)) == 1:
            self.agreement()
        elif max(answers_set.values()) == len(self.game_players) - 1: 
            self.sabotage(answers_set)
        else: 
            self.failure()

    def failure(self):
        for player in self.game_players:
            player.hp -= 1
    def sabotage(self, answers_set):
        major = max(answers_set, key=answers_set.get)
        for p in self.game_players:
            if p.answer != major:
                continue
            p.hp -= 1
    def agreement(self):
        pass
    def damage_random_player(self):
        if not self.game_players:
            return
        player = choice(list(self.game_players))
        player.hp -= 1
    def set_random_question(self):
        self.question = choice(quiz)