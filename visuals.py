import pygame


class Particle(object):

    def __init__(self, x, y, particle_type, motion, decay_rate, start_frame, custom_color=None, physics=False):
        self.x = x
        self.y = y
        self.type = particle_type
        self.motion = motion
        self.decay_rate = decay_rate
        self.color = custom_color
        self.frame = start_frame
        self.physics = physics
        self.orig_motion = self.motion
        self.temp_motion = [0, 0]
        self.time_left = len(particle_images[self.type]) + 1 - self.frame
        self.render = True
        self.random_constant = random.randint(20, 30) / 30

    def draw(self, surface, scroll):
        global particle_images
        if self.render:
            #if self.frame > len(particle_images[self.type]):
            #    self.frame = len(particle_images[self.type])
            if self.color == None:
                blit_center(surface,particle_images[self.type][int(self.frame)],(self.x-scroll[0],self.y-scroll[1]))
            else:
                blit_center(surface,swap_color(particle_images[self.type][int(self.frame)],(255,255,255),self.color),(self.x-scroll[0],self.y-scroll[1]))

    def update(self, dt):
        self.frame += self.decay_rate * dt
        self.time_left = len(particle_images[self.type]) + 1 - self.frame
        running = True
        self.render = True
        if self.frame >= len(particle_images[self.type]):
            self.render = False
            if self.frame >= len(particle_images[self.type]) + 1:
                running = False
            running = False
        if not self.physics:
            self.x += (self.temp_motion[0] + self.motion[0]) * dt
            self.y += (self.temp_motion[1] + self.motion[1]) * dt
            if self.type == 'p2':
                self.motion[1] += dt * 140
        self.temp_motion = [0, 0]
        return running
    
def blit_center(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2))

def blit_center_add(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

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