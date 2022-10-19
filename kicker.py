#for now assume that players can be found by name and location, in prnciple unique ids should be used
import yaml


class PlayerDataBase:
    data_base_filename = ''

    def __init__(self,data_base_filename):
        self.data_base_filename = data_base_filename 
    
    def createPlayerEntry(self,player):
        data_base_file = open(self.data_base_filename, 'a')
        data_base_file.write(player.getName() + '\n' + player.getLocation() + '\n' + str(player.getStatistics()) + '\n')
        data_base_file.close()

#lower vs upper case etc        
    def getPlayerEntry(self,name,location):
        player = Player(name,location)
        data_base_file = open(self.data_base_filename, 'r')
        data_base_content = data_base_file.readlines()
        data_base_file.close()
        player_found = False
        for i in range(0,len(data_base_content),3):
            current_name = data_base_content[i].replace('\n','')
            current_location = data_base_content[i+1].replace('\n','')
            if current_name == name and current_location == location:
                player_statistics = yaml.load(data_base_content[i+2].replace('\n',''))
                player.setStatistics(player_statistics)
                player_found = True
        if player_found == False:
            self.createPlayerEntry(player)
            print("Player was not found. A new player has been created.")
        return player

    
    def updatePlayerEntry(self,location,player,position,result):
        data_base_file = open(self.data_base_filename, 'r')
        data_base_content = data_base_file.readlines()
        data_base_file.close()
        player_name = player.getName()
        player_location = player.getLocation()
        for i in range(0,len(data_base_content),3):
            current_name = data_base_content[i].replace('\n','')
            current_location = data_base_content[i+1].replace('\n','')
            if current_name == player_name and current_location == player_location:
                player_statistics = yaml.load(data_base_content[i+2].replace('\n',''))
                win_loss_list = playerStatistics[location,position]
                if result == 1:
                    win_loss_list[0] += 1
                else:
                    win_loss_list[1] += 1
                playerStatistics[location,position] = win_loss_list
                data_base_content[i+2] = str(playerStatistics)
        data_base_file = open(self.data_base_filename, 'w')
        data_base_file.write(''.join(data_base_content))
        data_base_file.close()
        
                


class Player:

    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.playerStatistics = {'Munich': {'front':[0,0],'back':[0,0]},'Berlin': {'front':[0,0],'back':[0,0]},'Wurzburg': {'front':[0,0],'back':[0,0]}}
        self.current_position = ''

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getStatistics(self):
        return self.playerStatistics

    def setStatistics(self,statistics):
        self.playerStatistics = statistics

    def setCurrentPosition(self,position):
        self.current_position = position

        
        


class GameDataBase:
    data_base_filename = ''

    def __init__(self,data_base_filename):
        self.data_base_filename = data_base_filename 
    
    def createGameEntry(self,game):
        data_base_file = open(self.data_base_filename, 'a')
        data_base_file.write(game.getDate() + ' ' + game.getTime() + '\n')
        data_base_file.write('Team 1: ' + game.getTeam1().getPlayer(0).getName() + ' ' +  game.getTeam1().getPlayer(1).getName() + '\n')
        data_base_file.write('Team 2: ' + game.getTeam2().getPlayer(0).getName() + ' ' + game.getTeam2().getPlayer(1).getName() + '\n')
        data_base_file.write('Mode: ' + game.getMode() + '\n')
        data_base_file.write('Overall Winner: ' + game.getWinner() + '\n')
        matches = game.getMatches()
        i = 0
        for i in range(len(matches)):
            data_base_file.write('  Match ' + str(i+1) + ': \n')
            data_base_file.write('    Team 1: \n')
            data_base_file.write('    ' + matches[i].getTeam1().getPlayer(0).getName() + ' at position ' + matches[i].getPositions1(0) + '\n')
            data_base_file.write('    ' + matches[i].getTeam1().getPlayer(1).getName() + ' at position ' + matches[i].getPositions1(1) + '\n')
            data_base_file.write('    Team 2: \n')
            data_base_file.write('    ' + matches[i].getTeam2().getPlayer(0).getName() + ' at position ' + matches[i].getPositions2(0) + '\n')
            data_base_file.write('    ' + matches[i].getTeam2().getPlayer(1).getName() + ' at position ' + matches[i].getPositions2(1) + '\n')
            data_base_file.write('    Winner: ' + matches[i].getWinner() + '\n')
        data_base_file.close()
            
            
            
            
