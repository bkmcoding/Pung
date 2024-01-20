import pygame, time, math, random, sys
from visuals import *

pygame.init()
pygame.display.set_caption('Pung')

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# game variables
fps = 60
paddle_height = 75
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3
enemy_score = 0
player_score = 0
game_status = 0

class Button:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'assets/{image}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
        else:
            self.hover = False

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        else:
            self.clicked = False
    
    def update(self, mouse_pos):
        self.check_hover(mouse_pos)
        self.check_click(mouse_pos)
        if self.hover:
            pass
        if self.clicked:
            return True
        else: False

class Menu:
    def __init__(self):
        self.menu = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.status = "Main"
        self.menu_enabled = True
        self.particles = []
        
        self.load_assets()

    def load_assets(self):
        self.logo = pygame.image.load("assets/PungLogotest1.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (384, 256))
        self.logo_pos = (SCREEN_WIDTH // 2 - self.logo.get_width() // 2, SCREEN_HEIGHT // 4 - self.logo.get_height() // 2)
        self.start_button = Button(SCREEN_WIDTH // 2 - 384 / 2, SCREEN_HEIGHT // 2, 384, 256, "start_button")

    def star_effect(self):
        self.particles.append(
                Particle(
                    random.randint(0,SCREEN_WIDTH * 2),
                    0,
                    -0.1,
                    random.randint(11, 18) / 10 - 1,
                    random.randint(4, 6),
                    0.005,
                    0,
                    self.menu,
                )
            )


    def check_status(self):
        self.menu.fill((0, 0, 0))
        self.star_effect()
        for particle in self.particles:
            particle.update()
            if particle.radius <= 0:
                self.particles.remove(particle)
        if self.status == "Main":
            self.main_menu()
        elif self.status == "Settings":
            self.settings_menu()
        elif self.status == "Credits":
            self.credits_menu()
        elif self.status == "Quit":
            pygame.quit()
            sys.exit()
    
    def main_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        self.menu.blit(self.logo, self.logo_pos)
        self.menu.blit(self.start_button.image, self.start_button.rect)
        self.start_button.update(mouse_pos)


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

    def update(self):
        if not game_status:
            self.toggle = True

    def change_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

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
            return 0
        else:
            self.toggle = False
            self.set_default()
            return 1


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
        self.round_over = [0,0]

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (round(self.x_pos), round(self.y_pos)), self.radius)

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

        # gravity
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
        if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0):
            self.round_over[0] = 1
        if (self.x_pos > SCREEN_WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
            self.round_over[1] = 1

        # paddle bounce
        collision = [False, False]
        if not pog.toggle:
            for paddle in paddles:
                if self.rect.colliderect(paddle.rect):
                    collision[0] = True
                    if (
                            self.rect.right >= paddle.rect.left
                            and self.old_rect.right <= paddle.old_rect.left
                        ):
                            self.rect.right = paddle.rect.left
                            self.x_pos = self.rect.centerx
                            self.x_speed *= -1
                            collision[1] = True

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


menu = Menu()
ball = Ball(SCREEN_WIDTH / 2 - 15, 50, 30, 'white', 100, .75, 0, 0, 1, 0.02)
pog = POG(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 5, True)
player = Paddle(paddle_height / 4, SCREEN_WIDTH / 2 - paddle_height / 2, 15, paddle_height, 'white')
enemy = Paddle(SCREEN_WIDTH - paddle_height / 2, SCREEN_HEIGHT / 2 - paddle_height / 2, 15, paddle_height, 'white')
fps_counter = FPS()
particles = []
sparks = []
pog.set_circle(2000)
previous_time = time.time()
run = True


def game_loop():
    dt = time.time() - previous_time
    previous_time = time.time()
    clock.tick(fps)
    fps_counter.get_time()
    screen.fill("black")
    walls = draw_walls()
    mouse_coords = pygame.mouse.get_pos()
    player.update_pos(mouse_coords[1] - player.height / 2)
    enemy.update_pos(ball.y_pos - enemy.height / 2)
    player.draw()
    enemy.draw()
    ball.draw()
    ball.check_pog(pog)
    collision = ball.check_forces([player, enemy])
    ball.update_pos(dt)
    if ball.round_over[0] == 1:
        enemy_score += 1
        game_status = 0
    if ball.round_over[1] == 1:
        player_score += 1
        game_status = 0
    print(ball.round_over)
    pog.update()

    if collision[0]:
        if collision[1]:
            for i in range(15):
                particles.append(
                    Particle(
                        ball.x_pos,
                        ball.y_pos + ball.radius * 2,
                        random.randint(0, 40) / 10 - 1,
                        random.randint(-50, 10) / 10 - 1,
                        random.randint(4, 6),
                        0.1,
                        0.1,
                        screen,
                    )
                )
                pass
            for i in range(30):
                sparks.append(
                    Spark(
                        [ball.x_pos, ball.y_pos + ball.radius * 2],
                        math.radians(random.randint(90, 270)),
                        random.randint(2, 9),
                        (255, 255, 255),
                        2,
                    )
                )
        else:
            for i in range(15):
                particles.append(
                    Particle(
                        ball.x_pos,
                        ball.y_pos + ball.radius * 2,
                        random.randint(0, 40) / 10 - 1,
                        random.randint(-50, 10) / 10 - 1,
                        random.randint(4, 6),
                        0.1,
                        0.1,
                        screen,
                    )
                )
                pass
            for i in range(30):
                sparks.append(
                    Spark(
                        [ball.x_pos, ball.y_pos + ball.radius * 2],
                        math.radians(random.randint(-90, 90)),
                        random.randint(2, 9),
                        (255, 255, 255),
                        2,
                    )
                )

    if game_status == 0:
        game_status = pog.circle()
    for particle in particles:
        particle.update()
        if particle.radius <= 0:
            particles.remove(particle)

    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)

    fps_counter.render(dt, screen)


while run:
    if menu.menu_enabled:
        menu.check_status()
        screen.blit(menu.menu, (0, 0))
    else:
        game_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

