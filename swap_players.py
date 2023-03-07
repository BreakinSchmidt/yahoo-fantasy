from yahoo_oauth import OAuth2
import json
import argparse
import re
import yahoo_fantasy_api as yfa

parser = argparse.ArgumentParser()
parser.add_argument('--addname', type=str, required=False, default='')
parser.add_argument('--dropname', type=str, required=False, default='')
parser.add_argument('--leaguename', type=str, required=True)
args = parser.parse_args()

oauth = OAuth2(None, None, from_file='creds.json')

# Snippet below grabs the league ID numbers that I have hardcoded in main.
# TODO: Capture the leagueId variable programmatically

# game = yfa.game.Game(oauth, 'nhl')
# leagueIds = game.league_ids(year=2022)
# print(leagueIds)

# Snippet below grabs list of the teams in a league and details. This will show the team ID numbers I harcoded in main.
# TODO: Capture the teamId variable programmatically

# league = yfa.League(oauth, b2LeagueId)
# leagueTeams = league.teams()
# print(leagueTeams)3

def main():
    # Define the league info that I've manually grabbed from the yfa_init_oatuh_env.py script.
    if args.leaguename == 'dickfoy':
        leagueId = '419.l.23876'
        teamId = '11'
    elif args.leaguename == 'b2':
        leagueId = '419.l.36232'
        teamId = '10'
    else:
        print('League name not recognized')
        exit(1)

    # Figure out if were adding, dropping, or swapping a player

    if (args.addname == '') and (args.dropname == ''):
        print('You need to specify a player to add, drop, or both.')
        exit(1)
    elif (args.addname ==''):
        action = "drop"
    elif (args.dropname ==''):
        action = "add"
    else:
        action = "swap"

    # Turn the user input into a format readable by the API and print the attempted action

    if (action == 'swap') or (action == 'add'):
        playerAdded = player_lookup(args.addname, leagueId)
        playerIdAdded = playerAdded[0]
        playerNameAdded = playerAdded[1]
        print("Attempting to add", playerNameAdded)

    if (action == 'swap') or (action == 'drop'):
        playerDropped = player_lookup(args.dropname, leagueId)
        playerIdDropped = playerDropped[0]
        playerNameDropped = playerDropped[1]
        print("Attempting to drop", playerNameDropped)

    # Execute the action
    
    if action == "swap":
        add_drop(leagueId, teamId, playerIdAdded, playerIdDropped)
    elif action == "add":
        add(leagueId, teamId, playerIdAdded)
    elif action == "drop":
        drop(leagueId, teamId, playerIdDropped)


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

def add(league, team, playerAdded):
    try:
        yfa.Team(oauth, league+'.t.'+team).add_player(playerAdded)
    except RuntimeError as err:
        err = str(err)
        err = re.search('<description>(.*)</description>', err)
        print(err.group(1))

def drop(league, team, playerDropped):
    try:
        yfa.Team(oauth, league+'.t.'+team).drop_player(playerDropped)
    except RuntimeError as err:
        err = str(err)
        err = re.search('<description>(.*)</description>', err)
        print(err.group(1))

if __name__ == "__main__":
    main()