"""
test_pygame.py - Test the beautiful Pygame UI
"""
import pygame
import sys
import os

def test_game_menu():
    """Test the game menu"""
    print("Testing Game Menu...")
    from game_menu import add_tower_of_hanoi_to_menu, show_instructions
    
    choice = add_tower_of_hanoi_to_menu()
    print(f"Menu choice: {choice}")
    
    if choice == '2':
        show_instructions()
    
    pygame.quit()
    return True

def test_player_input():
    """Test player input screens"""
    print("\nTesting Player Input...")
    from player_input import get_player_name, select_disk_count, select_peg_count
    
    # Test each screen
    name = get_player_name()
    print(f"Player Name: {name}")
    
    if name:
        disks = select_disk_count()
        print(f"Disks: {disks}")
        
        if disks:
            pegs = select_peg_count()
            print(f"Pegs: {pegs}")
    
    pygame.quit()
    return True

def test_tower_ui():
    """Test the tower visualization"""
    print("\nTesting Tower UI...")
    try:
        from tower_ui import main
        main()
        return True
    except Exception as e:
        print(f"Error in tower UI: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Testing Beautiful Pygame UI for Tower of Hanoi")
    print("="*60)
    
    print("\n1. Starting Game Menu Test...")
    pygame.init()
    test_game_menu()
    
    print("\n2. Starting Player Input Test...")
    pygame.init()
    test_player_input()
    
    print("\n3. Starting Tower UI Test...")
    pygame.init()
    test_tower_ui()
    
    print("\n" + "="*60)
    print("All Pygame UI tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()