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

    self.tableConfigMaxPlayers = Label(self.StatsContainer, text="Max players: 9", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableConfigMaxPlayers.config(subFontConfig)
    self.tableConfigMaxPlayers["font"] = fontSmall
    self.tableConfigMaxPlayers.grid(column=1, row=0, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tableStatsTitle = Label(self.StatsContainer, text="Table stats", bg=bg2)
    self.tableStatsTitle.config(defaultFontConfig)
    self.tableStatsTitle["font"] = defaultFont
    self.tableStatsTitle.grid(column=0, row=1, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.tableStatsBlinds = Label(self.StatsContainer, text="blinds: 50/100", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableStatsBlinds.config(subFontConfig)
    self.tableStatsBlinds["font"] = fontSmall
    self.tableStatsBlinds.grid(column=1, row=1, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tableStatsAnte = Label(self.StatsContainer, text="ante: 15", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tableStatsAnte.config(subFontConfig)
    self.tableStatsAnte["font"] = fontSmall
    self.tableStatsAnte.grid(column=2, row=1, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsTitle = Label(self.StatsContainer, text="Round stats", bg=bg2)
    self.roundStatsTitle.config(defaultFontConfig)
    self.roundStatsTitle["font"] = defaultFont
    self.roundStatsTitle.grid(column=0, row=2, sticky=W, padx=itemPadX, pady=itemTitlePadY)

    self.roundStatsPotSize = Label(self.StatsContainer, text="Pot size: 99999", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsPotSize.config(subFontConfig)
    self.roundStatsPotSize["font"] = fontSmall
    self.roundStatsPotSize.grid(column=1, row=2, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsBetsize = Label(self.StatsContainer, text="Round bet size: 88888", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.roundStatsBetsize.config(subFontConfig)
    self.roundStatsBetsize["font"] = fontSmall
    self.roundStatsBetsize.grid(column=2, row=2, sticky=W, padx=itemPadX, pady=itemPadY)

    self.roundStatsOpponents = Label(self.StatsContainer, text="Opponents playing: 8", bg=bg, padx=padx, pady=pady, width=itemWidth)
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

    self.tablePlayerStatsCards = Label(self.StatsContainer, text="Cards: 10 ♥️ J ♦️", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tablePlayerStatsCards.config(subFontConfig)
    self.tablePlayerStatsCards["font"] = fontSmall
    self.tablePlayerStatsCards.grid(column=1, row=4, sticky=W, padx=itemPadX, pady=itemPadY)

    self.tablePlayerStatsChips = Label(self.StatsContainer, text="Chips: 17200", bg=bg, padx=padx, pady=pady, width=itemWidth)
    self.tablePlayerStatsChips.config(subFontConfig)
    self.tablePlayerStatsChips["font"] = fontSmall
    self.tablePlayerStatsChips.grid(column=2, row=4, sticky=W, padx=itemPadX, pady=itemPadY)

  def setData(self, data):
    self.tableConfigMaxPlayers["text"] = data.maxPlayers
    self.tableStatsBlinds["text"] = data.sb + '/' + data.bb
    self.tableStatsAnte["text"] = data.ante
    self.roundStatsPotSize["text"] = data.potSize
    self.roundStatsBetsize["text"] = data.roundBetSize
    self.roundStatsOpponents["text"] = data.opponents
    self.roundStatsFlop["text"] = data.roundStatsFlop
    self.roundStatsTurn["text"] = data.turn
    self.roundStatsRiver["text"] = data.river
    self.tablePlayerStatsCards["text"] = data.playerCards
    self.tablePlayerStatsChips["text"] = data.playerChips

if __name__ == "__main__":
  root = Tk()
  Interface(root)

  root.title("Python Play's Poker!")

  root.mainloop()
