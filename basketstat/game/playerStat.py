from .models import Game, PlayerRecord
import datetime
from django.contrib import messages

class ProcessGameRecord:
    def __init__(self, request, logging_path, game_id):
        self.request = request
        self.post_request = request.POST    # dict
        self.logging_path = logging_path         # path to logger
        self.id = game_id
        self.game = Game.objects.get(id=game_id)
        self.quarter = None

    def getGame(self):
        return self.game

    def getQuarter(self):
        return self.quarter

    def checkOpponentPress(self):
        op_ts1 =  "other_team_score1" in self.post_request
        op_ts2 =  "other_team_score2" in self.post_request
        op_ts3 =  "other_team_score3" in self.post_request
        if op_ts1 or op_ts2 or op_ts3:
            return True
        return False

    def writeToLog(self, msg):
        with open(self.logging_path, 'a') as file:
            msg_time = datetime.datetime.now()
            msg_time = msg_time.strftime("%m/%d/%Y, %H:%M:%S")
            file.write(f"[{msg_time}]   {msg}\n")

    def checkSelectPlayer(self):
        if 'select-player' not in self.post_request:
            return False

        self.player_record_id = self.post_request.get('select-player')
        print('Player record id: ', self.player_record_id)
        return True

    def checkQuarter(self):
        if 'quarter' not in self.post_request:
            return False

        self.quarter = self.post_request.get('quarter')
        print('Quarter: ', self.quarter)
        return True


    def instantiatePlayerRecordObject(self):
        playerRecord = PlayerRecord.objects.get(id = self.player_record_id)
        self.playerRecord = playerRecord
        self.playerName = playerRecord.playerId.name
        self.playerNumber = playerRecord.playerId.number


    def savePlayerRecordAndGame(self):
        self.game.save()
        self.playerRecord.save()



    def createMessageHeader(self):
        if self.quarter and self.playerName and self.playerNumber:
            msg_header = f"{self.quarter.upper()} #{self.playerNumber}|{self.playerName} "
            self.msg_header = msg_header


    def addQuarterScore(self, addPoints):
        if self.game:
            self.game.total_score += addPoints
            if self.quarter == 'q1':
                self.game.quarter1_score += addPoints
                print(f"Added {addPoints} to q1")
            
            elif self.quarter == 'q2':
                self.game.quarter2_score += addPoints
                print(f"Added {addPoints} to q2")

            elif self.quarter == 'q3':
                self.game.quarter3_score += addPoints
                print(f"Added {addPoints} to q3")
            
            elif self.quarter == 'q4':
                self.game.quarter4_score += addPoints
                print(f"Added {addPoints} to q4")

    def addOpponentQuarterScore(self, addPoints):
        if self.game and self.quarter:
            msg = f"{self.quarter.upper()} Opponent scores {addPoints}"

            self.game.other_total_score += addPoints
            if self.quarter == 'q1':
                self.game.other_quarter1_score += addPoints
            
            elif self.quarter == 'q2':
                self.game.other_quarter2_score += addPoints

            elif self.quarter == 'q3':
                self.game.other_quarter3_score += addPoints
            
            elif self.quarter == 'q4':
                self.game.other_quarter4_score += addPoints

            print(msg)
            self.game.save()
            self.writeToLog(msg)
            messages.success(self.request, msg)


    def endingSequence(self, additionalMsg):
        print("Saving player record and game record")
        self.savePlayerRecordAndGame()
        print("Creating logging message")
        msg = self.msg_header + additionalMsg
        print("Writing to game logger")
        self.writeToLog(msg)
        print("Finished.. ")
        print("Render msg..")
        messages.success(self.request, msg)


    def make2pt(self):
        if "make-2pt" in self.post_request:
            self.playerRecord.twoPointersMade += 1
            self.playerRecord.twoPointers += 1
            self.addQuarterScore(2)
            self.endingSequence('make 2')


    def miss2pt(self):
        if "miss-2pt" in self.post_request:
            self.playerRecord.twoPointers += 1
            self.endingSequence('miss 2')


    def make3pt(self):
        if "make-3pt" in self.post_request:
            self.playerRecord.threePointersMade += 1
            self.playerRecord.threePointers += 1    
            self.addQuarterScore(3)
            self.endingSequence('make 3')
    

    def miss3pt(self):
        if "miss-3pt" in self.post_request:
            self.playerRecord.threePointers += 1
            msg = self.msg_header + "miss 3"
            self.endingSequence('miss 3')


    def makeft(self):
        if "make-ft" in self.post_request:
            self.playerRecord.freethrowMade += 1
            self.playerRecord.freethrows += 1
            self.addQuarterScore(1)
            self.endingSequence('make ft')


    def missft(self):
        if "miss-ft" in self.post_request:
            self.playerRecord.freethrows += 1
            self.endingSequence('miss ft')
       

    def offReb(self):
        if "off-reb" in self.post_request:
            self.playerRecord.offensiveRebound += 1
            self.endingSequence('get offReb')



    def defReb(self):
        if "def-reb" in self.post_request:
            self.playerRecord.defensiveRebound += 1
            self.endingSequence('get defReb')  


    def steal(self):
        if "steal" in self.post_request:
            self.playerRecord.steal += 1
            self.endingSequence('get steal') 


    def block(self):
        if "block" in self.post_request:
            self.playerRecord.block += 1
            self.endingSequence('get block')             

    def ast(self):
        if "ast" in self.post_request:
            self.playerRecord.assist += 1
            self.endingSequence('get AST') 

    def to(self):
        if "to" in self.post_request:
            self.playerRecord.turnover += 1
            self.endingSequence('has TO') 


    def offFoul(self):
        if "off-foul" in self.post_request:
            self.playerRecord.offensiveFoul += 1
            self.endingSequence('commits OF') 

    def defFoul(self):
        if "def-foul" in self.post_request:
            self.playerRecord.defensiveFoul += 1
            self.endingSequence('commits DF') 

    def determineAction(self):
        self.make2pt()
        self.miss2pt()
        self.make3pt()
        self.miss3pt()
        self.makeft()
        self.missft()
        self.offReb()
        self.defReb()
        self.steal()
        self.block()
        self.ast()
        self.to()
        self.offFoul()
        self.defFoul()


    # access point
    def processHomeTeam(self):
        sp = self.checkSelectPlayer()
        q = self.checkQuarter()
        
        if sp and q:
            # if both are true then we process
            self.instantiatePlayerRecordObject()
            self.createMessageHeader()
            self.determineAction()

        elif not sp and not self.checkOpponentPress():
            messages.warning(self.request, "Need to select a player")
        
        elif not q and not self.checkOpponentPress():
            messages.warning(self.request, "Need to select a quarter")

        # opponent pressed
        else:
            self.processOpponent()


    def processOpponent(self):
        # first check quarter
        if not self.checkQuarter():
            messages.warning(self.request, "Need to select a quarter")
        else:
            addPoints = 0
            # selected quarter
            if 'other_team_score1' in self.post_request:
                addPoints = 1
            elif 'other_team_score2' in self.post_request:
                addPoints = 2
            elif 'other_team_score3' in self.post_request:
                addPoints = 3

            self.addOpponentQuarterScore(addPoints)













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






