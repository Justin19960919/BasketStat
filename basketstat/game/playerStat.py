class PlayerGameRecord:
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
        return "Name: {}, Number: {},NOM: {}, 2P: {}, 2PMade:{}, 3P:{}, 3PMade:{}, FT:{}, FTMade:{}, OR:{}, DR:{}, BLK:{}, STL:{}, AST:{}, TO:{}, OF:{}, DF:{}".format(
         self.name,
         self.number,
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



    # Basic Stats
    # Points
    def getPoints(self):
        return self.twoPointersMade * 2 + self.threePointersMade * 3
    

    # Field Goals
    def getFieldGoalMade(self):
        return self.twoPointersMade + self.threePointersMade
    

    def getFieldGoalAttempts(self):
        return self.twoPointers + self.threePointers


    def getFieldGoalPercentage(self):
        # round to 2 decimals
        fga = self.getFieldGoalAttempts()
        fgm = self.getFieldGoalMade()

        if fga == 0:
            return 0 
        elif fga > 0:
            return round(fgm/fga,2)


    def getTwoPointPercentage(self):
        if self.twoPointers == 0:
            return 0
        else:
            return round(self.twoPointersMade / self.twoPointers,2)



    # Three point stats
    def getThreePointPercentage(self):
        # round to 2 decimals
        if self.threePointers == 0:
            return 0
        else:
            return round(self.threePointersMade / self.threePointers,2)
    
    def getFreeThrowPercentage(self):
        # round to 2 decimals
        if self.freeThrows == 0:
            return 0
        else:
            return round(self.freeThrowsMade / self.freeThrows,2)


    # Total Rebounds
    def getTotalRebounds(self):
        return self.offensiveRebound + self.defensiveRebound



    # Advanced Stats
    
    # EFF (Efficiency)
    def getEfficiency(self):

        eff = (self.getPoints()+ self.getTotalRebounds()+ self.assist + \
            self.steal + self.block) - (self.getFieldGoalAttempts()- \
                self.getFieldGoalMade()) - (self.freeThrows - self.freeThrowsMade) - self.turnover
        
        return eff


    # GmSc (Game Score)
    def getGmsc(self):

        gmsc = (self.getPoints() + 0.7*self.offensiveRebound + 0.3*self.defensiveRebound + 0.7*self.assist + self.steal + 0.7*self.block) + 0.4* self.getFieldGoalMade() - 0.7* self.getFieldGoalAttempts() - 0.4*(self.freeThrows - self.freeThrowsMade) - self.turnover - 0.4 * (self.offensiveFoul + self.defensiveFoul)

        return gmsc


    # eFG% (effective field goal percentage)
    def getEfg(self):
        # eFG% = (FGM + 0.5*(3PM))/FGA
        try:
            efg = (self.getFieldGoalMade()+ 0.5*self.threePointersMade) / self.getFieldGoalAttempts()
        except:
            efg = 0
        return efg


    # TS (True shooting percentage)
    def getTS(self):
        # 得分/ (2* (FGA + 0.44 * FTA))
        try:
            TS = self.getPoints() / (2*(self.getFieldGoalAttempts()+0.44*self.freeThrows))
        except:
            TS = 0
        return TS

    # TurnOver percentage
    def getTOV(self):
        try:
            tov = self.turnover / (self.getFieldGoalAttempts() + 0.44* self.freeThrows + self.turnover)
        except: 
            tov = 0 
        return tov

    
    def turnToPercentage(self,number):
        return str(round(number * 100, 3)) + "%"


    def autoGenerate(self):
        # returns a dict for further pandas df merging
        
        statLine = {
            "Name": self.name,
            "Number": self.number,
            "PTS": self.getPoints(),
            "FGM": self.getFieldGoalMade(),
            "FGA": self.getFieldGoalAttempts(),
            "FGP": self.turnToPercentage(self.getFieldGoalPercentage()),
            "2PP": self.turnToPercentage(self.getTwoPointPercentage()),
            "3PP": self.turnToPercentage(self.getThreePointPercentage()),
            "FTP": self.turnToPercentage(self.getFreeThrowPercentage()),
            "EFF": self.getEfficiency(),
            "GMSC": round(self.getGmsc(), 2),
            "EFG": self.turnToPercentage(self.getEfg()),
            "TS": self.turnToPercentage(self.getTS()),
            "TOV": self.turnToPercentage(self.getTOV())
        }

        return statLine

