import time
import cv2 as cv
import mss
import numpy as np
import win32gui
import pytesseract
from stackImages import stackImages

pytesseract.pytesseract.tesseract_cmd = r'D:\\0 - Progamas\\Tesseract\\tesseract.exe'
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

class card:
  value = ''
  suit = '' # naipe

class stats:
  potValue = 0
  roundBetValue = 0
  flop = [card(), card(), card()]
  turn = card()
  river = card()

class player:
  chips = 0
  cards = [card(), card()]

  def __init__(self):
    self.chips = 0
    self.cards = [card(), card()]
  
  def getPlayerStats(img, self):
    global window

    y = int(window.height * 0.737) # quanto maior, mais pra baixo
    x = int(window.width * 0.415) # quanto maior, mais pra direita

    # [altura, largura]
    chipsImage = img[y:y + 26, x:x + 110]

    self.chips = detectNumber(chipsImage)
    
    # cv.imshow("Chips", chipsImage)
  
  def getPlayerCards(img, self):
    global window

    y = int(window.height * 0.62) # quanto maior, mais pra baixo
    x = int(window.width * 0.44) # quanto maior, mais pra direita

    # [altura, largura]
    cardsImg = img[y:y + 50, x:x + 120]

    h, w = cardsImg.shape
    #               [altura, largura]
    card1 = cardsImg[:, int(w/2/2 - 10):int(w/2)]
    card2 = cardsImg[:, int(w/2 + w/2/2 - 10):]

    self.cards[0].value = detectCaractere(card1)
    self.cards[1].value = detectCaractere(card2)
    
    """ cv.imshow("cards", cardsImg)
    cv.imshow("card1", card2) """

stats = stats()
window = window()
potImage = {}
tableBetImage = {}
flopImage = {}
flopCardsImage = [{}, {}, {}]
turnCardImage = {}
riverCardImage = {}

def callback(hwnd, extra):
  global window
  window_name = win32gui.GetWindowText(hwnd)

  if not ('No Limit Hold\'em' or 'No Limit Hold’em') in window_name:
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

def getMonitor():
  # https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
  win32gui.EnumWindows(callback, None)
  monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
  return monitor

def empty(a):
  pass

def detectCaractere(img):
  conf = r'--oem 1 --psm 10'
  result = pytesseract.image_to_string(img, config=conf)

  return result

def detectNumber(img):
  conf = r'--oem 1 --psm 7 outputbase digits'
  result = pytesseract.image_to_string(img, config=conf)

  return result

def getPot(img):
  global window
  global stats
  global potImage

  y = int(window.height * 0.313) # quanto maior, mais pra baixo
  x = int(window.width * 0.47) # quanto maior, mais pra direita

  # [altura, largura]
  potImage = img[y:y + 26, x:x + 100]
  # potImage = improveImage(potImage) 
  stats.potValue = detectNumber(potImage)
  
  # cv.imshow("Pot", potImage)

def getTableBet(img):
  global window
  global stats
  global tableBetImage
  

  y = int(window.height * 0.507) # quanto maior, mais pra baixo
  x = int(window.width * 0.46) # quanto maior, mais pra direita

  # [altura, largura]
  tableBetImage = img[y:y + 16, x:x + 100]
  # tableBetImage = improveImage(tableBetImage) 
  stats.roundBetValue = detectNumber(tableBetImage)
  
  # cv.imshow("TableBet", tableBetImage)

def getFlop(img):
  global window
  global stats
  global flopImage
  global flopCardsImage

  y = int(window.height * 0.355) # quanto maior, mais pra baixo
  x = int(window.width * 0.34) # quanto maior, mais pra direita
  # [altura, largura]
  flopImage = img[y:y + 47, x:x + int(x*0.54)]

  h, w = flopImage.shape
  #                         [altura, largura]
  flopCardImage1 = flopImage[:, int(w/3/2 - 10):int(w/3)]
  flopCardImage2 = flopImage[:, int(w/2.1):int(w/3*2)]
  flopCardImage3 = flopImage[:, int(w/1.23):int(w)]

  """ flopCardImage1 = improveImage(flopCardImage1, False)
  flopCardImage2 = improveImage(flopCardImage2, False) 
  flopCardImage3 = improveImage(flopCardImage3, False)  """
  flopCardsImage[0] = flopCardImage1
  flopCardsImage[1] = flopCardImage2
  flopCardsImage[2] = flopCardImage3

  stats.flop[0].value = detectCaractere(flopCardImage1)
  stats.flop[1].value = detectCaractere(flopCardImage2)
  stats.flop[2].value = detectCaractere(flopCardImage3)
  #cv.imshow("Flop", flopImage)

def getTurn(img):
  global window
  global stats
  global turnCardImage

  y = int(window.height * 0.355) # quanto maior, mais pra baixo
  x = int(window.width * 0.56) # quanto maior, mais pra direita
               # [altura, largura]
  turnCardImage = img[y:y + 47, x:x + int(x*0.055)]
  # turnCardImage = improveImage(turnCardImage, False) 

  stats.turn.value = detectCaractere(turnCardImage)

  #cv.imshow("Turn", turnImage)

