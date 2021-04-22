# Stats
# +/-
# https://www.sportsv.net/articles/45943?page=3

import os
from datetime import datetime

class Log:
    def __init__(self, datetime=None, quarter=None, subject=None, action=None):
        self.datetime = datetime
        self.quarter = quarter
        self.subject = subject
        self.action = action


    def __str__(self):
        return f"Datetime: {self.datetime}, Quarter: {self.quarter}, Subject: {self.subject} Action: {self.action}"


    # return minutes rounded up 2 digits
    def get_time_diff(self, o):
        # time delta object
        if o.datetime > self.datetime:
            time_diff = o.datetime - self.datetime
        else:
            time_diff = self.datetime - o.datetime
        
        secs = time_diff.seconds
        # transform to minutes
        return round(secs / 60, 2)



class LogAnalyzer:

    q1 = []
    q2 = []
    q3 = []
    q4 = []

    # GLOBALS
    MAKE2 = 'make 2'
    MISS2 = 'miss 2'
    MAKE3 = 'make 3'
    MISS3 = 'miss 3'
    MAKEFT = 'make ft'
    MISSFT = 'miss ft'
    OREB = 'get offReb'
    DREB = 'get defReb'
    STL = 'get steal'
    BLK = 'get block'
    AST = 'get AST'
    TO = 'has TO'
    OF = 'commits OF'
    DF = 'commits DF'

    def __init__(self, game_id):
        self.logs = self.readFile(game_id)
        self.logsArray = self.cleanLog()

    
    def readFile(self,game_id):
        game_path = f"logs/game_{game_id}_log.txt"
        if os.path.exists(game_path):
            f = open(game_path, 'r')
            game_log = f.readlines()
            f.close()
            return game_log
        return None    


    def printLogs(self):
        for log in self.logs:
            print(log)


    def printLogsArray(self):
        for log in self.logsArray:
            print(log)


    def cleanLog(self):
        logsArray = []
        CORRECT_LENGTH = 8
        if self.logs:
            for log in self.logs:    
                split_log = log.split(" ")
                if len(split_log) == CORRECT_LENGTH:
                    # transform string to datetime object
                    log_date = split_log[0][1:-1]
                    log_time = split_log[1][:-1]
                    log_datetime = log_date + " " + log_time
                    log_datetime = datetime.strptime(log_datetime, '%m/%d/%Y %H:%M:%S')

                    # quarter
                    quarter = split_log[4].upper().strip()
                    # number and name
                    subject = split_log[5].strip()
                    # action
                    action = (split_log[6] + " "+ split_log[7]).strip()

                    # make Log object
                    new_log = Log(log_datetime, quarter, subject, action)
                    logsArray.append(new_log)

            return logsArray


    def pullQuarters(self):
        
        for log in self.logsArray:
            if log.quarter == "q1":
                self.q1.append(log)
            
            elif log.quarter == "q2":
                self.q2.append(log)
            
            elif log.quarter == "q3":
                self.q3.append(log)
            
            elif log.quarter == "q4":
                self.q4.append(log)


    def filterBySubject(self, subject):
        # opponent / #<number>|<name>
        person_record = []
        for log in self.logsArray:
            res = log.subject.split("|")
            if len(res) == 2:
                # <number>|<name>
                player = res[1]
                if player == subject:
                    person.record.append(log)
            elif len(res) == 1:
                # opponent
                if subject == "Opponent":
                    person_record.append(log)
        return person_record


    def getScoreChangeByLog(self):
        time = []
        opponent = [0]
        home = [0]
        SCORE_CHANGE_FACTOR = {self.MAKEFT: 1, self.MAKE2: 2, self.MAKE3:3}
        for log in self.logsArray:
            if log.action in SCORE_CHANGE_FACTOR:
                time.append(log.datetime)
                if log.subject == "Opponent":

                    opponent.append(opponent[-1] + SCORE_CHANGE_FACTOR[log.action])
                    home.append(home[-1])
                else:
                    opponent.append(opponent[-1])
                    home.append(home[-1] + SCORE_CHANGE_FACTOR[log.action])
        
        # remove first dummy index
        opponent.pop(0)
        home.pop(0)
        return {"time": time,
                "opponent": opponent,
                "home": home}


    def getQuarterStats(self, quarter):
        pass

    def getPlayerCombinations(self):
        pass

    def getPlusMinus(self):
        pass

    def getBestCombo(self):
        pass



#logs = LogAnalyzer(24)






















