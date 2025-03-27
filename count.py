# Import necessary modules
import random

# Function to count cheaters per team
def count_cheaters(cheaters, teams):
    """Takes list of cheaters data and a dictionary of teams data
    Returns dictionary of cheater counts per team
    """
    # Create a set of cheater IDs to facilitate search
    cheater_ids = {cheater for cheater, start, ban in cheaters}
    cheaters_per_team = {}
    for match_id, teams_id in teams.items():
        for team, players in teams_id.items():
            num_cheaters = sum(1 for player in players if player in cheater_ids)
            # Add X number of cheaters into dictionary (if not already added)
            if num_cheaters not in cheaters_per_team:
                cheaters_per_team[num_cheaters] = 0
            # Increment the count of teams with X number of cheaters
            cheaters_per_team[num_cheaters] += 1
    # Sorts the dictionary by team size
    sorted_cheaters_per_team = dict(sorted(cheaters_per_team.items()))
    return sorted_cheaters_per_team

# Function to determine match start dates
def get_match_times(kills_data):
    """Takes list of kills data
    Calculates the start and end times of each match based on the first and last kill
    Returns dictionary of match start and end times
    """
    match_times = {}
    for match_id, killer_id, victim_id, time in kills_data:
        if match_id not in match_times:
            match_times[match_id] = {"start": time, "end": time}
        else:
            # Start time is the first kill in match
            if time < match_times[match_id]["start"]:
                match_times[match_id]["start"] = time
            # End time is the last kill in match
            if time > match_times[match_id]["end"]:
                match_times[match_id]["end"] = time
    return match_times

def count_influenced_victims(cheaters_data, kills_data):
    """Takes cheaters data and kills data
    Estimates the number of victims influenced to be cheaters by other cheaters while accounting for dead players
    Returns integer representing the number of influenced cheaters
    """
    cheaters_dict = {cheater_id: {"start_date": start_date, "ban_date": ban_date} for cheater_id, start_date, ban_date in cheaters_data}
    match_times = get_match_times(kills_data)
    influenced_cheaters = set()
    dead_players_by_match = {}
    for match_id, killer, victim, time in kills_data:
        # Add dead players set for this match (if not already added)
        if match_id not in dead_players_by_match:
            dead_players_by_match[match_id] = set()
        # Skip if the victim is already dead
        if victim in dead_players_by_match[match_id]:
            continue
        # Mark the victim as dead
        dead_players_by_match[match_id].add(victim)
        # Check if the killer is an active cheater at the match start time
        match_start = match_times[match_id]["start"]
        if killer in cheaters_dict:
            cheat_start_date = cheaters_dict[killer]["start_date"]
            if cheat_start_date <= match_start:
                # Check if the victim starts cheating after the match
                if victim in cheaters_dict:
                    victim_cheat_start = cheaters_dict[victim]["start_date"]
                    if victim_cheat_start >= match_start:
                        influenced_cheaters.add(victim)
    return len(influenced_cheaters)

def count_influenced_observers(cheaters, kills):
    """Takes lists of cheaters and kills data
    Estimates the number of observers of cheating influenced to be cheaters
    Returns integer representing the number of influenced observers
    """
    # Reorganize cheaters data by player ID
    cheater_times = {player_id: (cheat_start_time, cheat_ban_time) for player_id, cheat_start_time, cheat_ban_time in cheaters}

    # Reorganize kills data by match and killer
    matches = {}
    for match_id, killer_id, victim_id, kill_time in kills:
        if match_id not in matches:
            matches[match_id] = {}
        if killer_id not in matches[match_id]:
            matches[match_id][killer_id] = []
        matches[match_id][killer_id].append((victim_id, kill_time))

    # Function to check if a player is actively cheating
    def is_cheater_active(player_id, time):
        """Takes player ID and time
        Checks if the player is actively cheating at the given time
        Returns boolean"""
        if player_id in cheater_times:
            start, ban = cheater_times[player_id]
            return start <= time < ban
        return False
    
    count = 0
    counted_players = set()

    for match_id, graph in matches.items():
        for killer_id, kill_events in graph.items():
            # Skip killers who are not actively cheating at the time of their kills
            if not any(is_cheater_active(killer_id, kill_time) for victim, kill_time in kill_events):
                continue
            
            # Check if the killer has at least 3 kills
            for i, (victim_id, kill_time) in enumerate(kill_events):
                prior_kills = 0
                for j in range(i): 
                    prior_victim, prior_kill_time = kill_events[j]
                    if prior_kill_time < kill_time:
                        prior_kills += 1
                if prior_kills >= 3:
                    # Check if the victim was not cheating at the time of the kill
                    if victim_id not in counted_players and victim_id in cheater_times:
                        start_time, ban = cheater_times[victim_id]
                        if not is_cheater_active(victim_id, kill_time) and start_time > kill_time:
                            count += 1
                            counted_players.add(victim_id)

    return count
