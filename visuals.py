import pygame, math


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class Particle:
    def __init__(self, x_pos, y_pos, x_vel, y_vel, radius, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.radius = radius
        self.screen = screen

    def update(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.radius -= 0.1
        self.y_vel += 0.1
        self.circle = pygame.draw.circle(self.screen, 'white', (int(self.x_pos), int(self.y_pos)), int(self.radius))
        radius = self.radius * 2
        self.screen.blit(circle_surf(radius, (20, 20, 60)), (int(self.x_pos - radius), int(self.y_pos - radius)), special_flags=BLEND_RGB_ADD)

class Spark():
    def __init__(self, loc, angle, speed, color, scale=1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]


    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        self.speed -= 0.2

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
            pygame.draw.polygon(surf, self.color, points)

class FPS:
    def __init__(self):
        self.font = pygame.font.SysFont("Verdana", 20)
        self.fps = 0
        self.new_fps = 0
        self.history_length = 60
        self.frame_data = []
        for i in range(self.history_length):
            self.frame_data.append(60)
        self.last_tick = 0
        self.count = 0
        self.delay = 0.1
        self.visible = True

    def render(self, dt, display):
        self.get_framerate()
        if self.count >= self.delay:
            self.new_fps = self.fps
            self.count = 0
        else:
            self.count += dt
        if self.visible:
            text = self.font.render(str(self.new_fps), True, (255, 255, 255))
            display.blit(text, (10, 10))

    def get_time(self):
        t = pygame.time.get_ticks()
        time_diff = t - self.last_tick
        self.last_tick = t
        return time_diff

    def get_framerate(self):
        time_diff = self.get_time()
        try:
            time_fps = 1000 / time_diff
        except ZeroDivisionError:
            time_fps = 1000
        self.frame_data.append(time_fps)
        self.frame_data.pop(0)
        self.fps = int(sum(self.frame_data) / len(self.frame_data))