def getRiver(img):
  global window
  global stats
  global riverCardImage

  y = int(window.height * 0.355) # quanto maior, mais pra baixo
  x = int(window.width * 0.625) # quanto maior, mais pra direita
               # [altura, largura]
  riverCardImage = img[y:y + 47, x:x + int(x*0.055)]
  # riverCardImage = improveImage(riverCardImage, False) 

  stats.river.value = detectCaractere(riverCardImage)

  #cv.imshow("River", riverCardImage)

def getTableStats(img):
  global tableBetImage, potImage

  improvedImage = improveImage(img)

  getPot(improvedImage)
  getTableBet(improvedImage)

  """ w, h = 100, 30
  img1 = cv.resize(potImage,(w, h), fx=2, fy=2, interpolation=cv.INTER_CUBIC)
  img2 = cv.resize(tableBetImage,(w, h), fx=2, fy=2, interpolation=cv.INTER_CUBIC)
  imgStack = np.vstack([img1,img2])

  cv.namedWindow('Stats', cv.WINDOW_NORMAL)
  cv.imshow("Stats", imgStack) """

def getTableCards(img):
  improvedImage = improveImage(img, False)
  getFlop(improvedImage)
  getTurn(improvedImage)
  getRiver(improvedImage)

  # stack = get_one_image([flopCardsImage[0], flopCardsImage[1], flopCardsImage[2], turnCardImage, riverCardImage])
  # cv.imshow("Cards", stack)

def improveImage(image, invert=True):
  # source: https://stackoverflow.com/questions/54497882/how-improve-image-quality-to-extract-text-from-image-using-tesseract
  # create grayscale
  gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

  # perform threshold
  retr, mask = cv.threshold(gray_image, 190, 255, cv.THRESH_BINARY)

  #invert to get black text on white background
  if invert:
    result = cv.bitwise_not(gray_image)
  else:
    return gray_image

  # aumenta a imagem
  #result = cv.resize(result, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
  
  return result

def statusScreen(fps):
  global stats
  global potImage
  screen = np.zeros((512, 512, 3), np.uint8)
  stats_list = {'    STATUS EM TEMPO REAL    ': str(fps), '':'', 
  'potValue: ': stats.potValue,
  'roundBetValue: ': stats.roundBetValue,
  'flop: ': stats.flop[0].value + ' ' + stats.flop[1].value + ' ' + stats.flop[2].value,
  'turn: ': stats.turn.value,
  'river: ': stats.river.value,
  'Player chips: ': player.chips,
  'Player cards: ': player.cards[0].value + ' ' + player.cards[1].value
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
with mss.mss() as sct: 
  while "Screen capturing":
    last_time = time.time()
    # monitor = getMonitor()
    # img = np.array(sct.grab(monitor))
    img = cv.imread('tableWaiting.png')

    window.left = 0
    window.top = 0
    window.right = 955
    window.bottom = 689
    window.width = 955
    window.height = 689
    getTableStats(img)
    getTableCards(img)
    player.getPlayerStats(improveImage(img), player)
    player.getPlayerCards(improveImage(img, False), player)
    statusScreen("FPS: {: .2f}".format(1 / (time.time() - last_time)))
  
    cv.imshow("Screen", img)

    # Press "q" to quit
    if cv.waitKey(25) & 0xFF == ord("q"):
      cv.destroyAllWindows()
      break

  """ cv.namedWindow('TrackBar')
  cv.resizeWindow('TrackBar', 640, 250)
  cv.createTrackbar('Hue min', 'TrackBar', 0, 179, empty) # 0 179 0 255 165 255
  cv.createTrackbar('Hue max', 'TrackBar', 179, 179, empty) 
  cv.createTrackbar('Sat min', 'TrackBar', 0, 255, empty)
  cv.createTrackbar('Sat max', 'TrackBar', 255, 255, empty)
  cv.createTrackbar('Val min', 'TrackBar', 165, 255, empty)
  cv.createTrackbar('Val max', 'TrackBar', 255, 255, empty) """

""" potHSV = cv.cvtColor(pot, cv.COLOR_BGR2HSV)
lower = np.array([0, 0, 150]) # 0 179 0 131 150 255
upper = np.array([179, 131, 255])
mask = cv.inRange(potHSV, lower, upper)
imgResult = cv.bitwise_and(pot, pot, mask=mask)
imgResult = cv.cvtColor(imgResult, cv.COLOR_BGRA2GRAY) """

""" imgHSV = cv.cvtColor(pot, cv.COLOR_BGR2HSV)
h_min = cv.getTrackbarPos('Hue min', 'TrackBar')
h_max = cv.getTrackbarPos('Hue max', 'TrackBar')
s_min = cv.getTrackbarPos('Sat min', 'TrackBar')
s_max = cv.getTrackbarPos('Sat max', 'TrackBar')
v_min = cv.getTrackbarPos('Val min', 'TrackBar')
v_max = cv.getTrackbarPos('Val max', 'TrackBar')
lower = np.array([h_min, s_min, v_min])
upper = np.array([h_max, s_max, v_max])
mask = cv.inRange(imgHSV, lower, upper)
imgResult = cv.bitwise_and(pot, pot, mask=mask),
cv.imshow('Mask', mask) """