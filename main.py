import time
from tkinter import Tk
from interface import Interface
from read_info import get_data
from classes import *

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

def read_info():
  global data

  get_data(data)

if __name__ == "__main__":
  root, interface = start_interface()
  data = data()
  
  while interface_is_running:
    root.update_idletasks()
    root.update()
    read_info()
    interface.setData(data)

