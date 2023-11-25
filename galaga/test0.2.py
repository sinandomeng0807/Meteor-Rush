import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 500, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("METEOR RUSH")

# Load images
try:
    background = pygame.image.load("background.jpg")
    rocket = pygame.image.load("rockets.png")
    meteor_images = [
        pygame.image.load("meteor2.png"),
        pygame.image.load("meteor3.png"),
    ]
except pygame.error as e:
    print("Error loading image:", e)
    pygame.quit()
    sys.exit()

# Rocket initial position and velocity
rocket_width, rocket_height = rocket.get_width(), rocket.get_height()
rocket_x, rocket_y = width // 2 - rocket_width // 2, 650
rocket_vel = 10

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 9

    def move(self):
        self.y -= self.vel

# Meteor class
class Meteor:
    def __init__(self):
        self.image = random.choice(meteor_images)
        self.x = random.randint(0, width - self.image.get_width())
        self.y = random.randint(-height, 0)
        # Initial velocity range
        self.vel = random.uniform(0., 5 )

    def update_position(self):
        self.y += self.vel
        if self.y > height:
            self.reset_position()

    def reset_position(self):
        self.y = random.randint(-height, 0)
        self.x = random.randint(0, width - self.image.get_width())

# Initialize meteors, bullets, and game variables
num_meteors = 8 
meteors = [Meteor() for _ in range(num_meteors)]
bullets = []
clock = pygame.time.Clock()
score = 0
lives = 5  
invulnerability_cooldown = 0

# Flag to indicate whether the game has started
game_started = False

# Main game loop
running = True
while running and lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Show start screen if the game hasn't started yet
    if not game_started:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        title_text = font.render("METEOR RUSH", True, (255, 255, 255))
        start_text = font.render("Press SPACE to start", True, (255, 255, 255))

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))

        pygame.display.flip()

        # Check for spacebar press to start the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_started = True

    if game_started:
        # Handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and rocket_x - rocket_vel >= 0:
            rocket_x -= rocket_vel
        if keys[pygame.K_RIGHT] and rocket_x + rocket_vel <= width - rocket_width:
            rocket_x += rocket_vel

        # Handle firing bullets with the spacebar
        if keys[pygame.K_SPACE] and len(bullets) == 0:
            bullet = Bullet(rocket_x + rocket_width // 2, rocket_y)
            bullets.append(bullet)

        # Update screen
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Update and draw meteors
        for meteor in meteors:
            meteor.update_position()
            screen.blit(meteor.image, (meteor.x, meteor.y))

            # Check for collisions between rocket and meteors
            if (
                rocket_x < meteor.x + meteor.image.get_width()
                and rocket_x + rocket_width > meteor.x
                and rocket_y < meteor.y + meteor.image.get_height()
                and rocket_y + rocket_height > meteor.y
            ):
                # Check invulnerability cooldown
                if invulnerability_cooldown == 0:
                    # Collision detected, decrement lives and set invulnerability cooldown
                    lives -= 1
                    invulnerability_cooldown = 60  # Cooldown duration in frames (1 second at 60 fps)
                    if lives == 0:
                        running = False  # Game over when lives reach 0
                    else:
                        # Reset rocket position if there are remaining lives
                        rocket_x, rocket_y = width // 2 - rocket_width // 2, 650

        # Update invulnerability cooldown
        if invulnerability_cooldown > 0:
            invulnerability_cooldown -= 1

        # Update and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            pygame.draw.circle(screen, (255, 0, 0), (int(bullet.x), int(bullet.y)), 5)

            # Check if the bullet is out of the screen (above the top boundary)
            if bullet.y <= 0:
                bullets.remove(bullet)

            # Check for collisions between bullets and meteors
            for meteor in meteors[:]:
                if (
                    bullet.x < meteor.x + meteor.image.get_width()
                    and bullet.x + 5 > meteor.x
                    and bullet.y < meteor.y + meteor.image.get_height()
                    and bullet.y + 5 > meteor.y
                ):
                    # Collision detected, remove bullet and meteor
                    bullets.remove(bullet)
                    meteors.remove(meteor)
                    meteors.append(Meteor())  # Replace destroyed meteor with a new one
                    score += 5  # Increase the score

        # Draw the rocket
        screen.blit(rocket, (rocket_x, rocket_y))

        # Draw the score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (5, 5))

    # Update display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(80)  # Adjust the frame rate as needed

# Game over message
if lives == 0:
    print("Game Over - No Lives Remaining")
else:
    print("Game Over - Player Quit")

# Quit Pygame
pygame.quit()
sys.exit()  # Ensure that sys.exit() is called to terminate the script
