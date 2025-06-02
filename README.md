# final-project

# =========================
#     GAME INTRODUCTION
# =========================

# Game Overview
1. Title: Moon Warriors
2. Genre: Side-scrolling action shooter + mini-game
3. Tools Used: Python with Pygame
4. Battle Mechanics:  Player can attack enemies and dodge

# Game Flow
1. Menu: Show introductions and for players to enter their name.
2. Gameplay phase: Consist of battle phase and transition phase. The player need to beat every monster met on the way.
3. Ending: If the player defeats the ninth monster, they win the game. Otherwise, the game ends in failure.
4. Leaderboard: Rank players' score and used time.
5. Collection: Defeaing a monster can collect a correspond badge.

# Characters
1. Player
2. Monsters(1~9)
3. Willy in hidden Mini-game
4. Green Fish of hidden side effect

# Nothing can go wrong!
1. Discover and finish the secret task hidden within the game.
2. Eliminate monster in the every stage.
3. Survive without recovering any HP.

# Innovative Features
1. Mini-Game: Find Willy
      - Objective: Find Willy 15 times within 60 seconds
      - Distraction: Fake Willy (deducts score if touched)
      - Includes sound effects, voice lines, and background music
      - Only returns to main game upon success.
      - Once the game is passed, player gain a new Willy Bullets, which is bigger than the original ones.
      - If the player didn't find Willy, the rank drops by 1.
2. Hidden Effect: Green Fish
      - Triggered by pressing space 10 times within 5 seconds
      - Visual: A green fish grows and blocks your vision and disappear after 10 seconds automatically
3. Earn a badge for each boss you defeat.

# Controls
| Key         | Action                        |
|-------------|-------------------------------|
| W / S key   | Character movement            |
| A / D key   | Speed control                 |
| Space       | Player Attack                 |
| Q / E key   | Enter mini-game               |
| Mouse click | Shirnk Player                 |


# =========================
#     PROJECT STRUCTURE
# =========================

final_project/
├── assets/              # Game assets (images, etc.)
│ └── player.png
│ └── etc
├── main.py              # Main game loop
├── character_oh.py      # Projectile logic
├── willy.py             # Mini-game
├── score.JSON           # File I/O and saving scores
├── renew_state_display  # Display HP bar
└── greeny_effect.py     # Green Fish Effect

# ==============================
#     TECHNICAL REQUIREMENTS
# ==============================

# Basic Part
| Requirement        | Our Implementation                                                             |
|--------------------|--------------------------------------------------------------------------------|
| Basic Data Types   | Use `int`, `float`, `bool` and `none`                                          |
| String Data        | Use `strings` for player's name, monsters' name and dialog                     |
| Custom Structure   | Use `class` for player, monsters, projectiles, Willy, and Green Fish           |
| Traverse           | Track defeated monsters                                                        |
| Sort               | Levels difficulty and leaderboard                                              |
| Random             | Player's bullet, Willy's position, Cloud images selection, Monsters' movement  |
| File I/O           | Reading Image and Audio Files, Read scores from score.json                     |

# ================
#     TEAMWORK
# ================

| Member                 | Responsibility                         |
|------------------------|----------------------------------------|
| 413410007 張家馨 Joy    | Midterm Presentation, Final Presentation, Leaderboard, Image Sourcing, Player name             |
| 413410033 黃方柔 Zoe    | Midterm Presentation, Final Presentation, Find Willy, Green Fish Effect, Background music      |
| 413410057 林俞馨 Cindy  | Midterm Presentation, README, System coordination, Game loop, Character behavior, Art Design   |
| 413410069 呂慈玟 Wendy  | Midterm Presentation, Final Presentation, Trailer Video, HP bar, Collection                    |