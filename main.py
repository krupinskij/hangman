import json
import re
import random
import os

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

colors = {
  "user":'\033[36m',
  "info":'\033[93m',
  "success": '\033[32m',
  "error": '\033[31m',
  'reset': '\033[0m',
  # 'black': '\033[30m',
  # "error":'\033[31m',
  # "success":'\033[32m',
  # "orange":'\033[33m',
  # "user":'\033[34m',
  # "purple":'\033[35m',
  # "user":'\033[36m',
  # "lightgrey":'\033[37m',
  # "darkgrey":'\033[90m',
  # "lighterror":'\033[91m',
  # "lightsuccess":'\033[92m',
  # "yellow":'\033[93m',
  # "lightuser":'\033[94m',
  # "pink":'\033[95m',
  # "lightuser":'\033[96m'
}


class Game:
  def __init__(self, players_count):
    self.players_count = players_count

  def _play(self):
    clear_console()
    print(f"{colors['info']}Game started...{colors['reset']}")
    print()


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
      round = self.start_round()

      print(f"{colors['info']}New round started...{colors['reset']}")
      print()

      while True:
        print(f"{colors['info']}Hidden word is: {colors['reset']}{round.hidden_word}")
        if len(round.wrong_letters) > 0 and self.level == levels["beginner"]:
          print(f"{colors['info']}Letters: {colors['reset']}{', '.join(round.wrong_letters)} {colors['info']}are wrong{colors['reset']}")
        print(f"{colors['info']}You have: {colors['reset']}{round.chances} {colors['info']}chance(s){colors['reset']}")
        letter = self.get_letter()
        
        if round.check_letter(letter):
          print(f"{colors['success']}Nice! Letter {colors['reset']}\"{letter}\" {colors['success']}is in the word!{colors['reset']}")
          print()

          if round.check_word():
            print(f"{colors['success']}Congratulations!{colors['reset']}")
            print(f"{colors['success']}You guessed word: {colors['reset']}\"{round.word}\"{colors['success']}!{colors['reset']}")

            break
        else:
          print(f"{colors['error']}Ouch! Letter {colors['reset']}\"{letter}\" {colors['error']}isn't in the word!{colors['reset']}")
          print()

          if round.chances == 0:
            print(f"{colors['error']}I'm sorry! You've lost. The hidden word was {colors['reset']}\"{round.word}\"")
            break

      print()
      print(f"{colors['user']}Wanna play next round?{colors['reset']}")
      next = input(f"{colors['user']}Type {colors['reset']}\"no\" {colors['user']}to end the game or something else to continue: {colors['reset']}")
      if next == "no":
        print(f"{colors['user']}Bye!{colors['reset']}")
        break
      else:
        clear_console()

  def start_round(self):
    word = self.get_word()
    return Round(word, self.level['chances'])

  def get_letter(self):
    letter = ''

    while True:
      letter = input(f"{colors['user']}Get new letter: {colors['reset']}")

      if check_letter(letter):
        return letter
      else:
        print(f"{letter} {colors['error']}is not a letter! Try again!{colors['reset']}")

  def get_word(self):
    if self.players_count == 2:
      word = ''
      while True:
        word = input(f"{colors['user']}Get new word: {colors['reset']}")
        if check_word(word):
          clear_console()
          return word
        else:
          print(f"{colors['error']}It is not a valid word! Try again!{colors['reset']}")
          print()
    
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

print(colors["user"])
print("###    ###      #####      ####     ###    ########   ###         ###      #####      ####     ###")
print("###    ###     #######     ######   ###   ###    ###  ####       ####     #######     ######   ###")
print("##########    ###   ###    ### ###  ###  ###          #####     #####    ###   ###    ### ###  ###")
print("##########   ###########   ###  ### ###  ###    ####  ######   ######   ###########   ###  ### ###")
print("###    ###  ###       ###  ###   ######   ###    ###  ### ####### ###  ###       ###  ###   ######")
print("###    ###  ###       ###  ###     ####    ########   ###  #####  ###  ###       ###  ###     ####")
print(colors["reset"])

def select_option(options_dict, options_name):
  option = ""
  while option not in options_dict:
    option = input(f"{colors['user']}Select {options_name}{colors['reset']} ({', '.join(list(options_dict.keys()))}): ").lower()
    if option in options_dict:
      break
    else:
      print(f"{colors['error']}Option {colors['reset']}\"{option}\" {colors['error']}is not available! Try again!{colors['reset']}")

  print(f"{colors['info']}Selected {colors['reset']}\"{option}\"")
  print()
  return option;

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def check_letter(letter):
  return len(letter) == 1 and letter.isalpha()

def check_word(word):
  return len(word) >= 5 and word.isalpha()


mode_input = select_option(mode, "mode")
levels_input = select_option(levels, "level")
if mode_input == mode["single"]:
  languages_input = select_option(languages, "language")
else:
  languages_input = "english"

hangman = Hangman(mode[mode_input], levels[levels_input], languages[languages_input])
hangman.start_game()
