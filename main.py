import pygame
from display import ScreenManager, MainScreen

pygame.init()

class Engine():
    def __init__(self):
        self.display = pygame.display.set_mode((1200, 720))
        self.screenManager = ScreenManager()
        self.mainScreen = MainScreen(self.display)
        self.screenManager.show(self.mainScreen)

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screenManager.inputs(event)

            self.screenManager.update()
            self.screenManager.render()
            pygame.display.flip()
        pygame.quit()

engine = Engine()
engine.start()