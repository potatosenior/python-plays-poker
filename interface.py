from tkinter import *

class Interface:
  def __init__(self, master=None):
    bg = "#121212"
    bg2 = "#161616"
    defaultFont = ("sans-serif", "15")
    fontSmall = ("Arial", "10", "normal")
    defaultFontConfig = {'fg': "#FFF"}
    subFontConfig = {'fg': "red"}
    itemPadX = 2
    itemPadY = 2
    itemWidth = 20
    itemTitlePadY = 30
    padx = 15
    pady = 20

    # master.geometry('800x600')
    # master.wm_attributes('-transparentcolor', 'black')

    self.rootContainer = Frame(master, padx=5, pady=5)
    self.rootContainer.config(bg=bg)
    self.rootContainer.grid(column=0, row=0, sticky=(N, W, E, S))
    master.columnconfigure(0, weight=1)
    master.rowconfigure(0, weight=1)

    self.title = Label(self.rootContainer, text="PROGAM CONTROLLER", font=("Arial", "20", "bold"), bg=bg)
    self.title.config(defaultFontConfig, padx=20, pady=30)
    self.title.grid(column=0, row=0, sticky=N)

    self.StatsContainer = Frame(self.rootContainer, padx=5, pady=5)
    self.StatsContainer.config(bg=bg2)
    self.StatsContainer.grid(column=0, row=1, sticky=(N, W, E, S))

    self.tableConfigTitle = Label(self.StatsContainer, text="Table configs", bg=bg2)
    self.tableConfigTitle.config(defaultFontConfig)
    self.tableConfigTitle["font"] = defaultFont
    self.tableConfigTitle.grid(column=0, row=0, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.fps = Label(self.rootContainer, text="FPS:", bg=bg2)
    self.fps.config(defaultFontConfig)
    self.fps["font"] = defaultFont
    self.fps.grid(column=1, row=0, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.tableConfigMaxPlayers = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableConfigMaxPlayers.config(subFontConfig)
    self.tableConfigMaxPlayers["font"] = fontSmall
    self.tableConfigMaxPlayers.grid(column=1, row=0, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tableStatsTitle = Label(self.StatsContainer, text="Table stats", bg=bg2)
    self.tableStatsTitle.config(defaultFontConfig)
    self.tableStatsTitle["font"] = defaultFont
    self.tableStatsTitle.grid(column=0, row=1, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.tableStatsBlinds = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableStatsBlinds.config(subFontConfig)
    self.tableStatsBlinds["font"] = fontSmall
    self.tableStatsBlinds.grid(column=1, row=1, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tableStatsAnte = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableStatsAnte.config(subFontConfig)
    self.tableStatsAnte["font"] = fontSmall
    self.tableStatsAnte.grid(column=2, row=1, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsTitle = Label(self.StatsContainer, text="Round stats", bg=bg2)
    self.roundStatsTitle.config(defaultFontConfig)
    self.roundStatsTitle["font"] = defaultFont
    self.roundStatsTitle.grid(column=0, row=2, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.roundStatsPotSize = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsPotSize.config(subFontConfig)
    self.roundStatsPotSize["font"] = fontSmall
    self.roundStatsPotSize.grid(column=1, row=2, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsBetsize = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsBetsize.config(subFontConfig)
    self.roundStatsBetsize["font"] = fontSmall
    self.roundStatsBetsize.grid(column=2, row=2, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsOpponents = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsOpponents.config(subFontConfig)
    self.roundStatsOpponents["font"] = fontSmall
    self.roundStatsOpponents.grid(column=3, row=2, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsFlop = Label(self.StatsContainer, text="Flop: 10 ♥️ J ♦️ Q ♣", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsFlop.config(subFontConfig)
    self.roundStatsFlop["font"] = fontSmall
    self.roundStatsFlop.grid(column=1, row=3, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsTurn = Label(self.StatsContainer, text="Turn: K ♠️", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsTurn.config(subFontConfig)
    self.roundStatsTurn["font"] = fontSmall
    self.roundStatsTurn.grid(column=2, row=3, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsRiver = Label(self.StatsContainer, text="River: A ♠️", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsRiver.config(subFontConfig)
    self.roundStatsRiver["font"] = fontSmall
    self.roundStatsRiver.grid(column=3, row=3, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tablePlayerStatsTitle = Label(self.StatsContainer, text="Player stats", bg=bg2)
    self.tablePlayerStatsTitle.config(defaultFontConfig)
    self.tablePlayerStatsTitle["font"] = defaultFont
    self.tablePlayerStatsTitle.grid(column=0, row=4, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.tablePlayerStatsCards = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tablePlayerStatsCards.config(subFontConfig)
    self.tablePlayerStatsCards["font"] = fontSmall
    self.tablePlayerStatsCards.grid(column=1, row=4, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tablePlayerStatsChips = Label(self.StatsContainer, text="", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tablePlayerStatsChips.config(subFontConfig)
    self.tablePlayerStatsChips["font"] = fontSmall
    self.tablePlayerStatsChips.grid(column=2, row=4, sticky=W, padx=itemPadX, pady=itemPadY)

  def setData(self, data):
    self.tableConfigMaxPlayers["text"] = 'Max players: ' + str(data.maxPlayers)
    self.tableStatsBlinds["text"] = 'blinds: ' + str(data.sb) + '/' + str(data.bb)
    self.tableStatsAnte["text"] = 'Ante: ' + str(data.ante)
    self.roundStatsPotSize["text"] = 'Pot size: ' + str(data.potSize)
    self.roundStatsBetsize["text"] = 'Round bet size: ' + str(data.roundBetSize)
    self.roundStatsOpponents["text"] = 'Opponents: ' +  str(data.opponents)
    self.roundStatsFlop["text"] = 'Flop: {} {} {}'.format(str(data.flop[0].value), str(data.flop[1].value), str(data.flop[2].value))
    self.roundStatsTurn["text"] = 'Turn: ' + str(data.turn.value)
    self.roundStatsRiver["text"] = 'River: ' + str(data.river.value)
    self.tablePlayerStatsCards["text"] = 'Cards: ' + str(data.playerCards)
    self.tablePlayerStatsChips["text"] = 'Chips: ' + str(data.playerChips)
    self.fps["text"] = 'FPS: ' + str(data.fps)

if __name__ == "__main__":
  root = Tk()
  Interface(root)
  root.title("Python Play's Poker!")
  root.mainloop()
