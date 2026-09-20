import pygame
from display import ScreenManager, MainScreen, LevelScreen

pygame.init()

class Engine():
    def __init__(self):
        self.display = pygame.display.set_mode((1200, 720))
        self.screenManager = ScreenManager()
        self.mainScreen = MainScreen(self.display)
        self.levelScreen = LevelScreen(self.display)
        self.screenManager.show(self.mainScreen)

    def start(self):
        running = True
        while running:
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screenManager.inputs(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.screenManager.show(self.levelScreen)
                    if event.key == pygame.K_BACKSPACE:
                        self.screenManager.back()

            self.screenManager.update()
            self.screenManager.render()
            pygame.display.flip()
        pygame.quit()

engine = Engine()
engine.start()