import random
import time

# Seed for reproducibility
random.seed(42)

# Example list of teams in each pot with strength scores
pot1 = {f'Team_{i+1}': random.randint(70, 100) for i in range(10)}  # Strength between 70 and 100
pot2 = {f'Team_{i+11}': random.randint(50, 80) for i in range(10)}  # Strength between 50 and 80
pot3 = {f'Team_{i+21}': random.randint(30, 60) for i in range(10)}  # Strength between 30 and 60
pot4 = {f'Team_{i+31}': random.randint(10, 40) for i in range(12)}  # Strength between 10 and 40

# Shuffle the teams within each pot (preserving their strength scores)
pot1 = dict(random.sample(list(pot1.items()), len(pot1)))
pot2 = dict(random.sample(list(pot2.items()), len(pot2)))
pot3 = dict(random.sample(list(pot3.items()), len(pot3)))
pot4 = dict(random.sample(list(pot4.items()), len(pot4)))

# Number of groups (should be equal to len(pot1))
n_groups = len(pot1)

# Initialize the groups as empty lists
groups = [[] for _ in range(n_groups)]

# Function to perform weighted random selection
def weighted_choice(teams):
    total = sum(score for team, score in teams.items())
    r = random.uniform(0, total)
    upto = 0
    for team, score in teams.items():
        if upto + score >= r:
            return team
        upto += score

# Assign teams to groups, revealing them one by one
print("Assigning teams to groups...\n")
for i in range(n_groups):
    # Select and assign one team from each pot based on their strength
    team1 = weighted_choice(pot1)
    groups[i].append(team1)
    del pot1[team1]  # Remove selected team from the pot
    print(f"Group {i+1} gets {team1} from Pot 1")
    time.sleep(1)  # Pause to simulate reveal

    team2 = weighted_choice(pot2)
    groups[i].append(team2)
    del pot2[team2]  # Remove selected team from the pot
    print(f"Group {i+1} gets {team2} from Pot 2")
    time.sleep(1)  # Pause to simulate reveal

    team3 = weighted_choice(pot3)
    groups[i].append(team3)
    del pot3[team3]  # Remove selected team from the pot
    print(f"Group {i+1} gets {team3} from Pot 3")
    time.sleep(1)  # Pause to simulate reveal

# Distribute remaining pot4 teams across the groups, revealing them one by one
for i in range(n_groups):
    if pot4:
        team4 = weighted_choice(pot4)
        groups[i].append(team4)
        del pot4[team4]  # Remove selected team from the pot
        print(f"Group {i+1} gets {team4} from Pot 4")
        time.sleep(1)  # Pause to simulate reveal

# Display the final groups
print("\nFinal Groups:")
for i, group in enumerate(groups):
    print(f"Group {i+1}: {group}")

# Display the final groups
print("\nFinal Groups:")
for i, group in enumerate(groups):
    print(f"Group {i+1}: {group}")

group_results = {}
for i, group in enumerate(groups):
    group_results[i+1] = {team: random.randint(0, 9) for team in group}  # Points between 0 and 9


# Display group stage results
print("Group Stage Results:")
for group_id, results in group_results.items():
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print(f"Group {group_id}:")
    for team, points in sorted_results:
        print(f"{team}: {points} points")
    print()

# Determine the top 2 teams from each group
top_teams = []
for group_id, results in group_results.items():
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    top_teams.extend([sorted_results[0][0], sorted_results[1][0]])  # Top 2 teams

# Display top teams advancing to playoffs
print("Teams Advancing to Playoffs:")
for i, team in enumerate(top_teams, 1):
    print(f"{i}. {team}")

# Simulate playoffs (knockout stage)
random.shuffle(top_teams)  # Shuffle the top teams for random pairings

# Playoff pairings
print("\nPlayoff Matchups and Results:")
while len(top_teams) > 1:
    team1 = top_teams.pop(0)
    team2 = top_teams.pop(0)
    winner = random.choice([team1, team2])
    print(f"{team1} vs {team2} -> Winner: {winner}")
    top_teams.append(winner)  # Winner advances to the next round

# Final winner
champion = top_teams[0]
print(f"\nChampion: {champion}")