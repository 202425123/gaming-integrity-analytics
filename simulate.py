# Import necessary modules
import random
import counting

# Function to shuffle team ids n times
def shuffle_teams(teams, n):
    """Takes dictionary of teams data and n number of simulations.
    Returns a list of n dictionaries of shuffled teams.
    """
    shuffled_data = []
    # Shuffle team IDs n times
    for i in range(n):
        shuffled_teams = {}
        for match_id, teams_id in teams.items():
            # Shuffle within each match
            shuffled_teams[match_id] = {}
            # Create lists of all player IDs and team IDs
            all_players = []
            all_team_ids = []
            for team, players in teams_id.items():
                all_players.extend(players)
                all_team_ids.extend([team] * len(players))
            random.shuffle(all_team_ids)
            for player, team in zip(all_players, all_team_ids):
                if team not in shuffled_teams[match_id]:
                    shuffled_teams[match_id][team] = []
                shuffled_teams[match_id][team].append(player)
        shuffled_data.append(shuffled_teams)
    return shuffled_data

# Function to estimate simulated counts from shuffled teams
def process_shuffled_teams(cheaters, shuffled_teams_data):
    """Takes a list of cheaters data and list of shuffled teams dictionaries.
    Runs count_cheaters function on each shuffled team dictionary.
    Returns a dictionary where keys are cheater counts and values are lists of results from simulations.
    """
    simulated = {}
    for shuffled_teams in shuffled_teams_data:
        team_cheater_counts = counting.count_cheaters(cheaters, shuffled_teams)
        for cheater_count, team_count in team_cheater_counts.items():
            if cheater_count not in simulated:
                simulated[cheater_count] = []
            simulated[cheater_count].append(team_count)
    return simulated

# Function to shuffle player ids
def shuffle_players(kills, n):
    """Takes list of kills data and n number of simulations
    Shuffles player IDs within each match n times whilst keeping the timing and structure of interactions
    Returns list of n lists of shuffled kills data
    """
    simulated_data = []
    matches = {}
    # Create a dictionary of kills by match
    for match_id, killer_id, victim_id, time in kills:
        if match_id not in matches:
            matches[match_id] = []
        matches[match_id].append((killer_id, victim_id, time))
    # Shuffle players within each match
    for i in range(n):
        shuffled_players = []
        # Create a set of unique player IDs (killers and victims)
        for match_id, events in matches.items():
            player_ids = set()
            for killer_id, victim_id, time in events:
                player_ids.add(killer_id)
                player_ids.add(victim_id)
            shuffled_ids = list(player_ids)
            random.shuffle(shuffled_ids)
            # Create a dictionary mapping original player IDs to shuffled player IDs
            id_map = {original: shuffled for original, shuffled in zip(player_ids, shuffled_ids)}
            for killer_id, victim_id, time in events:
                shuffled_players.append((match_id, id_map[killer_id], id_map[victim_id], time))
        simulated_data.append(shuffled_players)
    return simulated_data

def process_shuffled_victims(cheaters, shuffled_kills_data):
    """Takes list of cheaters data and list of shuffled kills data.
    Runs count_influenced_victims function on each list of shuffled kills data.
    Returns a list of integers representing the expected influenced cheaters in each simulation.
    """
    simulated = []
    for shuffled_kills in shuffled_kills_data:
        influenced_cheaters = counting.count_influenced_victims(cheaters, shuffled_kills)
        simulated.append(influenced_cheaters)
    return simulated

def process_shuffled_observers(cheaters, shuffled_kills_data):
    """Takes list of cheaters data and list of shuffled kills data.
    Runs count_influenced_observers function on each list of shuffled kills data.
    Returns a list of integers representing the expected influenced cheaters in each simulation.
    """
    simulated = []
    for shuffled_kills in shuffled_kills_data:
        influenced_cheaters = counting.count_influenced_observers(cheaters, shuffled_kills)
        simulated.append(influenced_cheaters)
    return simulated

# Function to calculate statistics
def calculate_statistics(simulated, n):
    """Takes dictionary or list of simulated results and number of simulations.
    Calculates mean and confidence intervals for the simulated results.
    Returns mean, CI lower bound, CI upper bound.
    """
    # Calculate mean and confidence intervals for simulated worlds saved in a dictionary
    if isinstance(simulated, dict):
        results = {}
        for cheater_count, counts in simulated.items():
            mean = sum(counts) / n
            variance = sum((count - mean) ** 2 for count in counts) / (n - 1)
            std = variance ** 0.5
            ci_lower = mean - 1.96 * std / (n ** 0.5)
            ci_upper = mean + 1.96 * std / (n ** 0.5)
            results[cheater_count] = (mean, ci_lower, ci_upper)
    # Calculate mean and confidence intervals for simulated worlds saved in a list
    elif isinstance(simulated, list):
        results = []
        mean = sum(simulated) / n
        variance = sum((count - mean) ** 2 for count in simulated) / (n - 1)
        std = variance ** 0.5
        ci_lower = mean - 1.96 * std / (n ** 0.5)
        ci_upper = mean + 1.96 * std / (n ** 0.5)
        results = (mean, ci_lower, ci_upper)
    return results
