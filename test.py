from yahoo_oauth import OAuth2
import json
import yahoo_fantasy_api as yfa

oauth = OAuth2(None, None, from_file='/mnt/g/code/yahoo-fantasy/creds.json')
dickfoyLeagueId = "419.l.23876"
dickfoyTeamId = "11"
b2LeagueId = "419.l.36232"
b2TeamId = "10"
dropPlayerId = "5991"
addPlayerId = "6756"

# game = yfa.game.Game(oauth, 'nhl')
# game_ids = game.league_ids(year=2022)
# print(game_ids)

# Grab a list of the teams in a league and details
# league = yfa.League(oauth, b2LeagueId)
# leagueTeams = league.teams()
# print(leagueTeams)

# Grab a roster of a specified team (Max Domi: 5991 | Debrusk: 6756 )
# teamRoster = yfa.Team(oauth, b2LeagueId+'.t.'+b2TeamId).roster()
# print(json.dumps(teamRoster, indent=1))

# Grab the info of a specifc player
# playerDeets = yfa.League(oauth, b2LeagueId).player_details('Jake Debrusk')
# print(json.dumps(playerDeets, indent=1))

# Drop and Add
yfa.Team(oauth, b2LeagueId+'.t.'+b2TeamId).add_and_drop_players(addPlayerId, dropPlayerId)

