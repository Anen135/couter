class Player:
    def __init__(self, id, name, hp):
        self.id = id
        self.name = name
        self.hp = hp
        self.answer = ""
    
    def __str__(self):
        return f"{self.name} ({self.hp})"