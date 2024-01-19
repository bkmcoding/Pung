import pygame, time, math
import ui as ui

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

fps = 60
clock = pygame.time.Clock()

# game variables
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

class Game:
    def __init__(self):
        self.serve = None
        self.score = 0

# POG (point of gravity)
class POG:
    def __init__(self, x_pos, y_pos, strength, toggle):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.strength = strength
        self.toggle = toggle
        self.angle = 0
        self.speed = 10
        self.rotate_amount = 0
        self.current_rotation = 0
        # self.velocity = pygame.math.Vector2()

    def update(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def enable(self):
        self.toggle = True

    def disable(self):
        self.toggle = False

    def set_default(self):
        self.x_pos = SCREEN_WIDTH / 2
        self.y_pos = SCREEN_HEIGHT / 2

    def set_circle(self, amount: float):
        self.rotate_amount = amount

    def circle(self):
        if self.rotate_amount >= 0:
            self.x_pos = SCREEN_WIDTH / 2 + 50 * math.cos(math.radians(self.angle))
            self.y_pos = SCREEN_HEIGHT / 2 + 50 * math.sin(math.radians(self.angle))
            self.angle += self.speed
            self.rotate_amount -= self.angle
        else:
            self.toggle = False


# Paddles that can be used to knock the ball around
class Paddle:
    def __init__(self, x_pos, y_pos, width, height, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.old_rect = self.rect.copy()

    def draw(self):
        self.rect = pygame.draw.rect(screen, self.color, self.rect)

    def update_pos(self, y_pos):
        self.old_rect = self.rect.copy()
        if y_pos - self.height / 4 >= 0:
            if y_pos + self.height * 1.25 <= SCREEN_HEIGHT:  
                self.rect.y = y_pos

# The main ball that is used to score against the enemy
class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.rect = pygame.Rect(x_pos - radius, y_pos - radius + 1, radius * 2 + 1, radius * 2)
        self.old_rect = self.rect.copy()
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.friction = friction
        self.speed = 100
        self.pog_toggle = False

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (round(self.x_pos), round(self.y_pos)), self.radius)
        # self.rect = pygame.draw.rect(screen, 'red', self.rect)

    def check_pog(self, pog):
        if pog.toggle:
            self.pog_toggle = True
            distanceX = pog.x_pos - 485
            distanceY = pog.y_pos - 50
            pog_distance = math.sqrt(distanceX**2 + distanceY**2)
            if pog_distance != 0:
                target_vx = (pog.x_pos - self.x_pos) / pog_distance
                target_vy = (pog.y_pos - self.y_pos) / pog_distance
            else: 
                target_vx = 0
                target_vy = 0
            self.x_speed += target_vx * pog.strength
            self.x_speed *= 0.97
            self.y_speed += target_vy * pog.strength
            self.y_speed *= 0.97
        else: 
            self.pog_toggle = False

    def check_forces(self, paddles):
        if not pog.toggle:
            if self.y_pos < SCREEN_HEIGHT - self.radius - (wall_thickness / 2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0

        # wall bounce
        # if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
        #         (self.x_pos > SCREEN_WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
        #     self.x_speed *= -1 * self.retention
        #     if abs(self.x_speed) < bounce_stop:
        #         self.x_speed = 0

        # paddle bounce
        collision = False
        if not pog.toggle:
            for paddle in paddles:
                if self.rect.colliderect(paddle.rect):
                    collision = True
                    # if paddle.rect.right >= self.rect.left:
                    #     self.x_pos += 1
                    # else:
                    #     self.x_pos -= 1
                    # self.x_speed *= -1 * self.retention
                    if (
                            self.rect.right >= paddle.rect.left
                            and self.old_rect.right <= paddle.old_rect.left
                        ):
                            self.rect.right = paddle.rect.left
                            self.x_pos = self.rect.centerx
                            self.x_speed *= -1

                        # collision on the left
                    if (
                        self.rect.left <= paddle.rect.right
                        and self.old_rect.left >= paddle.old_rect.right
                    ):
                        self.rect.left = paddle.rect.right
                        self.x_pos = self.rect.centerx
                        self.x_speed *= -1
                    
                

        # friction
            # if self.y_speed == 0 and self.x_speed != 0:
            #     if self.x_speed > 0:
            #         self.x_speed -= self.friction
            #     elif self.x_speed < 0:
            #         self.x_speed += self.friction
                        
        return collision
    


    def update_pos(self, dt):
        self.old_rect = self.rect.copy()
        self.x_pos += self.x_speed * self.speed * dt
        self.y_pos += self.y_speed * self.speed * dt
        self.rect.x = self.x_pos - self.radius
        self.rect.y = self.y_pos - self.radius + 1

def draw_walls():
    left = pygame.draw.line(screen, 'white', (0, 0), (0, SCREEN_HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0, 0), (SCREEN_WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), wall_thickness)
    
    wall_list = [left, right, top, bottom]
    return wall_list


ball = Ball(SCREEN_WIDTH / 2 - 15, 50, 30, 'white', 100, .75, 0, 0, 1, 0.02)
pog = POG(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 5, True)
paddle_height = 75
player = Paddle(paddle_height / 4, SCREEN_WIDTH / 2 - paddle_height / 2, 15, paddle_height, 'white')
enemy = Paddle(SCREEN_WIDTH - paddle_height / 2, SCREEN_HEIGHT / 2 - paddle_height / 2, 15, paddle_height, 'white')
fps_counter = ui.FPS()
particles = []
pog.set_circle(2000)
# main game loop
run = True
previous_time = time.time()
while run:
    dt = time.time() - previous_time
    previous_time = time.time()
    clock.tick(fps)
    fps_counter.get_time()
    screen.fill('black')
    walls = draw_walls()
    mouse_coords = pygame.mouse.get_pos()
    player.update_pos(mouse_coords[1] - player.height / 2)
    enemy.update_pos(ball.y_pos - enemy.height / 2)
    player.draw()
    enemy.draw()
    # mouse_pos = pygame.mouse.get_pos()
    # pog.update(mouse_pos[0], mouse_pos[1])

    
    ball.draw()
    ball.check_pog(pog)
    if ball.check_forces([player, enemy]):

    ball.update_pos(dt)
    pog.circle()
    
    fps_counter.render(dt, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()