class Game:
  def __init__(self, players_count):
      self.players_count = players_count

  def __play(self):
    print("Game started")


class Hangman(Game):
  def __init__(self, players_count):
      super().__init__(players_count)



hangman = Hangman(1)