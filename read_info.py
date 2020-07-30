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

debug = False
hasAnte = True

def get_table_window(hwnd, monitor):
  window_name = win32gui.GetWindowText(hwnd)

  # if not (('No Limit Hold\'em' ) in window_name or ('No Limit Hold’em') in window_name):
  if not ('Hold' in window_name):
    return
  l, t, r, b = win32gui.GetWindowRect(hwnd)
  monitor["left"] = l
  monitor["top"] = t
  monitor["right"] = r
  monitor["bottom"] = b
  monitor["width"] = r - l
  monitor["height"] = b - t
  # print("%s:" % window_name)
  # print('window:', window.left, window.top)

def get_monitor(data):
  # https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
  monitor = {"top": 0, "left": 0, "width": 0, "height": 0}
  win32gui.EnumWindows(get_table_window, monitor)
  data.window.left = monitor["left"]
  data.window.top = monitor["top"]
  data.window.right = monitor["right"]
  data.window.bottom = monitor["bottom"]
  data.window.width = monitor["width"]
  data.window.height = monitor["height"]
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

def detect_number(img, shown=False):
  if shown:
    cv.imshow('detect number: ', img)

  conf = r'--oem 2 --psm 7 outputbase digits'
  result = pytesseract.image_to_string(img, config=conf)

  return result

def get_pot(img, data, shown=False):
  y = int(data.window.height * 0.313) # quanto maior, mais pra baixo
  x = int(data.window.width * 0.44) # quanto maior, mais pra direita

  # [altura, largura]
  potImage = img[y:y + int(y*0.13), x:x + int(x*0.3)]
  
  if shown:
    cv.imshow('pot', potImage)

  potValue = detect_number(potImage)
  potValue = validate_numbers_value(potValue)

  if potValue:
    try:
      int(potValue)
    except:
      # cannot read pot value
      return None
    else:
      return int(potValue)

def get_player_chips(img, data, shown=False):
  y = int(data.window.height * 0.737) # quanto maior, mais pra baixo
  x = int(data.window.width * 0.415) # quanto maior, mais pra direita
  marginError = int(x*0.05)

  # [altura, largura]
  chipsImage = img[y:y + int(y*0.08), x:x + int(x*0.4)]

  if shown:
    cv.imshow('Player Chips Image', chipsImage)

  return validate_numbers_value(detect_number(chipsImage))

def get_player_cards(img, data, shown=False):
  y = int(data.window.height * 0.64) # quanto maior, mais pra baixo
  x = int(data.window.width * 0.438) # quanto maior, mais pra direita
  marginError = int(x*0.02)
  #             [altura, largura]
  cardsImg = img[y:y + int(y*0.08), x:x + int(x*0.28)]
  h, w = cardsImg.shape[:2]
  
  if shown:
    cv.imshow('Player Cards', cardsImg)

  card1 = cardsImg[:, :int(w/2/2) + marginError, :]
  card2 = cardsImg[:, int(w/2):int(w/2 + w/2/2) + marginError, :]
  cards = [card(), card()]

  get_card(card1, cards[0], False)
  get_card(card2, cards[1], False)

  return cards

def get_table_bet(img, data):
  y = int(data.window.height * 0.507) # quanto maior, mais pra baixo
  x = int(data.window.width * 0.46) # quanto maior, mais pra direita

  # [altura, largura]
  tableBetImage = img[y:y + 16, x:x + 100]
  
  # if roundBetValue:
  try:
    roundBetValue = detect_number(tableBetImage)
    roundBetValue = validate_numbers_value(roundBetValue)
    int(roundBetValue)
  except:
    # cannot read table bet value
    return None
  else:
    return int(roundBetValue)

def get_card(img, var, shown=False):
  card_suit = get_card_suit(img, shown)

  if card_suit:
    card_value = detect_caractere(improve_card_image(img, card_suit, shown), False, var)
    if shown:
      print('card value: ', card_value)
    card_value = validate_card_value(card_value)


    if card_value: # check if has a card
      var.value = card_value
      var.suit = card_suit
    else:
      # print('card value invalid: ', card_value)
      return False
  else:
    # print('card suit invalid: ', card_value)
    return False
  
  return 1

