# Import and initialize the pygame library
import random
import pygame

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 941

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dirVect = [[1, 0], [0.5, -0.5], [0, -1], [-0.5, -0.5], [-1, 0], [-0.5, 0.5], [0, 1], [0.5, 0.5]]

offset = 15
distance = 20
how_many = 20

COLOR_R = 120
COLOR_G = 0
COLOR_B = 0

LINE_LENGTH = 8
LINE_WIDTH = 6

CAN_DIE = False
MIN_POPULATION = True
MIN_POPULATION_NR = 2800
death_min = 141
death_max = 196

##############

particles = []
indexElem = 0


class Particle:

    def __init__(self, x, y, direction):
        global indexElem, death_max
        self.x = x
        self.y = y
        self.xMov = x
        self.yMov = y
        self.direction = direction
        self.index = indexElem
        indexElem += 1

        if indexElem > 3000:
            indexElem %= 3000
            if death_min + 7 < death_max:
                death_max -= 6
                print(death_max)

        self.steps = random.randint(death_min, death_max)

    def move(self):
        global CAN_DIE
        self.xMov += dirVect[self.direction][0] * LINE_LENGTH
        self.yMov += dirVect[self.direction][1] * LINE_LENGTH

        if CAN_DIE:
            self.steps -= 1
            if self.steps < 0:
                self.delete()
        elif MIN_POPULATION_NR > indexElem:
            CAN_DIE = True

    def delete(self):
        for f in particles:
            if f.index == self.index:
                particles.remove(f)
                break
        del self

    def draw(self):
        if self:

            if self.xMov > SCREEN_WIDTH:
                if self.direction % 2 == 0:
                    particles.append(Particle(SCREEN_WIDTH, self.yMov, 5))
                    particles.append(Particle(SCREEN_WIDTH, self.yMov, 3))
                else:
                    if self.direction == 7:
                        particles.append(Particle(SCREEN_WIDTH, self.yMov, 5))
                    else:
                        particles.append(Particle(SCREEN_WIDTH, self.yMov, 3))
                    particles.append(Particle(SCREEN_WIDTH, self.yMov, 4))

                self.delete()

            elif self.xMov < 0:
                if self.direction % 2 == 0:
                    particles.append(Particle(0, self.yMov, 7))
                    particles.append(Particle(0, self.yMov, 1))
                else:
                    if self.direction == 3:
                        particles.append(Particle(0, self.yMov, 1))
                    else:
                        particles.append(Particle(0, self.yMov, 7))
                    particles.append(Particle(0, self.yMov, 0))

                self.delete()

            elif self.yMov < 0:
                if self.direction % 2 == 0:
                    particles.append(Particle(self.xMov, 0, 7))
                    particles.append(Particle(self.xMov, 0, 5))
                else:
                    if self.direction == 3:
                        particles.append(Particle(self.xMov, 0, 5))
                    else:
                        particles.append(Particle(self.xMov, 0, 7))
                    particles.append(Particle(self.xMov, 0, 6))
                self.delete()

            elif self.yMov > SCREEN_HEIGHT:
                if self.direction % 2 == 0:
                    particles.append(Particle(self.xMov, SCREEN_HEIGHT, 3))
                    particles.append(Particle(self.xMov, SCREEN_HEIGHT, 1))
                else:
                    if self.direction == 7:
                        particles.append(Particle(self.xMov, SCREEN_HEIGHT, 1))
                    else:
                        particles.append(Particle(self.xMov, SCREEN_HEIGHT, 3))
                    particles.append(Particle(self.xMov, SCREEN_HEIGHT, 2))
                self.delete()

            else:
                pygame.draw.line(screen, (COLOR_R, COLOR_G, COLOR_B), (self.x, self.y), (self.xMov, self.yMov),
                                 LINE_WIDTH)
                self.x = self.xMov
                self.y = self.yMov


particleStart = Particle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 6)
particles.append(particleStart)

RED_TIME = True
GREEN_TIME = False
BLUE_TIME = False

DECREASE_TIME = False

RED_TIME_D = False
GREEN_TIME_D = False
BLUE_TIME_D = False

# Run until the user asks to quit
running = True
while running:

    # User clicked the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    if RED_TIME:
        COLOR_R += 1
        if COLOR_R > 255:
            COLOR_R = 255
            GREEN_TIME = True
            RED_TIME = False

    elif GREEN_TIME:
        COLOR_G += 1
        if COLOR_G > 255:
            COLOR_G = 255
            BLUE_TIME = True
            GREEN_TIME = False

    elif BLUE_TIME:
        COLOR_B += 1
        if COLOR_B > 255:
            COLOR_B = 255
            DECREASE_TIME = True
            BLUE_TIME = False

    elif DECREASE_TIME:
        COLOR_R -= 1
        COLOR_G -= 1
        COLOR_B -= 1

        if COLOR_R == 0:
            RED_TIME = True
            DECREASE_TIME = False

    # Move and then update
    for particle in particles:
        particle.move()
        particle.draw()

    # Flip the display
    pygame.display.flip()

pygame.quit()
