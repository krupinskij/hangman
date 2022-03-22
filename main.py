levels = {
    "beginner": {"chances": 8},
    "intermediate": {"chances": 5},
    "advanced": {"chances": 3}
}

languages = {
    "english": "en",
    "german": "de",
    "italian": "it",
    "spanish": "es"
}

mode = {
    "single": 1,
    "multiplayer": 2
}


class Game:
    def __init__(self, players_count):
        self.players_count = players_count

    def __play(self):
        print("Game started")


class Hangman(Game):
    def __init__(self, players_count, level):
        super().__init__(players_count)
        self.level = level


hangman = Hangman(mode["single"], levels["beginner"])
