#
# This class holds the various states present in the game
#


class State:
    def __init__(self):
        self.totalPlayerCount = 0
        self.currentPlayer = 0



    def nextPlayer(self):
        self.currentPlayer += 1



    def incTotalPlayerCount(self):
        self.totalPlayerCount += 1



    def getNumTotalPlayers(self):
        return self.totalPlayerCount



    def setNumTotalPlayers(count):
        self.totalPlayerCount = count



    def getCurrentPlayer(self):
        return self.currentPlayer



    def setCurrentPlayer(self, number):
        self.currentPlayer = number



    def previousPlayer(self):
        self.currentPlayer -= 1



