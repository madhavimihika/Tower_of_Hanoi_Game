"""
game_menu.py - Stunning Pygame menu for Tower of Hanoi
"""
import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Game Hub")

# Colors - Modern palette
BACKGROUND = (18, 18, 30)
PRIMARY = (41, 128, 185)
SECONDARY = (52, 152, 219)
ACCENT = (46, 204, 113)
TEXT_COLOR = (236, 240, 241)
HOVER_COLOR = (52, 73, 94)
SHADOW = (10, 10, 20)

# Fonts
try:
    title_font = pygame.font.Font("assets/fonts/retro.ttf", 64)
    menu_font = pygame.font.Font("assets/fonts/retro.ttf", 36)
    text_font = pygame.font.Font(None, 28)
except:
    title_font = pygame.font.Font(None, 64)
    menu_font = pygame.font.Font(None, 36)
    text_font = pygame.font.Font(None, 28)

class Button:
    """Beautiful animated button"""
    def __init__(self, x, y, width, height, text, color=PRIMARY, hover_color=HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.shadow_offset = 5
        self.animation_progress = 0
        
    def draw(self, surface):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(surface, SHADOW, shadow_rect, border_radius=15)
        
        # Draw button with animation
        if self.is_hovered and self.animation_progress < 1:
            self.animation_progress += 0.1
        elif not self.is_hovered and self.animation_progress > 0:
            self.animation_progress -= 0.1
            
        # Animated color
        r = int(self.color[0] + (self.hover_color[0] - self.color[0]) * self.animation_progress)
        g = int(self.color[1] + (self.hover_color[1] - self.color[1]) * self.animation_progress)
        b = int(self.color[2] + (self.hover_color[2] - self.color[2]) * self.animation_progress)
        animated_color = (r, g, b)
        
        # Animated size
        scale = 1 + 0.05 * self.animation_progress
        animated_rect = self.rect.copy()
        animated_rect.width = int(self.rect.width * scale)
        animated_rect.height = int(self.rect.height * scale)
        animated_rect.center = self.rect.center
        
        pygame.draw.rect(surface, animated_color, animated_rect, border_radius=15)
        pygame.draw.rect(surface, TEXT_COLOR, animated_rect, 3, border_radius=15)
        
        # Draw text
        text_surf = menu_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=animated_rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def draw_gradient_background(surface):
    """Draw beautiful gradient background"""
    for y in range(SCREEN_HEIGHT):
        # Vertical gradient
        color_value = int(18 + (y / SCREEN_HEIGHT) * 10)
        color = (color_value, color_value, color_value + 10)
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

def draw_particles(surface, particles):
    """Draw floating particles"""
    for particle in particles:
        pygame.draw.circle(surface, (255, 255, 255, 100), (particle['x'], particle['y']), particle['size'])
        particle['y'] -= particle['speed']
        if particle['y'] < 0:
            particle['y'] = SCREEN_HEIGHT

def add_tower_of_hanoi_to_menu():
    """Beautiful Pygame menu for Tower of Hanoi"""
    clock = pygame.time.Clock()
    
    # Create buttons
    buttons = [
        Button(SCREEN_WIDTH//2 - 150, 250, 300, 70, " START GAME", ACCENT),
        Button(SCREEN_WIDTH//2 - 150, 350, 300, 70, " INSTRUCTIONS", SECONDARY),
        Button(SCREEN_WIDTH//2 - 150, 450, 300, 70, " LEADERBOARD", PRIMARY),
        Button(SCREEN_WIDTH//2 - 150, 550, 300, 70, " EXIT", (231, 76, 60))
    ]

    # Particles for background effect
    particles = []
    for _ in range(50):
        particles.append({
            'x': pygame.time.get_ticks() % SCREEN_WIDTH,
            'y': pygame.time.get_ticks() % SCREEN_HEIGHT,
            'size': pygame.time.get_ticks() % 3 + 1,
            'speed': pygame.time.get_ticks() % 2 + 0.5
        })
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Check button clicks
            for i, button in enumerate(buttons):
                if button.is_clicked(mouse_pos, event):
                    return str(i + 1)  # Return '1', '2', '3', or '4'
        
        # Update particles
        for particle in particles:
            particle['x'] += 0.5
            if particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
        
        # Draw everything
        draw_gradient_background(screen)
        draw_particles(screen, particles)
        
        # Draw title with shadow
        title_text = "TOWER OF HANOI"
        title_shadow = title_font.render(title_text, True, SHADOW)
        title_main = title_font.render(title_text, True, (255, 215, 0))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_shadow.get_width()//2 + 3, 103))
        screen.blit(title_main, (SCREEN_WIDTH//2 - title_main.get_width()//2, 100))
        
        # Draw subtitle
        subtitle = text_font.render("Classic Puzzle Game with Modern Twist", True, (200, 200, 255))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 180))
        
        # Draw buttons
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        # Draw footer
        footer = text_font.render("Use mouse to select options • Press ESC to exit", True, (150, 150, 180))
        screen.blit(footer, (SCREEN_WIDTH//2 - footer.get_width()//2, 650))
        
        # Animated tower in background
        draw_animated_towers(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Add a default return at the end
    return '4'  # Exit if window closed

def draw_animated_towers(surface):
    """Draw animated towers in background"""
    tower_base_y = 150
    tower_height = 100
    
    # Three towers
    for i in range(3):
        x = SCREEN_WIDTH//4 * (i + 1)
        
        # Tower base
        pygame.draw.rect(surface, (139, 69, 19), (x - 30, tower_base_y, 60, 10))
        
        # Tower pole with animation
        time_ms = pygame.time.get_ticks()
        pole_color = (160 + int(40 * abs(pygame.math.Vector2(x, 0).length() % 1)), 
                      82 + int(40 * abs(pygame.math.Vector2(x, 100).length() % 1)), 
                      45)
        
        pygame.draw.rect(surface, pole_color, (x - 5, tower_base_y - tower_height, 10, tower_height))
        
        # Animated disks
        disk_count = 4
        for d in range(disk_count):
            disk_width = 40 - d * 8
            disk_height = 15
            disk_y = tower_base_y - (d + 1) * disk_height
            
            # Animate first tower disks
            if i == 0:
                disk_color = (
                    255 - d * 30,
                    100 + d * 20,
                    50 + d * 25
                )
                pygame.draw.rect(surface, disk_color, 
                               (x - disk_width//2, disk_y, disk_width, disk_height))
                pygame.draw.rect(surface, (255, 255, 255), 
                               (x - disk_width//2, disk_y, disk_width, disk_height), 2)

def show_instructions():
    """Beautiful instructions screen"""
    clock = pygame.time.Clock()
    back_button = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "⬅ BACK", SECONDARY)
    
    instructions = [
        " TOWER OF HANOI RULES",
        "",
        "• Objective: Move all disks from first peg to last peg",
        "• Rules:",
        "  1. Move only one disk at a time",
        "  2. Larger disk cannot be placed on smaller disk",
        "  3. Use auxiliary pegs to help move disks",
        "",
        " GAME FEATURES",
        "• Random disks: 5 to 10 per game",
        "• Peg options: Choose 3 or 4 pegs",
        "• Move validation: Ensures legal moves only",
        "• Algorithm comparison: See optimal solution",
        "• Leaderboard: Save your best scores",
        "",
        "💡 TIP: Minimum moves for 3 pegs = 2^N - 1"
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if back_button.is_clicked(mouse_pos, event):
                return
        
        # Draw
        draw_gradient_background(screen)
        
        # Title
        title = title_font.render("INSTRUCTIONS", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Instructions text
        y_offset = 150
        for line in instructions:
            if line.startswith("🏰") or line.startswith("🎮") or line.startswith("💡"):
                color = (255, 215, 0) if line.startswith("🏰") else (46, 204, 113) if line.startswith("🎮") else (52, 152, 219)
                font = menu_font
            elif line.startswith("•"):
                color = (200, 200, 255)
                font = text_font
            elif line.startswith("  "):
                color = (180, 180, 240)
                font = text_font
            else:
                color = TEXT_COLOR
                font = text_font
            
            text_surf = font.render(line, True, color)
            screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y_offset))
            y_offset += 40 if line.startswith("🏰") or line.startswith("🎮") or line.startswith("💡") else 30
        
        # Back button
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    print("Starting Tower of Hanoi Menu...")
    choice = add_tower_of_hanoi_to_menu()
    print(f"User selected option: {choice}")
    
    if choice == '2':  # Instructions
        show_instructions()
    
    pygame.quit()