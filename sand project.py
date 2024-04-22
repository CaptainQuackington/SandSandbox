import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
SAND_SIZE = 5
SAND_COLOR = (194, 178, 128)
GRAVITY = 0.5
MAX_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sand Simulator')
clock = pygame.time.Clock()

class SandParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.settled = False

    def update(self):
        if self.settled:
            return

        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, MAX_SPEED)
        self.y += self.velocity_y

        # Check for collisions with other particles
        for particle in sand_particles:
            if particle is not self:
                if self.is_colliding(particle):
                    self.handle_collision(particle)
                    return  # Stop falling if collision occurs

        # Boundary check
        if self.y >= HEIGHT - SAND_SIZE:
            self.y = HEIGHT - SAND_SIZE
            self.settled = True
        elif self.x < 0:
            self.x = 0
        elif self.x >= WIDTH:
            self.x = WIDTH - SAND_SIZE

    def is_colliding(self, other_particle):
        return (abs(self.x - other_particle.x) < SAND_SIZE) and (abs(self.y - other_particle.y) < SAND_SIZE)

    def handle_collision(self, other_particle):
        if self.y < other_particle.y:
            # Adjust velocity to stop falling
            self.velocity_y = 0
            self.y = other_particle.y - SAND_SIZE

            # Check for space on sides when hitting another particle
            if self.space_on_side(-SAND_SIZE) and self.space_on_side(SAND_SIZE):
                # Randomly choose to move left or right
                if random.random() < 0.5:
                    self.move_side(-SAND_SIZE)
                else:
                    self.move_side(SAND_SIZE)
            elif self.space_on_side(-SAND_SIZE):
                self.move_side(-SAND_SIZE)
            elif self.space_on_side(SAND_SIZE):
                self.move_side(SAND_SIZE)
            else:
                # Settle if no space to move
                self.velocity_y = 0
                self.settled = True

            # Check if two blocks are lined up next to each other on the x-axis
            if abs(self.x - other_particle.x) == SAND_SIZE:
                # Stop falling if two blocks are lined up next to each other
                self.velocity_y = 0
                self.y = other_particle.y - SAND_SIZE

    def space_on_side(self, offset):
        for particle in sand_particles:
            if particle is not self and (self.x + offset == particle.x and self.y == particle.y):
                return False
        return True

    def move_side(self, offset):
        self.x += offset

    def draw(self):
        pygame.draw.rect(screen, SAND_COLOR, (self.x, self.y, SAND_SIZE, SAND_SIZE))

# List to hold sand particles
sand_particles = []

# Main loop
running = True
clicking = False
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicking = False
            
    x, y = pygame.mouse.get_pos()     
    if clicking:
        # Check if there's already a particle at this position
        particle_at_pos = any(particle.x == x and particle.y == y for particle in sand_particles)
        if not particle_at_pos:
            sand_particles.append(SandParticle(x, y))

    # Update particles
    for particle in sand_particles:
        particle.update()
        particle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
