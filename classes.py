class card:
  value = None
  suit = None # naipe

class oponnent:
  name = ''
  chips = None

class data:
  def __init__(self):
    self.potSize = None
    self.roundBetSize = None
    self.flop = [card(), card(), card()]
    self.turn = None
    self.river = None
    self.playerChips = None
    self.playerCards = None
    self.buttonPos = None
    self.sb = None
    self.bb = None
    self.maxPlayers = 9
    self.ante = None
    self.opponents = None
    self.fps = None

