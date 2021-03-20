class Game:

    def __init__(self,gameName):
        self.gameName = gameName
        self.players = []
        self.videoUrl = None
    

    def addPlayer(self,Player):
        self.players.append(Player)
    


