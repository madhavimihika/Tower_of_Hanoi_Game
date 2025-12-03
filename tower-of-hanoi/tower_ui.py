"""
tower_ui.py - Beautiful Tower of Hanoi visualization with Pygame
"""
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Game")

# Colors
BACKGROUND = (15, 15, 25)
TOWER_COLOR = (180, 160, 140)
BASE_COLOR = (139, 69, 19)
DISK_COLORS = [
    (231, 76, 60),    # Red
    (230, 126, 34),   # Orange
    (241, 196, 15),   # Yellow
    (46, 204, 113),   # Green
    (52, 152, 219),   # Blue
    (155, 89, 182),   # Purple
    (52, 73, 94),     # Dark Blue
    (26, 188, 156),   # Teal
    (149, 165, 166),  # Gray
    (243, 156, 18)    # Dark Orange
]
TEXT_COLOR = (236, 240, 241)
HIGHLIGHT = (255, 255, 100)
SHADOW = (10, 10, 15)

# Fonts
try:
    title_font = pygame.font.Font("assets/fonts/retro.ttf", 36)
    info_font = pygame.font.Font("assets/fonts/retro.ttf", 24)
    move_font = pygame.font.Font("assets/fonts/retro.ttf", 28)
except:
    title_font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 24)
    move_font = pygame.font.Font(None, 28)

