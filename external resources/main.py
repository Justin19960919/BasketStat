from playerStat import PlayerGameRecord
from team import TeamGameRecord

player1 = PlayerGameRecord("A", 1, 20, 3, 2)
player2 = PlayerGameRecord("B", 2, 25, 1, 1, 5, 1)
player3 = PlayerGameRecord("C", 3, 28, 9, 3, 0, 0, 2, 2, 0, 7, 1, 0, 1, 0, 0, 2)
player4 = PlayerGameRecord("D", 4, 25, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3)
player5 = PlayerGameRecord("E", 5, 3)
player6 = PlayerGameRecord("F", 6, 1)
player7 = PlayerGameRecord("G", 7, 10, 6, 1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 2)
player8 = PlayerGameRecord("H", 8, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
player9 = PlayerGameRecord("I", 9, 6, 2, 1, 2, 0)
player10 = PlayerGameRecord("J", 10, 10, 0, 0, 1, 1)
player11 = PlayerGameRecord("K", 11, 20, 0, 0, 1, 1)
player12 = PlayerGameRecord("L", 12, 25, 7, 1, 2, 0, 0, 0, 0, 1,0, 0, 2, 0, 0)


print(player1)
print(player2)
print(player3)
print(player4)
print(player5)
print(player6)
print(player7)
print(player8)
print(player9)
print(player10)
print(player11)
print(player12)



team = TeamGameRecord()
team.addPlayerRecord(player1)
team.addPlayerRecord(player2)
team.addPlayerRecord(player3)
team.addPlayerRecord(player4)
team.addPlayerRecord(player5)
team.addPlayerRecord(player6)
team.addPlayerRecord(player7)
team.addPlayerRecord(player8)
team.addPlayerRecord(player9)
team.addPlayerRecord(player10)
team.addPlayerRecord(player11)
team.addPlayerRecord(player12)

team.initTeamStat()
print(team.teamStats)
team.getPlayerUSG(player1)
# team.getPlayerTRB(player1)
# team.getPlayerORB(player1)
# team.getPlayerDRB(player1)
team.getPlayerASP(player1)
team.getPlayerASP(player12)


