import time
import cv2 as cv
import mss
import numpy as np
import win32gui
import pytesseract
from stackImages import stackImages
from math import floor
from validators import *
from classes import *

pytesseract.pytesseract.tesseract_cmd = r'D:\0 - Progamas\Tesseract\tesseract.exe'
# GetForegroundWindow() pega a tela ativa
# mostra o titulo da tela GetWindowText
# mostra o tamanho da tela GetWindowRect

class window:
  left = 0
  top = 0
  right = 0
  bottom = 0
  width = 0
  height = 0

class stats:
  potValue = None
  roundBetValue = None
  ante = None
  sb = None
  bb = None
  flop = [card(), card(), card()]
  turn = card()
  river = card()
  buttonPos = None
  qntd_opponents = None

class player:
  chips = None
  cards = [card(), card()]

  def __init__(self):
    self.chips = 0
    self.cards = [card(), card()]

stats = stats()
window = window()
opponents = [oponnent(), oponnent(), oponnent(), oponnent(), oponnent(), oponnent(), oponnent(), oponnent()]
debug = False
hasAnte = False

def get_table_window(hwnd, extra):
  global window
  window_name = win32gui.GetWindowText(hwnd)

  # if not (('No Limit Hold\'em' ) in window_name or ('No Limit Hold’em') in window_name):
  if not ('No Limit Hold' in window_name):
    return
  l, t, r, b = win32gui.GetWindowRect(hwnd)
  window.left = l
  window.top = t
  window.right = r
  window.bottom = b
  window.width = r - l
  window.height = b - t
  # print("%s:" % window_name)
  # print('window:', window)

def get_monitor():
  # https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
  win32gui.EnumWindows(get_table_window, None)
  monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
  return monitor

def detect_caractere(img, shown=False, var=None):
  thisDebug = False

  if shown or thisDebug:
    cv.imshow(str(var), img)

  conf = r'--oem 2 --psm 10'
  return pytesseract.image_to_string(img, config=conf)

def detect_inline_text(img):
  conf = r'--oem 2 --psm 7'
  result = pytesseract.image_to_string(img, config=conf)

  return result

def detect_number(img):
  conf = r'--oem 2 --psm 7 outputbase digits'
  result = pytesseract.image_to_string(img, config=conf)

  return result

def get_pot(img):
  global window
  global stats

  y = int(window.height * 0.313) # quanto maior, mais pra baixo
  x = int(window.width * 0.47) # quanto maior, mais pra direita

  # [altura, largura]
  potImage = img[y:y + 26, x:x + 100]
  potValue = detect_number(potImage)
  potValue = validate_numbers_value(potValue)

  if potValue:
    try:
      int(potValue)
    except:
      # cannot read pot value
      stats.potValue = None
      return None
    else:
      stats.potValue = int(potValue)
      return int(potValue)

def get_player_chips(img, self):
  global window

  y = int(window.height * 0.737) # quanto maior, mais pra baixo
  x = int(window.width * 0.415) # quanto maior, mais pra direita

  # [altura, largura]
  chipsImage = img[y:y + 26, x:x + 110]

  self.chips = detect_number(chipsImage)

def get_player_cards(img, self):
  global window

  y = int(window.height * 0.62) # quanto maior, mais pra baixo
  x = int(window.width * 0.44) # quanto maior, mais pra direita

  # [altura, largura]
  cardsImg = img[y:y + 50, x:x + 120]

  h, w = cardsImg.shape
  #               [altura, largura]
  card1 = cardsImg[:, int(w/2/2 - 10):int(w/2)]
  card2 = cardsImg[:, int(w/2 + w/2/2 - 10):]

  cards = [card(), card()]

  get_card(card1, cards[0])
  get_card(card2, cards[1])

def get_table_bet(img):
  global window
  global stats

  y = int(window.height * 0.507) # quanto maior, mais pra baixo
  x = int(window.width * 0.46) # quanto maior, mais pra direita

  # [altura, largura]
  tableBetImage = img[y:y + 16, x:x + 100]
  
  # if roundBetValue:
  try:
    roundBetValue = detect_number(tableBetImage)
    roundBetValue = validate_numbers_value(roundBetValue)
    int(roundBetValue)
  except:
    # cannot read table bet value
    stats.roundBetValue = None
    return None
  else:
    stats.roundBetValue = int(roundBetValue)
    return int(roundBetValue)

