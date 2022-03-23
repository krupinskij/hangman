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
  'reset': '\033[0m',
  'black': '\033[30m',
  "red":'\033[31m',
  "green":'\033[32m',
  "orange":'\033[33m',
  "blue":'\033[34m',
  "purple":'\033[35m',
  "cyan":'\033[36m',
  "lightgrey":'\033[37m',
  "darkgrey":'\033[90m',
  "lightred":'\033[91m',
  "lightgreen":'\033[92m',
  "yellow":'\033[93m',
  "lightblue":'\033[94m',
  "pink":'\033[95m',
  "lightcyan":'\033[96m'
}


class Game:
  def __init__(self, players_count):
    self.players_count = players_count

  def _play(self):
    clear_console()
    print(f"{colors['yellow']}Game started...{colors['reset']}")
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

      print(f"{colors['yellow']}New round started...{colors['reset']}")
      print()

      while True:
        print(f"{colors['yellow']}Hidden word is: {colors['reset']}{round.hidden_word}")
        if len(round.wrong_letters) > 0 and self.level == levels["beginner"]:
          print(f"{colors['yellow']}Letters: {colors['reset']}{', '.join(round.wrong_letters)} {colors['yellow']}are wrong{colors['reset']}")
        print(f"{colors['yellow']}You have: {colors['reset']}{round.chances} {colors['yellow']}chance(s){colors['reset']}")
        letter = self.get_letter()
        
        if round.check_letter(letter):
          print(f"{colors['yellow']}Nice! Letter {colors['reset']}\"{letter}\" {colors['yellow']}is in the word!{colors['reset']}")
          print()

          if round.check_word():
            print(f"{colors['green']}Congratulations!{colors['reset']}")
            print(f"{colors['green']}You guessed word: {colors['reset']}\"{round.word}\"{colors['green']}!{colors['reset']}")

            break
        else:
          print(f"{colors['red']}Ouch! Letter {colors['reset']}\"{letter}\" {colors['red']}isn't in the word!{colors['reset']}")
          print()

          if round.chances == 0:
            print(f"{colors['red']}I'm sorry! You've lost. The hidden word was {colors['reset']}\"{round.word}\"")
            break

      print()
      print(f"{colors['yellow']}Wanna play next round?{colors['reset']}")
      next = input(f"{colors['yellow']}Type {colors['reset']}\"no\" {colors['yellow']}to end the game or something else to continue: {colors['reset']}")
      if next == "no":
        print(f"{colors['yellow']}Bye!{colors['reset']}")
        break
      else:
        clear_console()

  def start_round(self):
    word = self.get_word()
    return Round(word, self.level['chances'])

  def get_letter(self):
    letter = ''

    while True:
      letter = input(f"{colors['green']}Get new letter: {colors['reset']}")

      if check_letter(letter):
        return letter
      else:
        print(f"{letter} {colors['red']}is not a letter! Try again!{colors['reset']}")

  def get_word(self):
    if self.players_count == 2:
      word = ''
      while True:
        word = input(f"{colors['green']}Get new word: {colors['reset']}")
        if check_word(word):
          clear_console()
          return word
        else:
          print(f"{colors['red']}It is not a valid word! Try again!{colors['reset']}")
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

print(colors["cyan"])
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
    option = input(f"{colors['green']}Select {options_name}{colors['reset']} ({', '.join(list(options_dict.keys()))}): ").lower()
    if option in options_dict:
      break
    else:
      print(f"{colors['red']}Option {colors['reset']}\"{option}\" {colors['red']}is not available! Try again!{colors['reset']}")

  print(f"{colors['yellow']}Selected {colors['reset']}\"{option}\"")
  print()
  return option;

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def check_letter(letter):
  return len(letter) == 1 and letter.isalpha()

def check_word(word):
  return len(word) >= 5 and word.isalpha()


mode_input = select_option(mode, "mode")
levels_input = select_option(levels, "level")
languages_input = select_option(languages, "language")

hangman = Hangman(mode[mode_input], levels[levels_input], languages[languages_input])
hangman.start_game()
