import random
import time

# Seed for reproducibility
random.seed(64)

# Example list of teams in each pot
pot1 = [f'Team_{i+1}' for i in range(16)]  # 10 teams in pot 1
pot2 = [f'Team_{i+16}' for i in range(16)]  # 10 teams in pot 2
pot3 = [f'Team_{i+32}' for i in range(16)]  # 10 teams in pot 3
pot4 = [f'Team_{i+48}' for i in range(16)]  # 12 teams in pot 4

# Shuffle the teams within each pot
random.shuffle(pot1)
random.shuffle(pot2)
random.shuffle(pot3)
random.shuffle(pot4)

# Number of groups (should be equal to len(pot1))
n_groups = len(pot1)

# Initialize the groups as empty lists
groups = [[] for _ in range(n_groups)]

print("Assigning teams to groups...\n")
for i in range(n_groups):
    # Assign and reveal one team from each pot
    groups[i].append(pot1[i])
    print(f"Group {i+1} gets {pot1[i]} from Pot 1")
    time.sleep(1)  # Pause to simulate reveal

    groups[i].append(pot2[i])
    print(f"Group {i+1} gets {pot2[i]} from Pot 2")
    time.sleep(1)  # Pause to simulate reveal

    groups[i].append(pot3[i])
    print(f"Group {i+1} gets {pot3[i]} from Pot 3")
    time.sleep(1)  # Pause to simulate reveal

# Distribute remaining pot4 teams across the groups, revealing them one by one
for i in range(n_groups):
    if i < len(pot4):
        groups[i].append(pot4[i])
        print(f"Group {i+1} gets {pot4[i]} from Pot 4")
        time.sleep(1)  # Pause to simulate reveal

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
