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
  def __init__(self, players_count, level, language):
    super().__init__(players_count)
    self.level = level
    self.language = language

print("HANGMAN")


def selectOption(options_dict, options_name):
  option = ""
  while option not in options_dict:
    option = input(f"Select {options_name} ({', '.join(list(options_dict.keys()))}): ").lower()

  print(f"Selected {option}")
  return option;


mode_input = selectOption(mode, "mode")
levels_input = selectOption(levels, "level")
languages_input = selectOption(languages, "language")

hangman = Hangman(mode[mode_input], levels[levels_input], languages[languages_input])
