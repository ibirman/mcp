# Tank Mountain Shooter

A simple Python game where you control a tank and try to shoot a target on the other side of a mountain.

## Features

- Control the tank's firing angle and power
- Adjustable gravity settings
- Randomly generated mountain terrain
- Score tracking

## How to Play

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   python tank_game.py
   ```

3. Game Controls:
   - **Up/Down Arrow Keys**: Adjust the firing angle
   - **Left/Right Arrow Keys**: Adjust the firing power
   - **Space Bar**: Fire the projectile
   - **Mouse Click**: Click the + and - buttons to adjust gravity

4. Game Objective:
   - Hit the target (bullseye) on the other side of the mountain
   - Each successful hit earns you a point
   - The target will move to a new position after each hit

## Adjusting Gravity

The game allows you to adjust the gravity setting, which affects how quickly the projectile falls:
- Click the "+" button to increase gravity (makes projectiles fall faster)
- Click the "-" button to decrease gravity (makes projectiles fall slower)

Experiment with different gravity settings to see how it affects your shots!

## Physics

The game simulates basic projectile physics:
- The projectile follows a parabolic trajectory
- Gravity pulls the projectile downward
- The initial velocity is determined by the power and angle settings

Have fun playing! 