def get_card(img, var, shown=False):
  card_suit = get_card_suit(img, shown)

  if card_suit:
    card_value = detect_caractere(improve_card_image(img, card_suit, shown), shown, var)
    card_value = validate_card_value(card_value)

    if card_value: # check if has a card
      var.value = card_value
      var.suit = card_suit
    else:
      return card()
  else:
    return card()
  
  return 1

def get_table_cards(img, shown=False):
  global window
  global stats
  y = int(window.height * 0.355) # quanto maior, mais pra baixo
  x = int(window.width * 0.336) # quanto maior, mais pra direita

  cards_image = img[y:y + int(y*0.345), x:x + int(x*0.986), :] #[altura, largura]
  h, w = cards_image.shape[:2]
  # space between cards
  space = int(w*0.015)
  space2 = int(w*0.01) 
  cards = [card(), card(), card(), card(), card()]

  if shown:
    cv.imshow('flop', cards_image)
  
  card_image = cards_image[:int(h/2), :int(w/5/2 + space), :]
  if not get_card(card_image, cards[0], False):
    cards[0] = card()
  
  card_image = cards_image[:int(h/2), int(w/5 + space2):int(w/5*1.5 + space), :]
  if not get_card(card_image, cards[1], False):
    cards[1] = card()
  
  card_image = cards_image[:int(h/2), int(w/5*2 + space2):int(w/5*2.5 + space), :]
  if not get_card(card_image, cards[2], False):
    cards[2] = card()

  card_image = cards_image[:int(h/2), int(w/5*3 + space2):int(w/5*3.5 + space), :]
  if not get_card(card_image, cards[3], False):
    cards[3] = card()

  card_image = cards_image[:int(h/2), int(w/5*4 + space2):int(w/5*4.5 + space), :]
  if not get_card(card_image, cards[4], False):
    cards[4] = card()

  return cards

def get_pixel(img, shown=False):
  # img format BGR
  # returns the pixel of the right bottom of the given image
  h, w, d = img.shape

  pixel = img[h-1, w-1]

  if shown:
    cv.imshow('detectColor', img)

  return pixel

def get_card_suit(img, shown=False):
  colors = ['diamonds', 'clubs', 'hearts', 'spades']
  if debug:
    pixel = get_pixel(img, shown=shown)
  else:
    pixel = get_pixel(img, shown=shown)[:-1]

  b, g, r = pixel

  if shown:
    print('b: ', b, 'g: ', g, 'r: ', r)

  if ((b == g) and (g == r)):
    return colors[3]

  greatest_color_idx = np.where(pixel == max(pixel))
  # print(pixel, 'idx: ', greatest_color_idx[0][0], 'len: ', len(greatest_color_idx))
  if len(greatest_color_idx) == 1:
    return colors[greatest_color_idx[0][0]]
  else:
    print('is Unknown!')
    return -1

def get_table_stats(img):
  pot = get_pot(img)
  tableBet = get_table_bet(img)
  sb, bb = get_blinds(img)

  if hasAnte:
    ante = get_ante(img)
  else:
    ante = None

def get_button_pos(img):
  global window
  w = window.width
  h = window.height

  y = int(h * 0.5) # quanto maior, mais pra baixo
  x = int(w * 0.24) # quanto maior, mais pra direita
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 1

  y = int(h * 0.37) 
  x = int(w * 0.18) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 2

  y = int(h * 0.28) 
  x = int(w * 0.29) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 3
  
  y = int(h * 0.22) 
  x = int(w * 0.4455) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 4
  
  y = int(h * 0.245) 
  x = int(w * 0.64) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 5

  y = int(h * 0.315) 
  x = int(w * 0.743) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 6
  
  y = int(h * 0.5) 
  x = int(w * 0.774) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 7
  
  y = int(h * 0.57) 
  x = int(w * 0.66) 
  buttonImg = img[y:y + int(h*0.05), x:x + int(w*0.05)]

  if is_button(buttonImg):
    return 8

  return None

def get_opponents(img):
  global window
  w = window.width
  h = window.height
  qntd_opponents = 0

  y = int(window.height * 0.615) # quanto maior, mais pra baixo
  x = int(window.width * 0.12) # quanto maior, mais pra direita
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 0):
    qntd_opponents += 1

  y = int(window.height * 0.418) 
  x = int(window.width * 0.02) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 1):
    qntd_opponents += 1

  y = int(window.height * 0.23) 
  x = int(window.width * 0.06) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 2):
    qntd_opponents += 1

  y = int(window.height * 0.14) 
  x = int(window.width * 0.246) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 3):
    qntd_opponents += 1

  y = int(window.height * 0.14) 
  x = int(window.width * 0.633) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 4):
    qntd_opponents += 1

  y = int(window.height * 0.23) 
  x = int(window.width * 0.815) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 5):
    qntd_opponents += 1
  
  y = int(window.height * 0.418) 
  x = int(window.width * 0.855) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 6):
    qntd_opponents += 1
  
  y = int(window.height * 0.615) 
  x = int(window.width * 0.76) 
  opContainer = img[y:y + int(h*0.078), x:x + int(w*0.125)]
  if is_opponent(opContainer, 7):
    qntd_opponents += 1

  return qntd_opponents

