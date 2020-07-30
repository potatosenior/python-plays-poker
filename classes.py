class card:
  value = None
  suit = None # naipe

  def isLoaded(self):
    # print('-- ', self.value)
    return self.value

class window:
  left = 0
  top = 0
  right = 0
  bottom = 0
  width = 0
  height = 0
class oponnent:
  name = None
  chips = None

class data:
  def __init__(self):
    # table config
    self.fps = None
    self.hasAnte = True
    self.maxPlayers = 9
    self.window = window()
    # round values
    self.potSize = None
    self.lastPotSize = None
    self.roundBetSize = None
    self.flop = [card(), card(), card()]
    self.turn = card()
    self.river = card()
    self.playerChips = None
    self.playerCards = [card(), card()]
    self.buttonPos = None
    self.sb = None
    self.bb = None
    self.ante = None
    self.opponents = [None, None, None, None, None, None, None, None]
    self.qntdOpponents = None
    # round checks
    self.state = 0
    self.round = 0
    self.stillPlaying = True
    self.hasPlayed = False

