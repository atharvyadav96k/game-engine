import pygame
from display import ScreenManager, MainScreen, LevelScreen

pygame.init()

class Engine():
    def __init__(self):
        self.display = pygame.display.set_mode((1200, 720))
        self.screenManager = ScreenManager()
        self.screenManager.registerScreen("main-screen", lambda: MainScreen(self.display, self.screenManager))
        self.screenManager.registerScreen("level-screen", lambda: LevelScreen(self.display, self.screenManager))
        self.screenManager.route("main-screen")

    def start(self):
        running = True
        while running:
            self.display.fill((0, 0, 0))
            inputEvents = pygame.event.get()
            for event in inputEvents:
                if event.type == pygame.QUIT:
                    running = False
            self.screenManager.inputs(inputEvents)
            self.screenManager.update()
            self.screenManager.render()
            pygame.display.flip()
        pygame.quit()

engine = Engine()
engine.start()