def get_table_cards(img, data, try_load_flop=False, try_load_turn=False, try_load_river=False, shown=False):
  y = int(data.window.height * 0.355) # quanto maior, mais pra baixo
  x = int(data.window.width * 0.336) # quanto maior, mais pra direita

  cards_image = img[y:y + int(y*0.345), x:x + int(x*0.986), :] #[altura, largura]
  h, w = cards_image.shape[:2]
  # space between cards
  space = int(w*0.015)
  space2 = int(w*0.01) 
  cards = [card(), card(), card()]

  if shown:
    cv.imshow('flop', cards_image)
  
  if try_load_flop:
    card_image = cards_image[:int(h/2), :int(w/5/2 + space), :]
    if not get_card(card_image, cards[0], False):
      # cards[0] = card()
      return cards
    
    card_image = cards_image[:int(h/2), int(w/5 + space2):int(w/5*1.5 + space), :]
    if not get_card(card_image, cards[1], False):
      # cards[1] = card()
      return cards
    
    card_image = cards_image[:int(h/2), int(w/5*2 + space2):int(w/5*2.5 + space), :]
    if not get_card(card_image, cards[2], False):
      # cards[2] = card()
      return cards

    return cards

  if try_load_turn:
    card_image = cards_image[:int(h/2), int(w/5*3 + space2):int(w/5*3.5 + space), :]
    turn = card()
    get_card(card_image, turn, False)

    return turn

  if try_load_river:
    card_image = cards_image[:int(h/2), int(w/5*4 + space2):int(w/5*4.5 + space), :]
    river = card()
    get_card(card_image, river, False)

    return river

def get_pixel(img, shown=False):
  # img format BGR
  # returns the pixel of the right bottom of the given image
  h, w, d = img.shape

  pixel = img[h-1, w-1]

  if shown:
    cv.imshow('get_pixel', img)

  return pixel

def get_card_suit(img, shown=False):
  colors = ['diamonds', 'clubs', 'hearts', 'spades']
  if debug:
    pixel = get_pixel(img, shown=shown)
  else:
    pixel = get_pixel(img, shown=shown)[:-1]

  b, g, r = pixel

  if not is_colorful(pixel):
    return colors[3]

  greatest_color_idx = np.where(pixel == max(pixel))
  # print(pixel, 'idx: ', greatest_color_idx[0][0], 'len: ', len(greatest_color_idx))
  if len(greatest_color_idx) == 1:
    return colors[greatest_color_idx[0][0]]
  else:
    print('is Unknown!')
    return -1

def get_button_pos(img, data):
  w = data.window.width
  h = data.window.height

  y = int(h * 0.5) # quanto maior, mais pra baixo
  x = int(w * 0.24) # quanto maior, mais pra direita
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 1):
    return 1

  y = int(h * 0.366) 
  x = int(w * 0.18) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 2):
    return 2

  y = int(h * 0.28) 
  x = int(w * 0.29) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 3):
    return 3

  y = int(h * 0.22) 
  x = int(w * 0.4455) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 4):
    return 4

  y = int(h * 0.245) 
  x = int(w * 0.64) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 5):
    return 5

  y = int(h * 0.315) 
  x = int(w * 0.743) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 6):
    return 6

  y = int(h * 0.5) 
  x = int(w * 0.774) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 7):
    return 7
  
  y = int(h * 0.57) 
  x = int(w * 0.66) 
  buttonImg = img[y:y + int(h*0.02), x:x + int(w*0.02)]

  if is_button(buttonImg, False, 8):
    return 8

  return 0

def get_opponents(img, data):
  w = data.window.width
  h = data.window.height
  qntd_opponents = 0
  # print('getting qntd opponents')

  y = int(h * 0.58) # quanto maior, mais pra baixo
  x = int(w * 0.17) # quanto maior, mais pra direita
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 1, False):
    data.opponents[0] = True
    qntd_opponents += 1

  y = int(h * 0.39) 
  x = int(w * 0.07) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 2, False):
    data.opponents[1] = True
    qntd_opponents += 1

  y = int(h * 0.2) 
  x = int(w * 0.1) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 3, False):
    data.opponents[2] = True
    qntd_opponents += 1

  y = int(h * 0.11) 
  x = int(w * 0.28) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 4, False):
    data.opponents[3] = True
    qntd_opponents += 1

  y = int(h * 0.11) 
  x = int(w * 0.63) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 5, False):
    data.opponents[4] = True
    qntd_opponents += 1

  y = int(h * 0.2) 
  x = int(w * 0.81) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 6, False):
    data.opponents[5] = True
    qntd_opponents += 1

  y = int(h * 0.39) 
  x = int(w * 0.85) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 7, False):
    data.opponents[6] = True
    qntd_opponents += 1

  y = int(h * 0.58) 
  x = int(w * 0.76) 
  opContainer = img[y:y + int(h*0.02), x:x + int(w*0.02)]
  if is_opponent(opContainer, 8, False):
    data.opponents[7] = True
    qntd_opponents += 1

  return qntd_opponents

