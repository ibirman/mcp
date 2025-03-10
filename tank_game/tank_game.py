import pygame
import sys
import math
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
TANK_COLOR = (50, 120, 50)
MOUNTAIN_COLOR = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game variables
gravity = 9.8
power = 50
angle = 45
game_state = "aiming"  # "aiming" or "projectile_moving"
score = 0
shots_taken = 0

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Mountain Shooter")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Projectile trail
projectile_trail = []
MAX_TRAIL_LENGTH = 20

# Generate mountain
def generate_mountain():
    mountain_points = []
    # Start at the left edge
    mountain_points.append((0, HEIGHT))
    
    # Create a series of points for the mountain
    num_points = 10
    for i in range(num_points):
        x = int(WIDTH * (i / (num_points - 1)))
        
        # Make the middle higher (mountain peak)
        if i == num_points // 2:
            y = HEIGHT - random.randint(250, 350)
        elif i == (num_points // 2) - 1 or i == (num_points // 2) + 1:
            y = HEIGHT - random.randint(200, 300)
        else:
            y = HEIGHT - random.randint(100, 200)
        
        mountain_points.append((x, y))
    
    # End at the right edge
    mountain_points.append((WIDTH, HEIGHT))
    
    return mountain_points

# Generate target position
def generate_target(mountain_points):
    # Place target on the right side of the mountain
    target_x = random.randint(int(WIDTH * 0.7), int(WIDTH * 0.9))
    
    # Find the mountain height at this x position
    for i in range(len(mountain_points) - 1):
        if mountain_points[i][0] <= target_x <= mountain_points[i+1][0]:
            # Linear interpolation to find the height
            x1, y1 = mountain_points[i]
            x2, y2 = mountain_points[i+1]
            ratio = (target_x - x1) / (x2 - x1)
            mountain_height = y1 + ratio * (y2 - y1)
            target_y = mountain_height - 20  # Place target just above the mountain
            return (target_x, target_y)
    
    # Fallback
    return (target_x, HEIGHT - 150)

def get_mountain_height_at_x(x, mountain_points):
    """Calculate the mountain height at a given x-coordinate."""
    for i in range(len(mountain_points) - 1):
        x1, y1 = mountain_points[i]
        x2, y2 = mountain_points[i + 1]
        if x1 <= x <= x2:
            if x2 - x1 == 0:
                return y1
            ratio = (x - x1) / (x2 - x1)
            return y1 + ratio * (y2 - y1)
    return HEIGHT  # Default to bottom if not found

# Initialize game elements
mountain_points = generate_mountain()
target_pos = generate_target(mountain_points)

# Set tank position based on mountain height
tank_x = 50
tank_y = get_mountain_height_at_x(tank_x, mountain_points) - 10  # Slightly above the mountain surface
tank_pos = (tank_x, tank_y)

# Projectile variables
projectile_pos = None
projectile_velocity = None
projectile_radius = 5

# UI elements
def draw_power_meter():
    meter_width = 150
    meter_height = 20
    meter_x = 20
    meter_y = 20
    
    # Draw background
    pygame.draw.rect(screen, WHITE, (meter_x, meter_y, meter_width, meter_height))
    
    # Draw filled portion
    fill_width = int((power / 100) * meter_width)
    pygame.draw.rect(screen, GREEN, (meter_x, meter_y, fill_width, meter_height))
    
    # Draw border
    pygame.draw.rect(screen, BLACK, (meter_x, meter_y, meter_width, meter_height), 2)
    
    # Draw text
    power_text = font.render(f"Power: {power}", True, BLACK)
    screen.blit(power_text, (meter_x + meter_width + 10, meter_y))

def draw_angle_indicator():
    # Text indicator
    angle_text = font.render(f"Angle: {angle}°", True, BLACK)
    screen.blit(angle_text, (20, 50))
    
    # Visual angle indicator
    indicator_x = 20
    indicator_y = 12
    indicator_radius = 10
    
    # Draw circle background
    pygame.draw.circle(screen, WHITE, (indicator_x, indicator_y), indicator_radius)
    pygame.draw.circle(screen, BLACK, (indicator_x, indicator_y), indicator_radius, 2)
    
    # Draw angle line
    line_length = indicator_radius - 5
    end_x = indicator_x + line_length * math.cos(math.radians(angle))
    end_y = indicator_y - line_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, RED, (indicator_x, indicator_y), (end_x, end_y), 3)
    
    # Draw angle adjustment buttons
    pygame.draw.rect(screen, BLUE, (indicator_x + indicator_radius + 10, indicator_y - 15, 20, 20))
    pygame.draw.rect(screen, BLUE, (indicator_x + indicator_radius + 40, indicator_y - 15, 20, 20))
    
    # Draw + and - symbols
    plus_text = font.render("+", True, WHITE)
    minus_text = font.render("-", True, WHITE)
    screen.blit(plus_text, (indicator_x + indicator_radius + 13, indicator_y - 15))
    screen.blit(minus_text, (indicator_x + indicator_radius + 45, indicator_y - 15))
    
    # Draw angle adjustment instructions
    instructions = small_font.render("Use UP/DOWN keys or click buttons to adjust angle", True, BLACK)
    screen.blit(instructions, (20, 80))

