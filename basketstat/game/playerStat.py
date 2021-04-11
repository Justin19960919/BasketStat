class MyPlayerRecord:
    def __init__(self, name, number, numberOfMinutesPlayed= 0, twoPointers = 0, twoPointersMade = 0, threePointers= 0, threePointersMade= 0,
        freethrows= 0, freethrowsMade= 0, offensiveRebound= 0, defensiveRebound= 0, block= 0, steal= 0, assist= 0,
        turnover= 0, offensiveFoul= 0, defensiveFoul= 0):
        
        # init
        self.name = name
        self.number = number
        # number of minutes played
        self.numberOfMinutesPlayed = numberOfMinutesPlayed
        # two pointers
        self.twoPointers = twoPointers
        self.twoPointersMade = twoPointersMade
        # ThreePointers
        self.threePointers = threePointers
        self.threePointersMade = threePointersMade
        # Freethrows
        self.freeThrows = freethrows
        self.freeThrowsMade = freethrowsMade
        # Rebounds
        self.offensiveRebound = offensiveRebound
        self.defensiveRebound = defensiveRebound
        # Block / Steals
        self.block = block
        self.steal = steal
        # Assist / turnOver
        self.assist = assist
        self.turnover = turnover
        # foul/ playTime
        self.offensiveFoul = offensiveFoul
        self.defensiveFoul = defensiveFoul



    def __str__(self):
        return "NOM: {}, 2P: {}, 2PMade:{}, 3P:{}, 3PMade:{}, FT:{}, FTMade:{}, OR:{}, DR:{}, BLK:{}, STL:{}, AST:{}, TO:{}, OF:{}, DF:{}".format(
         self.numberOfMinutesPlayed,
         self.twoPointers,
         self.twoPointersMade,
         self.threePointers,
         self.threePointersMade,
         self.freeThrows,
         self.freeThrowsMade,
         self.offensiveRebound,
         self.defensiveRebound,
         self.block,
         self.steal,
         self.assist,
         self.turnover,
         self.offensiveFoul,
         self.defensiveFoul)


class MyPlayerStat:

    def __init__(self,myPlayerRecord):
        # receives a Player Object
        self.playerRecord = myPlayerRecord


    # Basic Stats
    # Points
    def getPoints(self):
        return self.playerRecord.twoPointersMade * 2 + self.playerRecord.threePointersMade * 3
    

    # Field Goals
    def getFieldGoalMade(self):
        return self.playerRecord.twoPointersMade + self.playerRecord.threePointersMade
    
    def getFieldGoalAttempts(self):
        return self.playerRecord.twoPointers + self.playerRecord.threePointers

    def getFieldGoalPercentage(self):
        # round to 2 decimals
        fga = self.getFieldGoalAttempts()
        fgm = self.getFieldGoalMade()

        if fga == 0:
            return 0 
        elif fga > 0:
            return round(fgm/fga,2)


    def getTwoPointPercentage(self):
        if self.playerRecord.twoPointers == 0:
            return 0
        else:
            return round(self.playerRecord.twoPointersMade / self.playerRecord.twoPointers,2)



    # Three point stats
    def getThreePointPercentage(self):
        # round to 2 decimals
        if self.playerRecord.threePointers == 0:
            return 0
        else:
            return round(self.playerRecord.threePointersMade / self.playerRecord.threePointers,2)
    
    def getFreeThrowPercentage(self):
        # round to 2 decimals
        if self.playerRecord.freeThrows == 0:
            return 0
        else:
            return round(self.playerRecord.freeThrowsMade / self.playerRecord.freeThrows,2)


    # Total Rebounds
    def getTotalRebounds(self):
        return self.playerRecord.offensiveRebound + self.playerRecord.defensiveRebound



    # Advanced Stats
    
    # EFF (Efficiency)
    def getEfficiency(self):

        eff = (self.getPoints()+ self.getTotalRebounds()+ self.playerRecord.assist + \
            self.playerRecord.steal + self.playerRecord.block) - (self.getFieldGoalAttempts()- \
                self.getFieldGoalMade()) - (self.playerRecord.freeThrows - self.playerRecord.freeThrowsMade) - self.playerRecord.turnover
        
        return eff


    # GmSc (Game Score)
    def getGmsc(self):

        gmsc = (self.getPoints() + 0.7*self.playerRecord.offensiveRebound + 0.3*self.playerRecord.defensiveRebound + 0.7*self.playerRecord.assist + self.playerRecord.steal + 0.7*self.playerRecord.block) + 0.4* self.getFieldGoalMade() - 0.7* self.getFieldGoalAttempts() - 0.4*(self.playerRecord.freeThrows - self.playerRecord.freeThrowsMade) - self.playerRecord.turnover - 0.4 * (self.playerRecord.offensiveFoul + self.playerRecord.defensiveFoul)

        return gmsc


    # eFG% (effective field goal percentage)
    def getEfg(self):
        # eFG% = (FGM + 0.5*(3PM))/FGA
        try:
            efg = (self.getFieldGoalMade()+ 0.5*self.playerRecord.threePointersMade) / self.getFieldGoalAttempts()
        except:
            efg = 0
        return efg


    # TS (True shooting percentage)
    def getTS(self):
        # 得分/ (2* (FGA + 0.44 * FTA))
        try:
            TS = self.getPoints() / (2*(self.getFieldGoalAttempts()+0.44*self.playerRecord.freeThrows))
        except:
            TS = 0
        return TS


    # Further advanced stats need research....


    def autoGenerate(self):
        # returns a dict for further pandas df merging
        
        statLine = {
            "Name": self.playerRecord.name,
            "Number": self.playerRecord.number,
            "PTS": round(self.getPoints(),2),
            "FGM": round(self.getFieldGoalMade(),2),
            "FGA": round(self.getFieldGoalAttempts(),2),
            "FGP":  round(self.getFieldGoalPercentage(),2),
            "2PP": round(self.getTwoPointPercentage(),2),
            "3PP": round(self.getThreePointPercentage(),2),
            "FTP": round(self.getFreeThrowPercentage(),2),
            "EFF": round(self.getEfficiency(),2),
            "GMSC":round(self.getGmsc(),2),
            "EFG":round(self.getEfg(),2),
            "TS":round(self.getTS(),2)
        }

        return statLine




