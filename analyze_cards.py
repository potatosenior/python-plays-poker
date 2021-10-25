# import numpy as np
from classes import card

pairs = {
  1: ['AA', 'KK', 'QQ', 'JJ'],
  2: ['1010'],
  3: ['99'],
  4: ['88'],
  5: ['77'],
  6: ['66', '55'],
  7: ['44', '33', '22']
}
suiteds = {
  1: ['AKs'],
  2: ['AQs', 'AJs', 'KQs'],
  3: ['A10s', 'KJs', 'QJs', 'J10s'],
  4: ['K10s', 'Q10s', 'J9s', '109s', '98s'],
  5: ['A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
    'Q9s', '108s', '97s', '87s', '76s'],
  6: ['K9s', 'J8s', '86s', '75s', '54s'],
  7: ['K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s', 'Q8s',
    '107s', '64s', '53s', '43s'],
  8: ['J7s', '96s', '85s', '74s', '42s', '32s']
}
offsuiteds = {
  2: ['AKo'],
  3: ['AQo'],
  4: ['AJo', 'KQo'],
  5: ['KJo', 'QJo', 'J10o'],
  6: ['A10o', 'K10o', 'Q10o'],
  7: ['J9o', '98o'],
  8: ['A9o', 'K9o', 'Q9o', 'J8o', '108o', '87o', '76o', '65o', '54o']
}



def get_hand_power(card1, card2, same_suit):
  if card1.value == card2.value:
    # its a pair
    player_cards = str(card1.value) + str(card2.value)

    for rank, cards in pairs.items():
      if player_cards in cards:
        return rank
  elif same_suit:
    player_cards = str(card1.value) + str(card2.value) + 's'
    
    for rank, cards in suiteds.items():
      if player_cards in cards:
        return rank
  else:
    player_cards = str(card1.value) + str(card2.value) + 'o'

    for rank, cards in offsuiteds.items():
      if player_cards in cards:
        return rank

def sort_cards(card1, card2):
  # sort the cards in A -> 2 to fit in the arrays values
  # ordena as cartas em ordem crescente, ex: card1 = 7 e card2 = A, card1 recebe A, e card2 recebe 7 para encaixar nos arrays acima
  if card1.value == card2.value:
    return card1, card2
  else:
    values = {
      'A': 10,
      'K': 9,
      'Q': 8,
      'J': 7
    }
    if card1.value in values and card2.value in values:
      if values[card1.value] > values[card2.value]:
        return card1, card2
      else:
        return card2, card1
    else:
      if(card1.value[0] > card2.value[0]):
        return card1, card2
      else:
        return card2, card1

def analyze_initial_hand(card1, card2):
  card1, card2 = sort_cards(card1, card2)

  if card1.suit == card2.suit:
    # same suited
    return get_hand_power(card1, card2, True)
  else:
    # off suit
    return get_hand_power(card1, card2, False)

if __name__ == "__main__":
  playerCards = [card(), card()]

  playerCards[0].value = 'J'
  playerCards[0].suit = 'spades'
  playerCards[1].value = 'A'
  playerCards[1].suit = 'spades'

  result = analyze_initial_hand(playerCards[0], playerCards[1])
  print(result)