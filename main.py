import time
import numpy as np
from tkinter import Tk
from interface import Interface
from read_info import retrieve_data
from classes import *
from analyze_play import *
from mouse_controller import *

interface_is_running = True

def close_interface():
  global interface_is_running

  interface_is_running = False

def start_interface():
  root = Tk()
  interface = Interface(root)
  root.title("Python Play's Poker!")
  root.protocol("WM_DELETE_WINDOW", close_interface)

  return root, interface

def read_info(data):
  retrieve_data(data)

  if data.state > 0 and data.stillPlaying:
    # play
    print('state: {}, round: {}, cards: {} {}'.format(data.state, data.round, data.playerCards[0].value, data.playerCards[1].value))
    should, hand_power = should_play_initial_hand(data.playerCards, data.buttonPos, data)
    data.hasPlayed = True

    # makes the play
    if data.round == 0:
      if should:
        if hand_power == 1:
          # raise or all in
          click(data, 3)
          action = 1
        else:
          # call or check
          click(data, 2)
          action = 1
      else:
        if data.state == 1:
          # check
          click(data, 2)
          action = 1
        else:
          # fold
          click(data, 1)
          action = 0
          data.stillPlaying = False

      # log = np.asarray([[data.playerCards[0].value + data.playerCards[0].suit[0], data.playerCards[1].value + data.playerCards[1].suit[0], data.state, action]], dtype=object)

      # with open('./logs/flop_log.csv', 'a+') as file:
        # np.savetxt(file, log, fmt='%s')

    if data.round >= 1:
      if hand_power:
        if hand_power == 1:
          # raise or all in
          click(data, 3)

        if hand_power <= 3:
          if data.state <= 2:
            # check or call
            click(data, 2)
          else:
            click(data, 3)
        else:
          if data.state == 1:
            # check
            click(data, 2)
          else:
            # fold
            click(data, 1)
      else:
        if data.state == 1:
          # check
          click(data, 2)
        else:
          # fold
          click(data, 1)

if __name__ == "__main__":
  root, interface = start_interface()
  data = data()
  
  while interface_is_running:
    root.update_idletasks()
    root.update()
    read_info(data)
    interface.setData(data)