def draw_gravity_control():
    gravity_text = font.render(f"Gravity: {gravity:.1f}", True, BLACK)
    screen.blit(gravity_text, (20, 110))
    
    # Draw increase/decrease buttons
    pygame.draw.rect(screen, BLUE, (180, 110, 20, 20))
    pygame.draw.rect(screen, BLUE, (210, 110, 20, 20))
    
    # Draw + and - symbols
    plus_text = font.render("+", True, WHITE)
    minus_text = font.render("-", True, WHITE)
    screen.blit(plus_text, (183, 110))
    screen.blit(minus_text, (215, 110))

def draw_score():
    score_text = font.render(f"Score: {score} | Shots: {shots_taken}", True, BLACK)
    screen.blit(score_text, (WIDTH - 250, 20))

def draw_tank():
    # Tank body
    pygame.draw.rect(screen, TANK_COLOR, (tank_pos[0] - 15, tank_pos[1] - 10, 30, 20))
    
    # Tank turret
    turret_length = 30
    end_x = tank_pos[0] + turret_length * math.cos(math.radians(angle))
    end_y = tank_pos[1] - turret_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, TANK_COLOR, tank_pos, (end_x, end_y), 5)
    
    # Draw a small dot at the end of the turret to show where projectile will start
    pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 3)

def draw_target():
    pygame.draw.circle(screen, RED, target_pos, 15)
    pygame.draw.circle(screen, WHITE, target_pos, 10)
    pygame.draw.circle(screen, RED, target_pos, 5)

def draw_projectile():
    # Make projectile larger for better visibility
    global projectile_radius
    projectile_radius = 8  # Increased from 5 to 8
    
    # Draw projectile trail
    if projectile_trail and game_state == "projectile_moving":
        for i, pos in enumerate(projectile_trail):
            # Fade the trail from orange to yellow
            trail_color = (
                ORANGE[0] + (YELLOW[0] - ORANGE[0]) * i / len(projectile_trail),
                ORANGE[1] + (YELLOW[1] - ORANGE[1]) * i / len(projectile_trail),
                ORANGE[2] + (YELLOW[2] - ORANGE[2]) * i / len(projectile_trail)
            )
            trail_radius = max(3, projectile_radius * (i / len(projectile_trail)))
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), int(trail_radius))
    
    # Draw the current projectile with multiple layers for better visibility
    if projectile_pos and game_state == "projectile_moving":
        # Draw outer glow
        pygame.draw.circle(screen, YELLOW, (int(projectile_pos[0]), int(projectile_pos[1])), projectile_radius + 4)
        # Draw white outline
        pygame.draw.circle(screen, WHITE, (int(projectile_pos[0]), int(projectile_pos[1])), projectile_radius + 2)
        # Draw projectile
        pygame.draw.circle(screen, BLACK, (int(projectile_pos[0]), int(projectile_pos[1])), projectile_radius)

def draw_mountain():
    pygame.draw.polygon(screen, MOUNTAIN_COLOR, mountain_points)

def fire_projectile():
    global projectile_pos, projectile_velocity, game_state, shots_taken, projectile_trail
    
    # Initial position is at the end of the tank's turret
    turret_length = 30
    start_x = tank_pos[0] + turret_length * math.cos(math.radians(angle))
    start_y = tank_pos[1] - turret_length * math.sin(math.radians(angle))
    
    projectile_pos = [start_x, start_y]
    projectile_trail = [(start_x, start_y)]  # Initialize trail with starting position
    
    # Initial velocity based on power and angle (increased velocity for better visibility)
    velocity_magnitude = power * 0.5  # Increased from power / 5 to power * 0.5
    projectile_velocity = [
        velocity_magnitude * math.cos(math.radians(angle)),
        -velocity_magnitude * math.sin(math.radians(angle))
    ]
    
    game_state = "projectile_moving"
    shots_taken += 1

def update_projectile():
    global projectile_pos, projectile_velocity, game_state, score, projectile_trail
    
    if projectile_pos and game_state == "projectile_moving":  # Only update if we're in moving state
        # Add current position to trail before updating position
        projectile_trail.append((projectile_pos[0], projectile_pos[1]))
        
        # Limit trail length
        if len(projectile_trail) > MAX_TRAIL_LENGTH:
            projectile_trail.pop(0)
        
        # Update position based on velocity
        projectile_pos[0] += projectile_velocity[0]
        projectile_pos[1] += projectile_velocity[1]
        
        # Apply gravity
        projectile_velocity[1] += gravity / 10
        
        # Print debug info
        print(f"Projectile position: {projectile_pos}, velocity: {projectile_velocity}")
        
        # Check if projectile hits the target
        distance_to_target = math.sqrt((projectile_pos[0] - target_pos[0])**2 + 
                                      (projectile_pos[1] - target_pos[1])**2)
        
        if distance_to_target < 15:  # Target radius
            score += 1
            reset_game()
            return
        
        # Check if projectile hits the mountain
        if is_point_in_polygon(projectile_pos, mountain_points):
            reset_game()
            return
        
        # Check if projectile is out of bounds
        if (projectile_pos[0] < 0 or projectile_pos[0] > WIDTH or 
            projectile_pos[1] > HEIGHT):
            reset_game()
            return

