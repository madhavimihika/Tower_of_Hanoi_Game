# 🏰 Tower of Hanoi Game

A Python-based implementation of the classic Tower of Hanoi puzzle with advanced features including 3 & 4 peg variations, algorithm comparisons, and player progress tracking.

## 🎮 Features

### ✅ **Core Requirements Implemented:**
- **Game Menu Integration** - Added to main game hub
- **Random Disk Selection** - 5 to 10 disks per game round
- **Peg Selection** - User chooses 3 or 4 pegs
- **Move Validation** - Ensures legal moves only
- **Multiple Algorithms** - 2 solutions for 3 pegs, 2 for 4 pegs
- **Player Progress Saving** - Name and results stored in database
- **Algorithm Timing** - Records execution time for each algorithm
- **Unit Testing** - Comprehensive test suite
- **Frame-Stewart Algorithm** - 4-peg solution implementation
- **Input Validation & Exception Handling** - Robust error management

### 🎨 **User Interface:**
- Pygame-based visual display
- Interactive tower visualization
- Player name input screen
- Real-time move tracking
- Results display with save option
- Leaderboard view

## 📁 Project Structure
feature/tower-of-hanoi/
├── 📁 UI Branch (feature/tower-of-hanoi/UI)
│ ├── game_menu.py # Add to main game hub
│ ├── tower_ui.py # Pygame visual display
│ ├── player_input.py # Player name input
│ └── results_display.py # Results & save screen
│
├── ⚙️ Algorithms Branch (feature/tower-of-hanoi/algorithms)
│ ├── three_pegs.py # 3-peg solutions
│ ├── four_pegs.py # 4-peg solutions
│ └── solver.py # Algorithm controller
│
├── 💾 Data Branch (feature/tower-of-hanoi/data)
│ ├── firebase_handler.py # Database operations
│ ├── timer.py # Algorithm timing
│ └── validation.py # Input validation
│
└── 🧪 Test Branch (feature/tower-of-hanoi/test)
├── main.py # Test runner
├── test_algorithms.py # Algorithm tests
└── test_database.py # Database tests