class Game:

#need to catch non-allowed formats and locations
    def playGame(self):
        self.matches = []
        print("Please enter the date: ")
        self.date = input()
        print("Please enter the current time: ")
        self.time = input()
        print("Please enter the current location: ")
        self.location = input()
        team1 = Team(player_database)
        team2 = Team(player_database)
        self.teams = [team1,team2]
        for i in range(2):
            for j in range(2):
                print("Please enter the name of player " + str(j+1) + " in team " + str(i+1) + ": ")
                name = input()
                print("Please enter the site of player " + str(j+1) + " in team " + str(i+1) + ": ")
                site = input()
                self.teams[i].addPlayer(name,site)                
        print("Please enter the mode of the game (One-Match = 1/BestOf3 = 2/BestOf5 = 3): ")
        self.mode = input()
        if(self.mode == '1'):
            self.matches = self.playOneMatch()
        elif(self.mode == '2'):
            self.matches = self.playBestOf3()
        elif(self.mode == '3'):
            self.matches = self.playBestOf5()
        else:
            print("This mode has not been implemented yet!")
        self.setWinner()
        self.updatePlayerStatistics()

    def updatePlayerStatistics(self):
        for match in self.matches:
            player1 = self.teams[0].getPlayer(0)
            player2 = self.teams[0].getPlayer(1)
            player3 = self.teams[1].getPlayer(0)
            player4 = self.teams[1].getPlayer(1)
            if match.getResult() == 0:
                self.teams[0].updateStatistics(self.location,player1,match.getPositions1(0),1)
                self.teams[0].updateStatistics(self.location,player2,match.getPositions1(1),1)
                self.teams[1].updateStatistics(self.location,player3,match.getPositions2(0),0)
                self.teams[1].updateStatistics(self.location,player4,match.getPositions2(1),0)
            else:
                self.teams[0].updateStatistics(self.location,player1,match.getPositions1(0),0)
                self.teams[0].updateStatistics(self.location,player2,match.getPositions1(1),0)
                self.teams[1].updateStatistics(self.location,player3,match.getPositions2(0),1)
                self.teams[1].updateStatistics(self.location,player4,match.getPositions2(1),1)
        

    def getTime(self):
        return self.time

    def getDate(self):
        return self.date

    def getLocation(self):
        return self.location

    def getTeam1(self):
        return self.teams[0]

    def getTeam2(self):
        return self.teams[1]
    
    def getMode(self):
        if self.mode == '1':
            return "One-Match"
        elif self.mode == '2':
            return "BestOf3"
        elif self.mode == '3':
            return "BestOf5"
        else:
            return "mode unknown"
        

    def getMatches(self):
        return self.matches

    def setWinner(self):
        total = 0
        for match in self.matches:
            total = total + match.getResult()
        if(self.mode == '1'):
            if total == 0:
                self.winner = 'Team 1'
            else:
                self.winner = 'Team 2'
        elif(self.mode == '2'):
            if total < 2:
                self.winner = 'Team 1'
            else:
                self.winner = 'Team 2'
        elif(self.mode == '3'):
            if total < 3:
                self.winner = 'Team 1'
            else:
                self.winner = 'Team 2'
        else:
            print("Mode not implemented! Winner cannot be set!")
        
            
    def getWinner(self):
        return self.winner
            
        
    def playOneMatch(self):
        match = Match(self.teams[0],self.teams[1])
        match.assignPositions()
        match.requestResult()
        return [match]

    def playBestOf3(self):
        match1 = Match(self.teams[0],self.teams[1])
        match1.assignPositions()
        match1.requestResult()
        match2 = Match(self.teams[0],self.teams[1])
        match2.assignPositions()
        match2.requestResult()
        match3 = Match(self.teams[0],self.teams[1])
        match3.assignPositions()
        match3.requestResult()
        return [match1,match2,match3]

    def playBestOf5(self):
        match1 = Match(self.teams[0],self.teams[1])
        match1.assignPositions()
        match1.requestResult()
        match2 = Match(self.teams[0],self.teams[1])
        match2.assignPositions()
        match2.requestResult()
        match3 = Match(self.teams[0],self.teams[1])
        match3.assignPositions()
        match3.requestResult()
        match4 = Match(self.teams[0],self.teams[1])
        match4.assignPositions()
        match4.requestResult()
        match5 = Match(self.teams[0],self.teams[1])
        match5.assignPositions()
        match5.requestResult()
        return [match1,match2,match3,match4,match5]
        


