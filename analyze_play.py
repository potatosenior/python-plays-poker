import numpy as np
from analyze_cards import analyze_initial_hand

pos_combos = {
  0: [1, 2, 3, 4, 5, 6, 7, 8], # button
  1: [1, 2, 3, 4, 5], # small blind
  2: [1, 2, 3, 4], # big blind
  3: [1, 2], # UTG
  4: [1, 2, 3], # UTG +1
  5: [1, 2, 3, 4], # MP 1
  6: [1, 2, 3, 4, 5], # MP 2
  7: [1, 2, 3, 4, 5, 6], # HI JACK
  8: [1, 2, 3, 4, 5, 6, 7] # CUT OFF
}

def should_play_initial_hand(player_cards, button_pos, data):
  hand_power = analyze_initial_hand(player_cards[0], player_cards[1])
  player_pos = 0
  if button_pos > 0:
    # qntd of players - button pos
    player_pos = 9 - button_pos
  if hand_power:
    if hand_power in pos_combos[player_pos]:
      print('play! hand power: {}, player position: {}->{}'.format(hand_power, player_pos, pos_combos[player_pos]))
      result = True
    else:
      print('dontn\'t play! hand power: {}, player pos: {}->{}'.format(hand_power, player_pos, pos_combos[player_pos]))
      result = False
  else:
    print('dontn\'t play! hand power: {}, player pos: {}->{}'.format(hand_power, player_pos, pos_combos[player_pos]))
    result = False

  return result, hand_power

if __name__ == "__main__":
  from classes import card

  playerCards = [card(), card()]

  playerCards[0].value = '10'
  playerCards[0].suit = 'spades'
  playerCards[1].value = '10'
  playerCards[1].suit = 'clubs'

  should_play_initial_hand(playerCards, 0)
