from tkinter import Tk
from interface import Interface

class data:
  def __init__(self):
    self.potSize = None
    self.roundBetSize = None
    self.flop = None
    self.turn = None
    self.river = None
    self.playerChips = None
    self.playerCards = None
    self.buttonPos = None
    self.sb = None
    self.bb = None
    self.maxPlayers = None
    self.ante = None
    self.opponents = None

interface_is_running = True

def close_interface():
  global interface_is_running

  interface_is_running = False

def start_interface():
  root = Tk()
  Interface(root)
  root.title("Python Play's Poker!")
  root.protocol("WM_DELETE_WINDOW", close_interface)

  return root

if __name__ == "__main__":
  interface = start_interface()
  data = data()
  var = 0
  print('will run')
  
  while interface_is_running:
    interface.update_idletasks()
    interface.update()
    print(var)
    var += 1