#teams are assumed to be ordered
class Match:
    
    def __init__(self,team1,team2):
        self.team1 = team1
        self.team2 = team2
        self.positions1 = []
        self.positions2 = []

    
    def assignPositionsForTeam(self,positions,team):
        position = ''
        while position != 'b' and position != 'f':
            print("Assign the position of: " + team.getPlayer(0).getName() + " (f/b):")
            position = input()
        if position == 'f':
            positions.append('front')
            positions.append('back')
        else:
            positions.append('back')
            positions.append('front')
    
    def assignPositions(self):
        self.assignPositionsForTeam(self.positions1,self.team1)
        self.assignPositionsForTeam(self.positions2,self.team2)


    def requestResult(self):
        print("Please enter the number of goals scored by team 1:")
        goals_for_team1 = input()
        print("Please enter the number of goals scored by team 2:")
        goals_for_team2 = input()
        self.setResult(goals_for_team1,goals_for_team2)
        

#result = 0 means team1 won, result = 1 means team 2 won
#need to catch equal results
    def setResult(self,score1,score2):
        result = 0
        if score1 < score2:
            result = 1
        self.result = result

    def getResult(self):
        return self.result

    def getPositions1(self,id):
        return self.positions1[id]

    def getPositions2(self,id):
        return self.positions2[id]

    def getTeam1(self):
        return self.team1

    def getTeam2(self):
        return self.team2

    def getWinner(self):
        if self.result == 0:
            return "Team 1"
        else:
            return "Team 2"
        

#would be nice to be able to remove or replace players
class Team:

    def __init__(self,database):
        self.database = database
        self.players = []
    
    def addPlayer(self,name,location):
        if len(self.players) > 1:
            print("There are already 2 players in this team!")
        else:
            newPlayer = self.database.getPlayerEntry(name,location)
            self.players.append(newPlayer)

    def getPlayer(self,id):
        if id > 1:
            print("Id out of range. Returning player 1.")
            return self.players[0]
        return self.players[id]
    
    
    def updateStatistics(self,location,player,position,result):
        self.database.updatePlayerEntry(location,player,position,result)
        
        
        
        
        

player_database = PlayerDataBase('Players.txt')
game_data_base = GameDataBase("Games.txt")

#create some players and add to database

#myPlayer1 = Player('Benjamin Summ','Wurzburg')
#myPlayer2 = Player('Tom Wiesseckel','Munich')
#myPlayer3 = Player('Marcel Idler','Berlin')
#myPlayer4 = Player('Stefanie Osswald','Berlin')
#player_database.createPlayerEntry(myPlayer1)
#player_database.createPlayerEntry(myPlayer2)
#player_database.createPlayerEntry(myPlayer3)
#player_database.createPlayerEntry(myPlayer4)

#create teams and add players

#team1 = Team(player_database)
#team1.addPlayer('Benjamin Summ','Wurzburg')
#team1.addPlayer('Tom Wiesseckel','Munich')
#team2 = Team(player_database)
#team2.addPlayer('Marcel Idler','Berlin')
#team2.addPlayer('Stefanie Osswald','Berlin')

#start match

#myMatch = Match(team1,team2)
#myMatch.assignPositions()

myGame = Game()
myGame.playGame()
game_data_base.createGameEntry(myGame)
