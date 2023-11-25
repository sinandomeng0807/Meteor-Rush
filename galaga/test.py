import pygame
import random
import sys  # Import the sys module for sys.exit()

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
        pygame.image.load("meteor1.png"),
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
        self.vel = random.uniform(0., 5)

    def update_position(self):
        self.y += self.vel
        if self.y > height:
            self.reset_position()

    def reset_position(self):
        self.y = random.randint(-height, 0)
        self.x = random.randint(0, width - self.image.get_width())

# Initialize meteors
num_meteors = 5
meteors = [Meteor() for _ in range(num_meteors)]

# Initialize bullets
bullets = []

# Set up the game clock
clock = pygame.time.Clock()

# Initialize score
score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Draw the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (5, 5))

    # Update display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(80)  # Adjust the frame rate as needed

    # Check for game over condition
    if len(meteors) == 0:
        running = False

    # Adjust meteor velocity based on the score
    if score >= 50:
        for meteor in meteors:
            meteor.vel += 0.1  # Increase the velocity

# Quit Pygame
pygame.quit()
sys.exit()  # Ensure that sys.exit() is called to terminate the script
