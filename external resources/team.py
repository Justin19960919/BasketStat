# Team
# Field goal percentage, three point percentage, free throw percentage.rebounds per game ,
# assists, TOs, steals, blocks, fouls, points

# Lineups
# MIN OFFTRG DEFRTG NETRTG AST% AST/TO AST RATIO OREB% DREB% REB% TO RATIO EFG% TS% EFG% PACE PIE



# Basic team stats
class TeamGameRecord:
	
	def __init__(self):
		self.teamGameRecord = []

	def addPlayerRecord(self, PlayerGameRecord):
		self.teamGameRecord.append(PlayerGameRecord)


	def removePlayerRecord(self):
		# pop the last item
		self.teamGameRecord.pop()


	def getBasicTeamStats(self):
		
		if len(self.teamGameRecord) == 0:
			print("No team records!")

		else:
			teamTime = 0
			team2P = 0
			team2PM = 0
			team3P = 0
			team3PM = 0
			
			teamFTA = 0
			teamFTM = 0
			# teamFGM: field goals made
			# teamFGA: field goals attempts

			teamORB = 0 # offensive rebounds
			teamDRB = 0 # defensive rebounds
			teamBlK = 0
			teamSTL = 0
			teamAST = 0
			teamTO = 0
			teamOF = 0	# offfensive foul
			teamDF = 0	# defensive foul
			
			for pgr in self.teamGameRecord:
				teamTime += pgr.numberOfMinutesPlayed
				team2P += pgr.twoPointers
				team2PM += pgr.twoPointersMade
				team3P += pgr.threePointers
				team3PM += pgr.threePointersMade
				teamFTA += pgr.freeThrows
				teamFTM += pgr.freeThrowsMade
				teamORB += pgr.offensiveRebound
				teamDRB += pgr.defensiveRebound
				teamBlK += pgr.block
				teamSTL += pgr.steal
				teamAST += pgr.assist
				teamTO += pgr.turnover
				teamOF += pgr.offensiveFoul
				teamDF += pgr.defensiveFoul


			teamStats = {
				'totalMinutes': teamTime,
				'total2P': team2P,
				'total2PM': team2PM,
				'total2PP': round(team2PM/ team2P, 4),
				'total3P': team3P,
				'total3PM': team3PM,
				'total3PP': round(team3PM/ team3P, 4),
				'totalFGA': team2P + team3P,
				'totalFGM': team2PM + team3PM,
				'totalFGP': round((team2PM + team3PM) / (team2P + team3P), 2),
				'totalFTA': teamFTA,
				'totalFTM': teamFTM,
				'totalFTP': round(teamFTM / teamFTA, 4),
				'totalORB': teamORB,
				'totalDRB': teamDRB,
				'totalRB': teamORB + teamDRB,
				'totalBLK': teamBlK,
				'totalSTL': teamSTL,
				'totalAST': teamAST,
				'totalTO': teamTO,
				'totalOF': teamOF,
				'totalDF': teamDF
			}

			return teamStats

	def initTeamStat(self):
		self.teamStats = self.getBasicTeamStats()

	# gets another player record as input
	# Usage percentage
	def getPlayerUSG(self, playerRecord):
		# if team stats exist, then we return usage rate
		if self.teamStats:
			usg = (playerRecord.getFieldGoalAttempts() + 0.44 *playerRecord.freeThrows + playerRecord.turnover) /(self.teamStats['totalFGA'] + 0.44 * self.teamStats['totalFTA'] + self.teamStats['totalTO'])
			print(f"Usage rate of {playerRecord.name} is {round(usg, 3)}")
			return round(usg, 3)

		else:
			print("Team stats not available yet")

	############ Opponent Team not yet specified ############

	# Total Rebound Percentage
	def getPlayerTRB(self, playerRecord, opponentTeam):
		if not self.teamStats or not opponentTeam:
			print("Missing team stats or opponent team data")
		else:	
			# opponentTeam is not specified yet
			return (playerRecord.getTotalRebounds() * (self.teamStats['totalMinutes'] / 5)) / (playerRecord.numberOfMinutesPlayed * (self.teamStats['totalRB'] + opponentTeam.totalRebounds))

	# player offensive rebound
	def getPlayerORB(self, playerRecord, opponentTeam):
		if not self.teamStats or not opponentTeam:
			print("Missing team stats or opponent team data")
		else:	
			# opponentTeam is not specified yet
			return (playerRecord.offensiveRebound * (self.teamStats['totalMinutes'] / 5)) / (playerRecord.numberOfMinutesPlayed * (self.teamStats['totalORB'] + opponentTeam.totalOffensiveRebounds))		

	# player defensive rebound
	def getPlayerDRB(self, playerRecord, opponentTeam):
		if not self.teamStats or not opponentTeam:
			print("Missing team stats or opponent team data")
		else:	
			# opponentTeam is not specified yet
			return (playerRecord.defensiveRebound * (self.teamStats['totalMinutes'] / 5)) / (playerRecord.numberOfMinutesPlayed * (self.teamStats['totalDRB'] + opponentTeam.totalDefensiveRebounds))	

	############################################################

	# AST%: assist percentage
	def getPlayerASP(self, playerRecord):
		if not self.teamStats:
			print("Missing team stat")

		else:
			ast = playerRecord.assist / (playerRecord.numberOfMinutesPlayed / ((self.teamStats['totalMinutes'] / 5)) * self.teamStats['totalFGM'] - playerRecord.getFieldGoalMade())  
			print(f"Assist Percentage of {playerRecord.name} is {round(ast, 3)}")
			return round(ast, 3)
	
	# + / - ; plus minus

