def get_ante(img, data):
  w = data.window.width
  h = data.window.height
  y = int(h * 0.12) 
  x = int(w * 0.97) 
  anteImg = img[y:y + int(h*0.038), x:w]

  try: 
    ante = detect_number(anteImg)
    int(ante)
  except:
    # cannot read table bet value
    return None
  else:
    return int(ante)

def get_blinds(img, hasAnte, shown, data):
  w = data.window.width
  h = data.window.height

  if not hasAnte:
    y = int(h * 0.12) 
    x = int(w * 0.92) 
    blindsImg = img[y:y + int(h*0.038), x:w]
  else:
    y = int(h * 0.12) 
    x = int(w * 0.89) 
    blindsImg = img[y:y + int(h*0.038), x:x + int(w*0.07)]
  if shown:
    cv.imshow('blinds', blindsImg)
  try: 
    blinds = detect_number(blindsImg, False)
    # detect_number(16/32) gives -> 16132 then remove '1' -> 1632
    small_blind = blinds[:floor(len(blinds)/2)]
    int(small_blind)
  except:
    # cannot read table bet value
    return None, None
  else:
    return int(small_blind), int(small_blind)*2

def get_state(img, data, shown=False):
  # 0 cant play yet
  # 1 check or raise
  # 2 fold or call or raise
  # 3 fold or call
  w = data.window.width
  h = data.window.height

  y = int(h * 0.9) # quanto maior, mais pra baixo
  x = int(w * 0.5) # quanto maior, mais pra direita
  buttons = img[y:h - int(h*0.02), x:w]
  wid = buttons.shape[1]
  # check if can fold
  if debug:
    pixel = buttons[20, 20]
  else:
    pixel = buttons[20, 20][:-1]
  if is_colorful(pixel):
    # it can fold
    btn2 = buttons[:, int(wid/3):int(wid/3*2)]
    if debug:
      pixel = btn2[20, 20]
    else:
      pixel = btn2[20, 20][:-1]
    if is_colorful(pixel):
      # it can raises too -> 2
      print('can fold or call or raise')
      return 2
    else:
      # cant call, raise or has to go all in -> 3
      print('can fold or go all in')
      return 3
  else:
    # check if can check
    btn2 = buttons[:, int(wid/3):int(wid/3*2)]

    if debug:
      pixel = btn2[20, 20]
    else:
      pixel = btn2[20, 20][:-1]

    if is_colorful(pixel):
      # it can check, wich means that it can raises too -> 1
      print('can check or bet')
      return 1
    else:
      return 0
  if shown:
    cv.imshow('state', buttons)

def is_button(img, shown=False, idx=None):
  if debug:
    pixel = get_pixel(img, shown=shown)
  else:
    pixel = get_pixel(img, shown=shown)[:-1]

  if shown:
    print(pixel, 'idx: ', idx)

  if is_colorful(pixel, False):
    return True
  else:
    return False

def is_opponent(img, idx, shown=False):
  result = False
  if debug:
    pixel = get_pixel(img)
  else:
    pixel = get_pixel(img)[:-1]

  if is_colorful(pixel, False):
    result = True
  else:
    result = False

  if shown:
    cv.imshow('Opponent ' + str(idx), img)
    print(b, g, r, 'idx: ', idx, result)
  
  return result

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

def is_colorful(pixel, shown=False):
  if debug:
    b, g, r = pixel
  else:
    b, g, r = pixel

  if not(b == g and g == r):
    # is colorful
    return True
  else:
    return False

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
  # not working, class stats removed
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

