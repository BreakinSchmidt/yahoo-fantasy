from yahoo_oauth import OAuth2
import json
import pause
import time, datetime
from datetime import date
import pytz
import argparse
import re
import yahoo_fantasy_api as yfa

parser = argparse.ArgumentParser()
parser.add_argument('--addname', type=str, required=True)
parser.add_argument('--dropname', type=str, required=True)
parser.add_argument('--leaguename', type=str, required=True)
parser.add_argument('--now', type=bool, required=False, default=False)
args = parser.parse_args()

oauth = OAuth2(None, None, from_file='/mnt/g/code/yahoo-fantasy/creds.json')

# Grabs the league ID numbers that I have hardcoded below.
# TODO: Capture the leagueId variable dynamically

# game = yfa.game.Game(oauth, 'nhl')
# leagueIds = game.league_ids(year=2022)
# print(leagueIds)


# Grab a list of the teams in a league and details. This will show the team ID numbers I
#  have hardcoded below.
# TODO: Capture the teamId variable dynamically

# league = yfa.League(oauth, b2LeagueId)
# leagueTeams = league.teams()
# print(leagueTeams)




def main():
    if args.leaguename == 'dickfoy':
        leagueId = '419.l.23876'
        teamId = '11'
    elif args.leaguename == 'b2':
        leagueId = '419.l.36232'
        teamId = '10'
    else:
        print('League name not recognized')
        exit(1)

    playerAdded = player_lookup(args.addname, leagueId)
    playerDropped = player_lookup(args.dropname, leagueId)

    playerIdAdded = playerAdded[0]
    playerIdDropped = playerDropped[0]

    playerNameAdded = playerAdded[1]
    playerNameDropped = playerDropped[1]

    print(args.now)

    print("Attempting to add", playerNameAdded, "| Attempting to drop", playerNameDropped)

# The default action is to wait until 1AM localtime.
# Take current datetime, add a day, change the time to 1AM by converting it to a string
# and then back to a datetime 
# TODO: Change to 00:01 Pacific Time to follow global Yahoo waiver time
    # if not args.now:
        
    #     print(time.daylig)
    #     waiver_time = datetime.datetime.now()
    #     waiver_time += datetime.timedelta(days=1)
    #     waiver_time = waiver_time.strftime('%y-%m-%d') + ' 00-01-15 UTC'
    #     waiver_time = datetime.datetime.strptime(waiver_time, '%y-%m-%d %H-%M-%S %Z')
    
    #     pause.until(waiver_time)
    #     print(waiver_time)

    add_drop(leagueId, teamId, playerIdAdded, playerIdDropped)

def player_lookup(name, league):
    try:
        playerDeets = yfa.League(oauth, league).player_details(name)
    except Exception:
        print("Something weird happed during player lookup. Exiting.")
        exit(1)
    
    # yfa.League lookup returns an empty json array if player isn't found
    if str(playerDeets) == "[]":
        print("Player", name, "not found")
        exit(1)

    # Count objects in the base array to get number of players returned. Exit if it finds more than one.
    playerCount = len(playerDeets)

    if playerCount > 1:
        print("I found", playerCount, "players with the name", name,"- please be more specific.")
        exit(1)
    
    playerId = playerDeets[0]['player_id']
    playerFullName = playerDeets[0]['name']['full']

    return playerId, playerFullName


# If a condition in the league prevents a player from being added or dropped, the
# reason is inserted in the "Description" XML field. Choosing to Regex that out because the returned
# XML doesn't follow some sort of standard that the xml.etree.ElementTree expects to be parsed out.

def add_drop(league, team, playerAdded, playerDropped):
    try:
        yfa.Team(oauth, league+'.t.'+team).add_and_drop_players(playerAdded, playerDropped)
    except RuntimeError as err:
        err = str(err)
        err = re.search('<description>(.*)</description>', err)
        print(err.group(1))

if __name__ == "__main__":
    main()