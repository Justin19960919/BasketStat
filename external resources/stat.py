
class Stat:

    def __init__(self,Player):
        # receives a Player Object
        self.player = Player


    # Basic Stats
    # Points
    def getPoints(self):
        return self.player.twoPointerMade * 2 + self.player.threePointerMade * 3
    

    # Field Goals
    def getFieldGoalMade(self):
        return self.player.twoPointerMade + self.player.threePointerMade
    
    def getFieldGoalAttempts(self):
        return self.player.twoPointer + self.player.threePointer

    def getFieldGoalPercentage(self):
        # round to 2 decimals
        fga = self.getFieldGoalAttempts()
        fgm = self.getFieldGoalMade()

        if fga == 0:
            return 0 
        elif fga > 0:
            return round(fgm/fga,2)


    def getTwoPointPercentage(self):
        if self.player.twoPointer == 0:
            return 0
        else:
            return round(self.player.twoPointerMade / self.player.twoPointer,2)



    # Three point stats
    def getThreePointPercentage(self):
        # round to 2 decimals
        if self.player.threePointer == 0:
            return 0
        else:
            return round(self.player.threePointerMade / self.player.threePointer,2)
    
    def getFreeThrowPercentage(self):
        # round to 2 decimals
        if self.player.freeThrow == 0:
            return 0
        else:
            return round(self.player.freeThrowMade / self.player.freeThrow,2)


    # Total Rebounds
    def getTotalRebounds(self):
        return self.player.offensiveRebound + self.player.defensiveRebound



    # Advanced Stats
    
    # EFF (Efficiency)
    def getEfficiency(self):

        eff = (self.getPoints()+ self.getTotalRebounds()+ self.player.assist + \
            self.player.steal + self.player.block) - (self.getFieldGoalAttempts()+ \
                self.getFieldGoalMade()) - (self.player.freeThrow - self.player.freeThrowMade) - self.player.turnOver
        
        return eff


    # GmSc (Game Score)
    def getGmsc(self):

        gmsc = (self.getPoints() + 0.7*self.player.offensiveRebound + 0.3*self.player.defensiveRebound + 0.7*self.player.assist + self.player.steal + 0.7*self.player.block) + 0.4* self.getFieldGoalMade() - 0.7* self.getFieldGoalAttempts() - 0.4*(self.player.freeThrow - self.player.freeThrowMade) - self.player.turnOver - 0.4 * self.player.foul

        return gmsc


    # eFG% (effective field goal percentage)
    def getEfg(self):
        # eFG% = (FGM + 0.5*(3PM))/FGA
        efg = (self.getFieldGoalMade()+ 0.5*self.player.threePointerMade) / self.getFieldGoalAttempts()

        return efg


    # TS (True shooting percentage)
    def getTS(self):
        # 得分/ (2* (FGA + 0.44 * FTA))
        TS = self.getPoints() / (2*(self.getFieldGoalAttempts()+0.44*self.player.freeThrow))

        return TS


    # Further advanced stats need research....


    def autoGenerate(self):
        # returns a dict for further pandas df merging
        
        statLine = {
            "PTS": self.getPoints(),
            "FGM": self.getFieldGoalMade(),
            "FGA": self.getFieldGoalAttempts(),
            "FG": self.getFieldGoalPercentage(),
            "2PP": self.getTwoPointPercentage(),
            "3PP": self.getThreePointPercentage(),
            "FTP": self.getFreeThrowPercentage(),
            "EFF": self.getEfficiency(),
            "GMSC":self.getGmsc(),
            "EFG":self.getEfg(),
            "TS":self.getTS()
        }

        return statLine