def is_point_in_polygon(point, polygon):
    # Simple collision detection for the mountain
    x, y = point
    
    # Check if point is below the mountain at this x position
    for i in range(len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i+1]
        
        if x1 <= x <= x2:
            # Linear interpolation to find the height
            if x2 - x1 == 0:  # Avoid division by zero
                mountain_height = y1
            else:
                ratio = (x - x1) / (x2 - x1)
                mountain_height = y1 + ratio * (y2 - y1)
            
            if y >= mountain_height:
                return True
    
    return False

def reset_game():
    global projectile_pos, projectile_velocity, game_state, target_pos, projectile_trail
    
    projectile_pos = None
    projectile_velocity = None
    projectile_trail = []
    game_state = "aiming"
    
    # Generate a new target position
    target_pos = generate_target(mountain_points)

def check_gravity_buttons(pos):
    global gravity
    
    # Check + button
    if 180 <= pos[0] <= 200 and 110 <= pos[1] <= 130:
        gravity = min(20, gravity + 0.5)
    
    # Check - button
    if 210 <= pos[0] <= 230 and 110 <= pos[1] <= 130:
        gravity = max(1, gravity - 0.5)

def check_angle_buttons(pos):
    global angle
    
    # Visual angle indicator position
    indicator_x = 120
    indicator_y = 50
    indicator_radius = 30
    
    # Check + button
    if indicator_x + indicator_radius + 10 <= pos[0] <= indicator_x + indicator_radius + 30 and indicator_y - 15 <= pos[1] <= indicator_y + 5:
        angle = min(90, angle + 5)
    
    # Check - button
    if indicator_x + indicator_radius + 40 <= pos[0] <= indicator_x + indicator_radius + 60 and indicator_y - 15 <= pos[1] <= indicator_y + 5:
        angle = max(0, angle - 5)

# Draw trajectory prediction (optional feature)
def draw_trajectory_prediction():
    if game_state == "aiming":
        # Calculate predicted trajectory points
        points = []
        
        # Initial position
        turret_length = 30
        start_x = tank_pos[0] + turret_length * math.cos(math.radians(angle))
        start_y = tank_pos[1] - turret_length * math.sin(math.radians(angle))
        
        # Initial velocity
        velocity_magnitude = power / 5
        vel_x = velocity_magnitude * math.cos(math.radians(angle))
        vel_y = -velocity_magnitude * math.sin(math.radians(angle))
        
        # Simulate trajectory
        sim_x, sim_y = start_x, start_y
        sim_vel_x, sim_vel_y = vel_x, vel_y
        
        for _ in range(100):  # Limit to 100 points
            points.append((int(sim_x), int(sim_y)))
            
            # Update position
            sim_x += sim_vel_x
            sim_y += sim_vel_y
            
            # Apply gravity
            sim_vel_y += gravity / 10
            
            # Check if point is out of bounds or hits mountain
            if (sim_x < 0 or sim_x > WIDTH or sim_y > HEIGHT or 
                is_point_in_polygon([sim_x, sim_y], mountain_points)):
                break
        
        # Draw trajectory as dotted line
        for i, point in enumerate(points):
            if i % 5 == 0:  # Draw every 5th point for a dotted effect
                pygame.draw.circle(screen, (100, 100, 100, 128), point, 2)

# Main game loop
running = True
show_trajectory = False  # Toggle for trajectory prediction

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and game_state == "aiming":
                fire_projectile()
            
            elif event.key == K_UP:
                angle = min(90, angle + 1)
            
            elif event.key == K_DOWN:
                angle = max(0, angle - 1)
            
            elif event.key == K_LEFT:
                power = max(10, power - 1)
            
            elif event.key == K_RIGHT:
                power = min(100, power + 1)
                
            elif event.key == K_t:
                # Toggle trajectory prediction
                show_trajectory = not show_trajectory
        
        elif event.type == MOUSEBUTTONDOWN:
            check_gravity_buttons(event.pos)
            check_angle_buttons(event.pos)
    
    # Update game state
    if game_state == "projectile_moving":
        update_projectile()
    
    # Draw everything
    screen.fill(SKY_BLUE)
    
    # Optional trajectory prediction
    if show_trajectory and game_state == "aiming":
        draw_trajectory_prediction()
    
    # Draw game elements in the correct order
    draw_mountain()
    draw_target()  # Draw target before projectile
    draw_projectile()  # Draw projectile after mountain and target
    draw_tank()  # Draw tank last
    
    # UI elements
    draw_power_meter()
    draw_angle_indicator()
    draw_gravity_control()
    draw_score()
    
    # Draw instructions
    instructions_text = small_font.render("Press SPACE to fire, T to toggle trajectory prediction", True, BLACK)
    screen.blit(instructions_text, (WIDTH // 2 - 200, HEIGHT - 30))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit() 