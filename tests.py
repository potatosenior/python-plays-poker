cont = 0

for i in range(11):
  for j in range(11):
    for k in range(4):
      if (i + j + k == 10):
        cont += 1
        print("(", cont, ")", i, "+", j, "+", k, "= 10")

print("Numero de soluções: ", cont)