"""
player_input.py - Elegant Pygame player input screen
"""
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Player Setup")

# Colors
BACKGROUND = (25, 25, 40)
INPUT_BG = (40, 40, 60)
INPUT_BORDER = (52, 152, 219)
INPUT_HOVER = (41, 128, 185)
TEXT_COLOR = (236, 240, 241)
BUTTON_COLOR = (46, 204, 113)
BUTTON_HOVER = (39, 174, 96)
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

# Fonts
try:
    title_font = pygame.font.Font("assets/fonts/retro.ttf", 48)
    label_font = pygame.font.Font("assets/fonts/retro.ttf", 32)
    input_font = pygame.font.Font("assets/fonts/retro.ttf", 28)
    text_font = pygame.font.Font(None, 24)
except:
    title_font = pygame.font.Font(None, 48)
    label_font = pygame.font.Font(None, 32)
    input_font = pygame.font.Font(None, 28)
    text_font = pygame.font.Font(None, 24)

class InputBox:
    """Beautiful input box with animation"""
    def __init__(self, x, y, width, height, label="", is_numeric=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = ""
        self.is_numeric = is_numeric
        self.active = False
        self.color = INPUT_BORDER
        self.label_surf = label_font.render(label, True, TEXT_COLOR)
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = INPUT_HOVER if self.active else INPUT_BORDER
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.is_numeric:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                else:
                    self.text += event.unicode
        return False
        
    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
    def draw(self, surface):
        # Draw label
        surface.blit(self.label_surf, (self.rect.x, self.rect.y - 40))
        
        # Draw input box
        pygame.draw.rect(surface, INPUT_BG, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.color, self.rect, 3, border_radius=10)
        
        # Draw text
        text_surf = input_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_rect = pygame.Rect(cursor_x, self.rect.y + 10, 2, self.rect.height - 20)
            pygame.draw.rect(surface, TEXT_COLOR, cursor_rect)
            
    def get_value(self):
        if self.is_numeric and self.text:
            return int(self.text)
        return self.text.strip()

class Button:
    """Modern button with hover effect"""
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER
        self.current_color = color
        self.shadow_offset = 4
        
    def draw(self, surface, mouse_pos):
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(surface, (20, 20, 30), shadow_rect, border_radius=10)
        
        # Hover effect
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Button
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        # Text
        text_surf = label_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def draw_disk_visualization(surface, disks, pegs):
    """Draw beautiful disk visualization"""
    center_x = SCREEN_WIDTH // 2
    base_y = 550
    
    # Draw pegs
    for i in range(pegs):
        x = center_x - (pegs - 1) * 100 + i * 200
        
        # Peg base
        pygame.draw.rect(surface, (139, 69, 19), (x - 40, base_y, 80, 15))
        
        # Peg pole
        pygame.draw.rect(surface, (160, 82, 45), (x - 8, base_y - 250, 16, 250))
        
        # Peg label
        label = chr(65 + i)  # A, B, C, D
        label_surf = label_font.render(label, True, (255, 255, 255))
        surface.blit(label_surf, (x - label_surf.get_width()//2, base_y + 25))
    
    # Draw disks on first peg (for visualization)
    if disks > 0:
        for d in range(disks):
            disk_width = 120 - d * (100 // disks)
            disk_height = 20
            disk_y = base_y - (d + 1) * disk_height
            
            # Color based on disk size
            color_idx = d % len(DISK_COLORS)
            color = DISK_COLORS[color_idx]
            
            x = center_x - (pegs - 1) * 100  # First peg position
            
            pygame.draw.rect(surface, color, 
                           (x - disk_width//2, disk_y, disk_width, disk_height),
                           border_radius=10)
            pygame.draw.rect(surface, (255, 255, 255),
                           (x - disk_width//2, disk_y, disk_width, disk_height),
                           2, border_radius=10)

def get_player_name():
    """Beautiful player name input screen"""
    clock = pygame.time.Clock()
    
    # Input boxes
    name_input = InputBox(SCREEN_WIDTH//2 - 200, 200, 400, 50, "PLAYER NAME")
    
    # Buttons
    start_button = Button(SCREEN_WIDTH//2 - 150, 350, 300, 60, "🎮 START GAME")
    random_button = Button(SCREEN_WIDTH//2 - 150, 430, 300, 50, "🎲 RANDOM NAME")
    
    # Random names
    random_names = ["DragonSlayer", "TowerMaster", "PuzzleKing", "DiskMover", 
                   "HanoiHero", "Brainiac", "StrategyStar", "LogicLord"]
    
    player_name = ""
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
            # Handle input
            if name_input.handle_event(event):
                if name_input.text.strip():
                    return name_input.text.strip()
            
            # Handle buttons
            if start_button.is_clicked(mouse_pos, event):
                if name_input.text.strip():
                    return name_input.text.strip()
                    
            if random_button.is_clicked(mouse_pos, event):
                name_input.text = random.choice(random_names)
        
        # Update
        name_input.update()
        
        # Draw
        screen.fill(BACKGROUND)
        
        # Title
        title = title_font.render("PLAYER REGISTRATION", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Input box
        name_input.draw(screen)
        
        # Buttons
        start_button.draw(screen, mouse_pos)
        random_button.draw(screen, mouse_pos)
        
        # Instructions
        instr = text_font.render("Enter your name or click for random name", True, (200, 200, 220))
        screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, 300))
        
        # Draw sample tower
        draw_disk_visualization(screen, 5, 3)
        
        pygame.display.flip()
        clock.tick(60)

def select_disk_count():
    """Beautiful disk selection with visualization"""
    clock = pygame.time.Clock()
    
    disks = 7  # Default
    disk_buttons = []
    
    # Create disk number buttons
    for i in range(6):  # 5 to 10 disks
        disk_num = i + 5
        x = 200 + i * 120
        disk_buttons.append({
            'rect': pygame.Rect(x, 200, 100, 50),
            'number': disk_num,
            'selected': disk_num == 7
        })
    
    random_button = Button(SCREEN_WIDTH//2 - 150, 280, 300, 50, "🎲 RANDOM DISKS (5-10)")
    continue_button = Button(SCREEN_WIDTH//2 - 150, 350, 300, 60, "✅ CONTINUE")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check disk buttons
                for btn in disk_buttons:
                    if btn['rect'].collidepoint(mouse_pos):
                        for b in disk_buttons:
                            b['selected'] = False
                        btn['selected'] = True
                        disks = btn['number']
                
                # Check random button
                if random_button.is_clicked(mouse_pos, event):
                    disks = random.randint(5, 10)
                    for btn in disk_buttons:
                        btn['selected'] = btn['number'] == disks
                
                # Check continue button
                if continue_button.is_clicked(mouse_pos, event):
                    return disks
        
        # Draw
        screen.fill(BACKGROUND)
        
        # Title
        title = title_font.render("SELECT DISK COUNT", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Subtitle
        subtitle = text_font.render("Choose number of disks (5-10)", True, (200, 200, 220))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 120))
        
        # Disk buttons
        for btn in disk_buttons:
            color = (46, 204, 113) if btn['selected'] else (52, 152, 219)
            hover_color = (39, 174, 96) if btn['selected'] else (41, 128, 185)
            
            # Hover effect
            current_color = hover_color if btn['rect'].collidepoint(mouse_pos) else color
            
            pygame.draw.rect(screen, current_color, btn['rect'], border_radius=10)
            pygame.draw.rect(screen, TEXT_COLOR, btn['rect'], 2, border_radius=10)
            
            # Number
            num_text = label_font.render(str(btn['number']), True, TEXT_COLOR)
            screen.blit(num_text, num_text.get_rect(center=btn['rect'].center))
            
            # Draw mini disk visualization
            for d in range(btn['number']):
                disk_width = 80 - d * (70 // btn['number'])
                x = btn['rect'].centerx - disk_width//2
                y = btn['rect'].bottom + 20 + d * 15
                
                color_idx = d % len(DISK_COLORS)
                pygame.draw.rect(screen, DISK_COLORS[color_idx], 
                               (x, y, disk_width, 10),
                               border_radius=5)
        
        # Current selection display
        selection_text = label_font.render(f"Selected: {disks} disks", True, (46, 204, 113))
        screen.blit(selection_text, (SCREEN_WIDTH//2 - selection_text.get_width()//2, 450))
        
        # Buttons
        random_button.draw(screen, mouse_pos)
        continue_button.draw(screen, mouse_pos)
        
        pygame.display.flip()
        clock.tick(60)

def select_peg_count():
    """Beautiful peg selection screen"""
    clock = pygame.time.Clock()
    
    pegs = 3  # Default
    peg_buttons = []
    
    # Create peg buttons
    peg_options = [3, 4]
    for i, peg_count in enumerate(peg_options):
        x = SCREEN_WIDTH//2 - 150 + i * 300
        peg_buttons.append({
            'rect': pygame.Rect(x, 200, 250, 150),
            'count': peg_count,
            'selected': peg_count == 3
        })
    
    continue_button = Button(SCREEN_WIDTH//2 - 150, 400, 300, 60, "✅ CONTINUE")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check peg buttons
                for btn in peg_buttons:
                    if btn['rect'].collidepoint(mouse_pos):
                        for b in peg_buttons:
                            b['selected'] = False
                        btn['selected'] = True
                        pegs = btn['count']
                
                # Check continue button
                if continue_button.is_clicked(mouse_pos, event):
                    return pegs
        
        # Draw
        screen.fill(BACKGROUND)
        
        # Title
        title = title_font.render("SELECT PEG COUNT", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Subtitle
        subtitle = text_font.render("Choose 3 pegs (Classic) or 4 pegs (Advanced)", True, (200, 200, 220))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 120))
        
        # Peg buttons
        for btn in peg_buttons:
            color = (46, 204, 113) if btn['selected'] else (52, 152, 219)
            hover_color = (39, 174, 96) if btn['selected'] else (41, 128, 185)
            
            # Hover effect
            current_color = hover_color if btn['rect'].collidepoint(mouse_pos) else color
            
            # Button background
            pygame.draw.rect(screen, current_color, btn['rect'], border_radius=15)
            pygame.draw.rect(screen, TEXT_COLOR, btn['rect'], 3, border_radius=15)
            
            # Peg count text
            count_text = title_font.render(f"{btn['count']} PEGS", True, TEXT_COLOR)
            screen.blit(count_text, count_text.get_rect(center=(btn['rect'].centerx, btn['rect'].y + 40)))
            
            # Draw peg visualization
            base_y = btn['rect'].y + 80
            for p in range(btn['count']):
                x = btn['rect'].centerx - (btn['count'] - 1) * 30 + p * 60
                
                # Peg
                pygame.draw.rect(screen, (160, 82, 45), (x - 5, base_y - 60, 10, 60))
                
                # Base
                pygame.draw.rect(screen, (139, 69, 19), (x - 20, base_y, 40, 8))
            
            # Description
            desc = "Classic" if btn['count'] == 3 else "Frame-Stewart"
            desc_text = text_font.render(desc, True, TEXT_COLOR)
            screen.blit(desc_text, desc_text.get_rect(center=(btn['rect'].centerx, btn['rect'].bottom - 20)))
        
        # Current selection
        selection_text = label_font.render(f"Selected: {pegs} pegs", True, (46, 204, 113))
        screen.blit(selection_text, (SCREEN_WIDTH//2 - selection_text.get_width()//2, 500))
        
        # Continue button
        continue_button.draw(screen, mouse_pos)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    print("Testing Player Input Screens...")
    
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