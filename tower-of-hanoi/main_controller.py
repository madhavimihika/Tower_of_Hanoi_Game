# main_controller.py
import pygame
import sys

class GameController:
    def __init__(self):
        pygame.init()
        self.current_screen = "menu"
        self.player_data = {}
        
    def run(self):
        """Main game loop"""
        while True:
            if self.current_screen == "menu":
                self.show_menu()
            elif self.current_screen == "player_input":
                self.get_player_info()
            elif self.current_screen == "game":
                self.play_game()
            elif self.current_screen == "exit":
                pygame.quit()
                sys.exit()
    
    def show_menu(self):
        """Show main menu"""
        from game_menu import add_tower_of_hanoi_to_menu, show_instructions
        
        choice = add_tower_of_hanoi_to_menu()
        
        if choice == '1':  # Start Game
            self.current_screen = "player_input"
        elif choice == '2':  # Instructions
            show_instructions()
            # After instructions, stay in menu
        elif choice == '3':  # Leaderboard
            print("Leaderboard screen - To be implemented")
            # Stay in menu
        elif choice == '4':  # Exit
            self.current_screen = "exit"
    
    def get_player_info(self):
        """Get player name, disks, pegs"""
        from player_input import get_player_name, select_disk_count, select_peg_count
        
        # Get player name
        name = get_player_name()
        if not name:
            self.current_screen = "menu"
            return
            
        # Get disk count
        disks = select_disk_count()
        if not disks:
            self.current_screen = "menu"
            return
            
        # Get peg count
        pegs = select_peg_count()
        if not pegs:
            self.current_screen = "menu"
            return
        
        # Store player data
        self.player_data = {
            'name': name,
            'disks': disks,
            'pegs': pegs
        }
        
        print(f"\n✅ Player registered: {name}")
        print(f"   Disks: {disks}")
        print(f"   Pegs: {pegs}")
        
        self.current_screen = "game"
    
    def play_game(self):
        """Start the actual game"""
        print(f"\n🎮 Starting Tower of Hanoi game...")
        print(f"   Player: {self.player_data['name']}")
        print(f"   Disks: {self.player_data['disks']}")
        print(f"   Pegs: {self.player_data['pegs']}")
        
        # Import and run the tower game
        try:
            from tower_ui import main as tower_main
            tower_main()
        except Exception as e:
            print(f"❌ Error starting game: {e}")
            import traceback
            traceback.print_exc()
        
        # After game, go back to menu
        print("\n📋 Game completed! Returning to menu...")
        self.current_screen = "menu"

if __name__ == "__main__":
    print("🏰 Tower of Hanoi - Game Controller")
    print("=" * 50)
    
    game = GameController()
    game.run()