def get_ante(img):
  global window
  global stats

  w = window.width
  h = window.height
  y = int(h * 0.12) 
  x = int(w * 0.97) 
  anteImg = img[y:y + int(h*0.038), x:w]

  try: 
    ante = detect_number(anteImg)
    int(ante)
  except:
    # cannot read table bet value
    stats.ante = None
    return None
  else:
    stats.ante = int(ante)
    return int(ante)

def get_blinds(img):
  global window
  global stats

  w = window.width
  h = window.height

  if not hasAnte:
    y = int(h * 0.12) 
    x = int(w * 0.953) 
    blindsImg = img[y:y + int(h*0.038), x:w]
  else:
    y = int(h * 0.12) 
    x = int(w * 0.9) 
    blindsImg = img[y:y + int(h*0.038), x:x + int(w*0.07)]

  try: 
    blinds = detect_number(blindsImg)
    # detect_number(16/32) gives -> 16132 then remove '1' -> 1632
    small_blind = blinds[:floor(len(blinds)/2)]
    int(small_blind)
  except:
    # cannot read table bet value
    stats.sb = None
    stats.bb = None
    return None, None
  else:
    stats.sb = int(small_blind)
    stats.bb = int(small_blind)*2
    return int(small_blind), int(small_blind)*2

def is_button(img):
  img = cv.Canny(img, 50, 50)
  # pega as formas na imagem
  countours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  if not countours:
    return False

  for cnt in countours:
    # area da forma
    area = cv.contourArea(cnt)

    if area > 400:
      # perimetro da forma
      perimeter = cv.arcLength(cnt, True)
      approx = cv.approxPolyDP(cnt, 0.02*perimeter, True)
      # quantidade de pontas da forma; 3 == triangulo, 4 == retangulo/quadrado, etc...
      objCorners = len(approx)
      if objCorners > 4: 
        return True 
      else: 
        return False

def is_opponent(img, idx):
  h = img.shape[0]
  name = img[0: int(h/2), :]
  name = detect_inline_text(name)

  if(len(name) > 0):
    chips = img[int(h/2):, :]
    chips = detect_number(chips)
    opponents[idx].name = name
    opponents[idx].chips = chips
    return True
  
  return False

def improve_image(image, invert=True, blur=False):
  # source: https://stackoverflow.com/questions/54497882/how-improve-image-quality-to-extract-text-from-image-using-tesseract
  # help https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/
  # create grayscale
  result = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

  # perform threshold
  # se o valor for maior q 160 fica preto, senao, branco
  retr, mask = cv.threshold(result, 160, 255, cv.THRESH_BINARY)
  result = mask
  if blur:
    result = cv.medianBlur(result, 3)
    # result = cv.GaussianBlur(result,(3,3), 0)

  #invert to get black text on white background
  if invert:
    result = cv.bitwise_not(result)
  else:
    return result

  # aumenta a imagem
  #result = cv.resize(result, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
  
  return result

def improve_card_image(img, suit, shown=False):
  # convert to grayscale

  result = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  if shown:
    print('suit: ', suit)

  if suit == 'hearts':
    retr, result = cv.threshold(result, 220, 255, cv.THRESH_BINARY)
    result = cv.medianBlur(result, 3)
    # invert to get black text on white background
    result = cv.bitwise_not(result)
    if shown:
      cv.imshow('improvedCardImageHearts', result)
    return result
  elif suit == 'clubs':
    retr, result = cv.threshold(result, 220, 255, cv.THRESH_BINARY)
    result = cv.medianBlur(result, 3)
    # invert to get black text on white background
    result = cv.bitwise_not(result)
    if shown:
      cv.imshow('improvedCardImageClubs', result)
    return result
  elif suit == 'diamonds':
    retr, result = cv.threshold(result, 220, 255, cv.THRESH_BINARY)
    result = cv.medianBlur(result, 3)
    # invert to get black text on white background
    result = cv.bitwise_not(result)
    if shown:
      cv.imshow('improvedCardImageDiamonds', result)
    return result
  elif suit == 'spades':
    retr, result = cv.threshold(result, 210, 255, cv.THRESH_BINARY)
    result = cv.medianBlur(result, 3)
    # invert to get black text on white background
    result = cv.bitwise_not(result)
    if shown:
      cv.imshow('improvedCardImageSpades', result)
    return result
  else:
    return -1

