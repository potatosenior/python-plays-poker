import re

def validate_card_value(card, shown=False):
  values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
  others = ['g', 'G', 'O']
  othersValue = ['9', 'Q', '6']

  #removes all other caracteres
  result = re.sub("[^0-9^AJQKGOg]", "", card)
  if shown:
    print('og: ', card, 'filtred: ', result)

  if result in values:
    return result
  elif result in others:
    return othersValue[others.index(result)]
  else:
    return False

def validate_numbers_value(numbers):
  result = re.sub("[^0-9]", "", numbers)
  
  return result

def validate_name(numbers):
  result = re.sub("[^A-Z^a-z^0-9]", "", numbers)
  
  return result