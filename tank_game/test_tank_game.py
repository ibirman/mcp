import unittest
import pygame
import tank_game
import time

class TestProjectileVisibility(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        pygame.init()
        # Create a small test screen
        self.test_screen = pygame.display.set_mode((800, 600))
        # Store original screen and restore it after tests
        self.original_screen = tank_game.screen
        tank_game.screen = self.test_screen
        
    def tearDown(self):
        """Clean up after each test."""
        tank_game.screen = self.original_screen
        pygame.quit()

    def test_projectile_visibility(self):
        """Test that the projectile is visible and updates correctly."""
        # Set up initial game state
        tank_game.game_state = "aiming"
        tank_game.angle = 45
        tank_game.power = 50
        
        # Fire the projectile
        tank_game.fire_projectile()
        
        # Verify projectile was created
        self.assertIsNotNone(tank_game.projectile_pos)
        self.assertIsNotNone(tank_game.projectile_velocity)
        self.assertEqual(tank_game.game_state, "projectile_moving")
        
        # Get initial position
        initial_pos = tank_game.projectile_pos.copy()
        
        # Update and check position changes
        tank_game.update_projectile()
        
        # Verify projectile moved
        self.assertNotEqual(initial_pos, tank_game.projectile_pos)
        
        # Test projectile rendering
        # Clear screen
        self.test_screen.fill((135, 206, 235))  # Sky blue
        
        # Draw projectile
        tank_game.draw_projectile()
        
        # Get the color of pixels where the projectile should be
        x, y = int(tank_game.projectile_pos[0]), int(tank_game.projectile_pos[1])
        
        # Check multiple pixels around the projectile's position
        pixels_to_check = [
            (x, y),  # Center
            (x + tank_game.projectile_radius, y),  # Right
            (x - tank_game.projectile_radius, y),  # Left
            (x, y + tank_game.projectile_radius),  # Bottom
            (x, y - tank_game.projectile_radius)   # Top
        ]
        
        non_sky_blue_pixels = 0
        for px, py in pixels_to_check:
            if 0 <= px < 800 and 0 <= py < 600:  # Check if within screen bounds
                color = self.test_screen.get_at((px, py))
                if color != (135, 206, 235, 255):  # If not sky blue
                    non_sky_blue_pixels += 1
        
        # Assert that we found some non-sky-blue pixels (projectile is visible)
        self.assertGreater(non_sky_blue_pixels, 0)
        
    def test_projectile_trail(self):
        """Test that the projectile leaves a visible trail."""
        # Set up initial game state
        tank_game.game_state = "aiming"
        tank_game.angle = 45
        tank_game.power = 50
        
        # Fire the projectile
        tank_game.fire_projectile()
        
        # Update several times to create trail
        for _ in range(5):
            tank_game.update_projectile()
        
        # Verify trail exists
        self.assertGreater(len(tank_game.projectile_trail), 1)
        
        # Test trail rendering
        self.test_screen.fill((135, 206, 235))  # Sky blue
        tank_game.draw_projectile()
        
        # Check for trail pixels
        trail_pixels = 0
        for trail_pos in tank_game.projectile_trail:
            x, y = int(trail_pos[0]), int(trail_pos[1])
            if 0 <= x < 800 and 0 <= y < 600:  # Check if within screen bounds
                color = self.test_screen.get_at((x, y))
                if color != (135, 206, 235, 255):  # If not sky blue
                    trail_pixels += 1
        
        # Assert that trail is visible
        self.assertGreater(trail_pixels, 0)
    
    def test_projectile_movement(self):
        """Test that the projectile moves in a parabolic path."""
        # Set up initial game state
        tank_game.game_state = "aiming"
        tank_game.angle = 45
        tank_game.power = 50
        tank_game.gravity = 9.8
        
        # Fire the projectile
        tank_game.fire_projectile()
        
        # Track positions
        positions = []
        
        # Update several times and record positions
        for _ in range(10):
            positions.append(tank_game.projectile_pos.copy())
            tank_game.update_projectile()
        
        # Verify y-coordinates follow parabolic path (first up, then down)
        y_coords = [pos[1] for pos in positions]
        
        # Find the highest point
        min_y = min(y_coords)  # Remember: y increases downward in pygame
        min_y_index = y_coords.index(min_y)
        
        # Check that y-coordinates decrease (go up) then increase (fall down)
        if min_y_index > 0:  # Only check if we have enough points
            # Check path up to highest point
            for i in range(min_y_index):
                self.assertGreater(y_coords[i], y_coords[i + 1])
            
            # Check path after highest point
            for i in range(min_y_index, len(y_coords) - 1):
                self.assertLess(y_coords[i], y_coords[i + 1])

if __name__ == '__main__':
    unittest.main() 