def status_screen(fps):
  global stats

  screen = np.zeros((512, 512, 3), np.uint8)
  stats_list = {'    STATUS EM TEMPO REAL    ': str(fps), '':'', 
  'potValue: ': str(stats.potValue),
  'roundBetValue: ': str(stats.roundBetValue),
  'flop: ': str(stats.flop[0].value) + '['+str(stats.flop[0].suit)+'] ' + str(stats.flop[1].value) + '['+str(stats.flop[1].suit)+'] ' + str(stats.flop[2].value) + '['+str(stats.flop[2].suit)+'] ',
  'turn: ': str(stats.turn.value) + '['+str(stats.turn.suit)+'] ',
  'river: ': str(stats.river.value) + '['+str(stats.river.suit)+'] ',
  'Player chips: ': str(player.chips),
  'Player cards: ': str(player.cards[0].value) + ' ' + str(player.cards[1].value),
  'Button pos: ': str(stats.buttonPos),
  'total opponents: ': str(stats.qntd_opponents),
  'small blind/big blind: ': str(stats.sb) + '/' + str(stats.bb)
  }
  padding = 25
  for key, value in stats_list.items():
    text = str(key) + str(value)
    cv.putText(screen, text, (2, padding), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 256), 1)
    padding += 38

  cv.namedWindow('Status', cv.WINDOW_NORMAL)
  cv.imshow('Status', screen)

def get_one_image(images): # junta as img, ta dando erro pq potImage so é 2D
  #img_list = []
  img_list = images
  padding = 200
  # for img in img_list:
    #img_list.append(cv.imread(img, 1))
  max_width = []
  max_height = 0
  for img in img_list:
    max_width.append(img.shape[0])
    max_height += img.shape[1]
  w = np.max(max_width)
  h = max_height + padding

  # create a new array with a size large enough to contain all the images
  final_image = np.zeros((h, w), dtype=np.uint8)

  current_y = 0  # keep track of where your current image was last placed in the y coordinate
  for image in img_list:
    # add an image to the final array and increment the y coordinate
    final_image[current_y:image.shape[0] + current_y, : image.shape[1]] = image
    current_y += image.shape[0]

  return final_image  
# https://python-mss.readthedocs.io/examples.html
def capture_screen():
  with mss.mss() as sct:
    if not debug:
      monitor = get_monitor()
      img = np.array(sct.grab(monitor))
    else:
      global window
      img = cv.imread('./images/error7.png')
      window.left = 0
      window.top = 0
      window.right = 955
      window.bottom = 689
      window.width = 955
      window.height = 689
  
  return img

def get_data(data):
  last_time = time.time()
  img = capture_screen()
  improvedImage = improve_image(img)
  
  data.potSize = get_pot(improvedImage)
  data.roundBetSize = get_table_bet(improvedImage)
  data.ante = get_ante(improvedImage)
  cards = get_table_cards(img)
  data.flop = cards[:3]
  data.turn = cards[3]
  data.river = cards[4]
  # data.playerChips = get_player_chips(improvedImage)
  # data.playerCards = get_player_cards(improvedImage)
  data.buttonPos = get_button_pos(improvedImage)
  data.sb, data.bb = get_blinds(improvedImage)
  data.opponents = get_opponents(improvedImage)
  data.fps = "{: .2f}".format(1 / (time.time() - last_time))

if __name__ == "__main__":
  cont = 5
  print('iniciando read_info')
  while "Screen capturing":
    last_time = time.time()
    img = capture_screen()

    improvedImage = improve_image(img)

    get_table_stats(improvedImage)
    # get_table_cards(img, False)
    """ if cont == 5:
      getOpponents(improvedImage)
      cont = 0
    stats.buttonPos = getButtonPos(improvedImage)
    player.getPlayerStats(improvedImage, player)
    player.getPlayerCards(improveImage(img, False), player) """
    # status_screen("FPS: {: .2f}".format(1 / (time.time() - last_time)))

    # cv.namedWindow("Screen", cv.WINDOW_NORMAL)
    # cv.imshow("Screen", img)
    cont += 1
    # Press "q" to quit
    if cv.waitKey(25) & 0xFF == ord("q"):
      cv.destroyAllWindows()
      break