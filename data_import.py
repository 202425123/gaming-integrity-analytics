# Import necessary modules
from datetime import datetime

# Function to import cheaters data
def load_cheaters(fname):
    """Takes filename as input
    Returns list of cheaters data
    """
    data= []
    with open(fname, 'r') as f:
        for line in f.readlines():
            player_id, start, ban = line.strip().split('\t')
            data.append([player_id,
                        datetime.strptime(start, "%Y-%m-%d"),
                        datetime.strptime(ban, "%Y-%m-%d")])
    return data

# Function to import team data
def load_teams(fname):
    """Takes filename as input
    Returns dictionary of team data
    """
    data = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            match_id, player_id, team_id = line.strip().split('\t')
            if match_id not in data:
                data[match_id] = {}
            if team_id not in data[match_id]:
                data[match_id][team_id] = []
            data[match_id][team_id].append(player_id)
    return data

# Function to import interaction data
def load_interaction(fname):
    """Takes filename as input
    Returns list of interaction data
    """
    data= []
    with open(fname, 'r') as f:
        for line in f.readlines():
            match_id, killer_id, victim_id, time = line.strip().split('\t')
            data.append([match_id,
                        killer_id,
                        victim_id,
                        datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")])
    return data