class TowerOfHanoiUI:
    """Beautiful Tower of Hanoi visualization"""
    def __init__(self, disks=5, pegs=3, player_name="Player"):
        self.disks = disks
        self.pegs = pegs
        self.player_name = player_name
        self.towers = self.initialize_towers()
        self.move_count = 0
        self.selected_disk = None
        self.selected_peg = None
        self.animation_queue = []
        self.is_animating = False
        self.animation_progress = 0
        self.move_history = []
        
        # Tower positions
        self.base_y = 650
        self.tower_height = 400
        self.peg_spacing = SCREEN_WIDTH // (pegs + 1)
        self.disk_height = 30
        
        # Buttons
        self.buttons = {
            'solve': pygame.Rect(50, 700, 150, 50),
            'reset': pygame.Rect(220, 700, 150, 50),
            'undo': pygame.Rect(390, 700, 150, 50),
            'hint': pygame.Rect(560, 700, 150, 50)
        }
        
    def initialize_towers(self):
        """Create initial tower state"""
        towers = [[] for _ in range(self.pegs)]
        # Put all disks on first peg (largest at bottom)
        for disk_size in range(self.disks, 0, -1):
            towers[0].append(disk_size)
        return towers
    
    def draw_background(self):
        """Draw beautiful gradient background"""
        for y in range(SCREEN_HEIGHT):
            color_value = int(15 + (y / SCREEN_HEIGHT) * 20)
            color = (color_value, color_value, color_value + 5)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw grid pattern
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, (30, 30, 45), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, (30, 30, 45), (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_towers(self):
        """Draw all towers and disks"""
        # Draw base platform
        pygame.draw.rect(screen, BASE_COLOR, (50, self.base_y, SCREEN_WIDTH - 100, 20))
        pygame.draw.rect(screen, (160, 90, 45), (50, self.base_y, SCREEN_WIDTH - 100, 20), 3)
        
        # Draw each peg
        for i in range(self.pegs):
            x = self.peg_spacing * (i + 1)
            
            # Peg shadow
            pygame.draw.rect(screen, SHADOW, 
                           (x - 6, self.base_y - self.tower_height + 3, 12, self.tower_height))
            
            # Peg
            peg_color = (200, 180, 160)
            pygame.draw.rect(screen, peg_color, 
                           (x - 5, self.base_y - self.tower_height, 10, self.tower_height))
            pygame.draw.rect(screen, (220, 200, 180), 
                           (x - 5, self.base_y - self.tower_height, 10, self.tower_height), 2)
            
            # Peg base
            pygame.draw.rect(screen, (160, 120, 90), (x - 25, self.base_y, 50, 10))
            
            # Peg label
            label = chr(65 + i)  # A, B, C, D
            label_surf = title_font.render(label, True, (255, 255, 200))
            screen.blit(label_surf, (x - label_surf.get_width()//2, self.base_y + 20))
            
            # Draw disks on this peg
            for j, disk_size in enumerate(self.towers[i]):
                disk_width = 120 - (disk_size - 1) * (100 // self.disks)
                disk_y = self.base_y - (j + 1) * self.disk_height
                
                # Color based on disk size
                color_idx = (disk_size - 1) % len(DISK_COLORS)
                disk_color = DISK_COLORS[color_idx]
                
                # Disk with gradient
                pygame.draw.rect(screen, disk_color, 
                               (x - disk_width//2, disk_y, disk_width, self.disk_height),
                               border_radius=8)
                
                # Disk border with highlight
                pygame.draw.rect(screen, (255, 255, 255, 100), 
                               (x - disk_width//2, disk_y, disk_width, self.disk_height),
                               2, border_radius=8)
                
                # Disk label
                if disk_size <= 5:  # Only label smaller disks
                    label = str(disk_size)
                    label_surf = info_font.render(label, True, (255, 255, 255))
                    screen.blit(label_surf, 
                              (x - label_surf.get_width()//2, 
                               disk_y + self.disk_height//2 - label_surf.get_height()//2))
        
        # Highlight selected disk if any
        if self.selected_disk is not None and self.selected_peg is not None:
            if self.selected_peg < len(self.towers) and self.selected_disk < len(self.towers[self.selected_peg]):
                disk_size = self.towers[self.selected_peg][self.selected_disk]
                disk_width = 120 - (disk_size - 1) * (100 // self.disks)
                x = self.peg_spacing * (self.selected_peg + 1)
                disk_y = self.base_y - (self.selected_disk + 1) * self.disk_height
                
                # Highlight glow
                for glow in range(3, 0, -1):
                    glow_color = (255, 255, 100, 50 - glow * 15)
                    glow_rect = pygame.Rect(x - disk_width//2 - glow, disk_y - glow, 
                                          disk_width + glow*2, self.disk_height + glow*2)
                    pygame.draw.rect(screen, glow_color, glow_rect, border_radius=8 + glow)
    
    def draw_info_panel(self):
        """Draw game information panel"""
        # Panel background
        pygame.draw.rect(screen, (30, 30, 50), (20, 20, 400, 200), border_radius=15)
        pygame.draw.rect(screen, (52, 152, 219), (20, 20, 400, 200), 3, border_radius=15)
        
        # Game info
        info_lines = [
            f"Player: {self.player_name}",
            f"Disks: {self.disks}",
            f"Pegs: {self.pegs}",
            f"Moves: {self.move_count}",
            f"Optimal: {2**self.disks - 1}",
            f"Status: {'Solved!' if self.is_solved() else 'In Progress'}"
        ]
        
        y_offset = 40
        for line in info_lines:
            text_surf = info_font.render(line, True, TEXT_COLOR)
            screen.blit(text_surf, (40, y_offset))
            y_offset += 30
    
    def draw_controls(self):
        """Draw control buttons"""
        button_labels = ['🧠 SOLVE', '🔄 RESET', '↩ UNDO', '💡 HINT']
        button_colors = [(46, 204, 113), (230, 126, 34), (52, 152, 219), (155, 89, 182)]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (btn_name, rect) in enumerate(self.buttons.items()):
            color = button_colors[i]
            hover_color = tuple(min(c + 30, 255) for c in color)
            
            # Hover effect
            current_color = hover_color if rect.collidepoint(mouse_pos) else color
            
            # Button shadow
            shadow_rect = rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=10)
            
            # Button
            pygame.draw.rect(screen, current_color, rect, border_radius=10)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=10)
            
            # Button text
            text_surf = move_font.render(button_labels[i], True, TEXT_COLOR)
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))
    
    def draw_move_input(self):
        """Draw move input area"""
        # Input panel
        input_panel = pygame.Rect(SCREEN_WIDTH - 350, 20, 330, 150)
        pygame.draw.rect(screen, (30, 30, 50), input_panel, border_radius=15)
        pygame.draw.rect(screen, (52, 152, 219), input_panel, 3, border_radius=15)
        
        # Title
        title = title_font.render("ENTER MOVE", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH - 330, 30))
        
        # Instructions
        instr = info_font.render("Format: A->B (from peg A to B)", True, (200, 200, 220))
        screen.blit(instr, (SCREEN_WIDTH - 330, 70))
        
        # Input display
        input_display = pygame.Rect(SCREEN_WIDTH - 330, 100, 290, 40)
        pygame.draw.rect(screen, (40, 40, 60), input_display, border_radius=8)
        pygame.draw.rect(screen, (52, 152, 219), input_display, 2, border_radius=8)
        
        # Move history
        if self.move_history:
            last_moves = self.move_history[-3:]  # Show last 3 moves
            for i, move in enumerate(reversed(last_moves)):
                move_text = info_font.render(f"Move {self.move_count - i}: {move}", True, (200, 200, 255))
                screen.blit(move_text, (SCREEN_WIDTH - 330, 150 + i * 25))
    
    def draw(self):
        """Draw everything"""
        self.draw_background()
        self.draw_towers()
        self.draw_info_panel()
        self.draw_controls()
        self.draw_move_input()
        
        # Draw title
        title = title_font.render("🏰 TOWER OF HANOI", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 10))
    
    def is_solved(self):
        """Check if puzzle is solved"""
        # All disks should be on last peg
        return len(self.towers[-1]) == self.disks
    
    def move_disk(self, from_peg, to_peg):
        """Move disk from one peg to another with animation"""
        if not self.towers[from_peg]:
            return False, "Source peg is empty"
        
        disk = self.towers[from_peg][-1]
        
        if self.towers[to_peg] and disk > self.towers[to_peg][-1]:
            return False, "Cannot place larger disk on smaller disk"
        
        # Add to animation queue
        self.animation_queue.append({
            'from_peg': from_peg,
            'to_peg': to_peg,
            'disk': disk,
            'progress': 0
        })
        
        return True, "Move queued"
    
    def update_animation(self):
        """Update disk animations"""
        if self.animation_queue and not self.is_animating:
            self.is_animating = True
            
        if self.is_animating:
            animation = self.animation_queue[0]
            animation['progress'] += 0.02
            
            if animation['progress'] >= 1:
                # Complete the move
                self.towers[animation['from_peg']].pop()
                self.towers[animation['to_peg']].append(animation['disk'])
                self.move_count += 1
                self.move_history.append(f"{chr(65 + animation['from_peg'])}->{chr(65 + animation['to_peg'])}")
                self.animation_queue.pop(0)
                self.is_animating = False
    
    def handle_click(self, pos):
        """Handle mouse clicks for disk selection"""
        # Check if click is on a disk
        for peg_idx in range(self.pegs):
            x = self.peg_spacing * (peg_idx + 1)
            
            if abs(pos[0] - x) < 100:  # Click near peg
                if self.towers[peg_idx]:
                    # Select the top disk
                    self.selected_peg = peg_idx
                    self.selected_disk = len(self.towers[peg_idx]) - 1
                    return True
                else:
                    # Clicked empty peg - move selected disk here
                    if self.selected_disk is not None:
                        success, message = self.move_disk(self.selected_peg, peg_idx)
                        self.selected_disk = None
                        self.selected_peg = None
                        return success
        return False
    
    def handle_button_click(self, pos):
        """Handle control button clicks"""
        for btn_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return btn_name
        return None

def main():
    """Main game loop"""
    clock = pygame.time.Clock()
    
    # Create game instance
    game = TowerOfHanoiUI(disks=5, pegs=3, player_name="Test Player")
    
    # Input text
    input_text = ""
    input_active = False
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Handle text input
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Process move
                        if '->' in input_text:
                            try:
                                src, dest = input_text.upper().split('->')
                                src_idx = ord(src.strip()) - 65
                                dest_idx = ord(dest.strip()) - 65
                                
                                if 0 <= src_idx < game.pegs and 0 <= dest_idx < game.pegs:
                                    success, message = game.move_disk(src_idx, dest_idx)
                                    print(f"Move: {message}")
                            except:
                                print("Invalid move format")
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check buttons
                    btn_clicked = game.handle_button_click(mouse_pos)
                    if btn_clicked:
                        print(f"Button clicked: {btn_clicked}")
                        if btn_clicked == 'reset':
                            game = TowerOfHanoiUI(disks=game.disks, pegs=game.pegs, player_name=game.player_name)
                    
                    # Check move input area
                    input_area = pygame.Rect(SCREEN_WIDTH - 330, 100, 290, 40)
                    if input_area.collidepoint(mouse_pos):
                        input_active = True
                    else:
                        input_active = False
                    
                    # Check disk selection
                    game.handle_click(mouse_pos)
        
        # Update animation
        game.update_animation()
        
        # Draw everything
        screen.fill(BACKGROUND)
        game.draw()
        
        # Draw input text if active
        if input_active:
            input_rect = pygame.Rect(SCREEN_WIDTH - 330, 100, 290, 40)
            pygame.draw.rect(screen, (80, 80, 120), input_rect, border_radius=8)
            
            input_surf = move_font.render(input_text + ("|" if pygame.time.get_ticks() % 1000 < 500 else ""), 
                                        True, TEXT_COLOR)
            screen.blit(input_surf, (SCREEN_WIDTH - 320, 108))
        
        # Check if solved
        if game.is_solved():
            # Draw victory message
            victory_bg = pygame.Surface((600, 200), pygame.SRCALPHA)
            victory_bg.fill((0, 0, 0, 200))
            screen.blit(victory_bg, (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 100))
            
            victory_text = title_font.render("🎉 PUZZLE SOLVED! 🎉", True, (255, 215, 0))
            screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            moves_text = move_font.render(f"Moves: {game.move_count} (Optimal: {2**game.disks - 1})", 
                                        True, (200, 255, 200))
            screen.blit(moves_text, (SCREEN_WIDTH//2 - moves_text.get_width()//2, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()