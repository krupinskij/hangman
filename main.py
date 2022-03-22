import json
import re
import random

levels = {
  "beginner": {"chances": 8},
  "intermediate": {"chances": 5},
  "advanced": {"chances": 3}
}

languages = {
  "english": "en",
  "polish": "pl"
}

mode = {
  "single": 1,
  "multiplayer": 2
}


class Game:
  def __init__(self, players_count):
    self.players_count = players_count

  def _play(self):
    print("Game started")


class Hangman(Game):
  def __init__(self, players_count, level, language):
    super().__init__(players_count)
    self.level = level
    self.language = language
    self.rounds = []
    self.current_round = None

  def start_game(self):
    self._play()

    while True:
      print("Nowa runda")
      round = self.start_round()
      print(round.word)

      while True:
        letter = input("Get new letter: ")
        
        if round.check_letter(letter):
          print(f"Brawo: {round.hidden_word}")

          if round.check_word():
            print("Brawo brawo brawo")
            break
        else:
          print("Błąd")

          if round.chances == 0:
            print("Przegrywasz!!!")
            break

  def start_round(self):
    word = self.get_word()
    return Round(word, self.level['chances'])

  def get_word(self):
    if self.players_count == 2:
      return input("Get new word: ")
    
    file = open(f'./words/{self.language}.json')
    data = json.load(file)
    word = data[random.randrange(0,len(data))]
    file.close()
    return word


class Round:
  def __init__(self, word, chances):
    self.word = word
    self.hidden_word = re.sub('.', '*', word)
    self.correct_letters = set()
    self.wrong_letters = set()
    self.chances = chances

  def check_letter(self, letter):
    if letter in self.word:
      self.correct_letters.add(letter)
      self.hidden_word = re.sub(f"[^{''.join(self.correct_letters)}]", '*', self.word)
      return True
    else:
      self.wrong_letters.add(letter)
      self.chances -= 1;
      return False

  def check_word(self):
    return self.word == self.hidden_word

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
hangman.start_game()
