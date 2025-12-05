# main.py - FIXED VERSION (no emoji)
print("=" * 50)
print("TOWER OF HANOI GAME")
print("=" * 50)
print("Starting the game...")

try:
    from main_controller import GameController
    game = GameController()
    game.run()
except ImportError as e:
    print(f"ERROR: {e}")
    print("\nMake sure you have these files:")
    print("1. game_menu.py")
    print("2. player_input.py") 
    print("3. tower_ui.py")
    print("4. main_controller.py")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to exit...")