# https://python-mss.readthedocs.io/examples.html
def capture_screen(data):
  with mss.mss() as sct:
    last_tm = time.time()
    if not debug:
      monitor = get_monitor(data)
      img = np.array(sct.grab(monitor))
      # print('screens p/s: {: 2.f}'.format(1/(time.time() - last_tm)))
    else:
      img = cv.imread('./images/error.png')
      data.window.left = 0
      data.window.top = 0
      data.window.right = 955
      data.window.bottom = 689
      data.window.width = 955
      data.window.height = 689
  
  return img

def get_cards(data, img):
  # se nenhuma carta for valida no array de cartas do player
  if any(not card.isLoaded() for card in data.playerCards):
    # did not recieved cards
    data.playerCards = get_player_cards(img, data, shown=False)
    
    if (data.playerCards[0].isLoaded()):
      print('Player cards loaded')

  if data.round < 1 and any(not card.isLoaded() for card in data.flop):
    print('loading flop')
    data.flop = get_table_cards(img, data, try_load_flop=True)
    # se todas carta forem validas no array do flop
    if all(card.isLoaded() for card in data.flop):
      # if flop was loaded with sucess
      print('flop loaded')

      if data.round < 1:
        data.hasPlayed = False
        data.round = 1

  if data.round < 2 and not data.turn.isLoaded() and (all(card.isLoaded() for card in data.flop)):
    data.turn = get_table_cards(img, data, try_load_turn=True)

    if data.turn.isLoaded():
      print('turn loaded')

      if data.round < 2:
        data.hasPlayed = False
        data.round = 2

  if data.round < 3 and data.turn.isLoaded() and not data.river.isLoaded():
    data.river = get_table_cards(img, data, try_load_river=True)

    if data.river.isLoaded():
      print('river loaded')
      if data.round < 3:
        data.hasPlayed = False
        data.round = 3

def reset_varaibles(data):
  print('reseting')
  data.round = 0
  data.flop = [card(), card(), card()]
  data.turn = card()
  data.river = card()
  data.playerCards = [card(), card()]
  data.playerChips = None
  data.sb, data.bb = [None, None]
  data.ante = None
  data.buttonPos = None
  data.qntdOpponents = None
  data.opponents = [None, None, None, None, None, None, None, None]
  data.hasPlayed = False
  data.stillPlaying = True
  data.state = 0

def retrieve_data(data):
  # data.round
  # -1 = break or network error
  # 0 = initial bets
  # 1 = flop
  # 2 = turn
  # 3 = river
  last_time = time.time()
  img = capture_screen(data)
  improvedImage = improve_image(img)
  data.potSize = get_pot(improvedImage, data, shown=False)

  if not data.potSize:
    # if doesnt have pot, probabyly is animating from an ending round or in an interval
    data.fps = "{: .2f}".format(1 / (time.time() - last_time))
    return -1

  if not data.lastPotSize:
    # initialize lastPotSize
    data.lastPotSize = data.potSize + 1

  if data.potSize < data.lastPotSize:
    # table reseted -> reset variables
    print('potSize: {} <? lastPotSize: {}'.format(data.potSize, data.lastPotSize))
    reset_varaibles(data)
  else:
    # table still going
    pass

  if not data.stillPlaying:
    data.fps = "{: .2f}".format(1 / (time.time() - last_time))
    return -1

  data.lastPotSize = data.potSize
  data.roundBetSize = get_table_bet(improvedImage, data)
  data.state = get_state(img, data, shown=False)
  get_cards(data, img)
  
  if not data.playerChips:
    data.playerChips = get_player_chips(improvedImage, data, shown=False)
  
  if not data.sb:
    data.sb, data.bb = get_blinds(improvedImage, data.hasAnte, True, data)

  if not data.ante and data.hasAnte:
    data.ante = get_ante(improvedImage, data)
  
  if not data.buttonPos:
    data.buttonPos = get_button_pos(img, data)

  data.qntdOpponents = get_opponents(img, data)
  data.fps = "{: .2f}".format(1 / (time.time() - last_time))

if __name__ == "__main__":
  print('iniciando read_info')
  while "Screen capturing":
    last_time = time.time()
    img = capture_screen(data)
    improvedImage = improve_image(img)

    get_state(img, True)

    # Press "q" to quit
    if cv.waitKey(25) & 0xFF == ord("q"):
      cv.destroyAllWindows()
      break