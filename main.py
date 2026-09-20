import pygame
from display import ScreenManager

pygame.init()

class Engine():
    def __init__(self):
        self.display = pygame.display.set_mode((1200, 720))
        self.screenManager = ScreenManager()

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screenManager.inputs(event)

            self.screenManager.update()
            self.screenManager.render()

        pygame.quit()

engine = Engine()
engine.start()