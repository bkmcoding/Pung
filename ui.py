import pygame


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