## Cricket Practical - OOPS

# INDIAN CRICKET TEAM - OOPs Practice

# Topics covered: Class, Object, **init**, Instance attributes,

# Instance methods, Inheritance, super(), Classroom-style container

# ============================================================

# CHALLENGE 1 — Base Class

# ============================================================

# Create a Cricketer class with:

# Attributes : name, matches, runs (list of runs per match)

# Methods :

# calculate_average() → total runs / matches played

# display_profile() → print all details including average

#

# Test it:

# c1 = Cricketer("Virat Kohli", 10, [82, 45, 120, 33, 67, 90, 55, 110, 23, 78])

# c1.display_profile()

# ============================================================

# CHALLENGE 2 — Edge Case

# ============================================================

# What if matches = 0 ?

# Handle ZeroDivisionError in calculate_average()

# Test it:

# c2 = Cricketer("New Player", 0, [])

# c2.display_profile()

# ============================================================

# CHALLENGE 3 — Inheritance

# ============================================================

# Create AllRounder(Cricketer) with extra attribute: wickets

# Override display_profile() to show wickets too

# Use super() — don't rewrite existing logic

#

# Test it:

# ar1 = AllRounder("Hardik Pandya", 8, [55, 30, 70, 20, 45, 60, 35, 40], 12)

# ar1.display_profile()

# ============================================================

# CHALLENGE 4 — Container Class

# ============================================================

# Create a Team class (NO inheritance — just contains players)

# Attributes : team_name, players (empty list)

# Methods :

# add_player(player) → add to list

# top_scorer() → player with highest average

# team_average() → average of all player averages

# display_squad() → display_profile() of every player

#

# Test it:

# india = Team("India")

# india.add_player(c1)

# india.add_player(ar1)

# india.display_squad()

# print("Top Scorer:", india.top_scorer().name)

# print("Team Average:", india.team_average())

# ============================================================

# CHALLENGE 5 — **str** Magic Method

# ============================================================

# Add **str** to Cricketer class

# So this prints nicely:

# print(india.top_scorer())

# Expected output → "Virat Kohli | Avg: 70.3 | Matches: 10"

# ============================================================

# CHALLENGE 6 — Class Attribute

# ============================================================

# Add a class attribute to Cricketer:

# total_cricketers = 0 → increases by 1 every time a new object is created

#

# Test it:

# print(Cricketer.total_cricketers) # should print total objects created

# ============================================================

# CHALLENGE 7 — Defensive Thinking

# ============================================================

# What if someone does this:

# india.add_player("Rohit Sharma") # string instead of object

# team_average() will crash

# Add a check in add_player() — only add if it's a Cricketer instance

# Hint: isinstance()

# ============================================================

# CHALLENGE 8 — List Comprehension

# ============================================================

# Add a method in Team:

# top_performers() → return list of players with average > 50

# Use list comprehension — one line only

# Print their names

# ============================================================

# CHALLENGE 9 — Sorting

# ============================================================

# Add a method in Team:

# leaderboard() → print all players sorted by average (highest first)

# Hint: sorted() with key and reverse=True

# ============================================================

# CHALLENGE 10 — Real Thinking

# ============================================================

# Rohit Sharma played 5 matches but his runs list has only 3 entries

# c3 = Cricketer("Rohit Sharma", 5, [90, 110, 85])

# Your calculate_average() uses matches in denominator

# But len(runs) = 3, not 5

# Which one should you use — matches or len(runs)?

# Think, decide, implement, explain in a comment WHY you chose it
