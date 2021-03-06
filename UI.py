import pygame
import sys
import Main as ProgramMa


class pygameUI:

    def __init__(self, colour, Font, FontSize):
        self.Program = ProgramMa.main()
        pygame.init()
        self.res = (400, 350)

        self.screen = pygame.display.set_mode(self.res)

        self.colour = colour[0]
        self.colourLight = colour[1]
        self.colourDark = colour[2]

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.smallfont = pygame.font.SysFont(Font, FontSize)

    def EventChecks(self, event):
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # quit
                if 0 <= self.mouse[0] <= 120 and 0 <= self.mouse[1] <= 30:
                    sys.exit("Program Quit")

                # List
                if 0 <= self.mouse[0] <= 120 and 35 <= self.mouse[1] <= 65:
                    self.Program.Input(3)

                # List
                if 0 <= self.mouse[0] <= 120 and 70 <= self.mouse[1] <= 100:
                    self.Program.Input(4)

                # Settings
                if 0 <= self.mouse[0] <= 120 and 105 <= self.mouse[1] <= 135:
                    self.Program.Input(1)

                # Test File
                if 0 <= self.mouse[0] <= 120 and 140 <= self.mouse[1] <= 170:
                    self.Program.Input(5)

                # Print File
                if 0 <= self.mouse[0] <= 120 and 175 <= self.mouse[1] <= 205:
                    self.Program.Input(2)

                # Move Files
                if 0 <= self.mouse[0] <= 120 and 210 <= self.mouse[1] <= 240:
                    self.Program.Input(7)

                # Move Files Back
                if 0 <= self.mouse[0] <= 120 and 245 <= self.mouse[1] <= 275:
                    self.Program.Input(8)

                # Test File
                if 0 <= self.mouse[0] <= 120 and 280 <= self.mouse[1] <= 310:
                    self.Program.Input(9)

                # Next point for when we need it.
                # if 0 <= self.mouse[0] <= 120 and 315 <= self.mouse[1] <= 345:
                #     self.Program.Input(9)

            if ev.type == pygame.QUIT:
                # pygame.quit()
                # StartUp()  # make sure that the program can still be used
                sys.exit("Program Quit")

    def DrawButtons(self):
        # Quit Button
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 0, 120, 30])
        self.screen.blit(self.smallfont.render('Quit', True, self.colourLight), (45, 10))  # noqa
        self.screen.blit(self.smallfont.render('Exits the program', True, self.colourLight), (120, 10))  # noqa

        # List Files
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 35, 120, 30])
        self.screen.blit(self.smallfont.render('List Files', True, self.colourLight), (25, 45))  # noqa
        self.screen.blit(self.smallfont.render('Shows all files in specified folder', True, self.colourLight), (120, 45))  # noqa

        # Clean Up
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 70, 120, 30])
        self.screen.blit(self.smallfont.render('Clean up Files', True, self.colourLight), (10, 80))  # noqa
        self.screen.blit(self.smallfont.render("Removes temporary files", True, self.colourLight), (120, 75))  # noqa
        self.screen.blit(self.smallfont.render("(this should be automatic)", True, self.colourLight), (120, 85))  # noqa

        # settings
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 105, 120, 30])
        self.screen.blit(self.smallfont.render('Settings', True, self.colourLight), (30, 115))  # noqa
        self.screen.blit(self.smallfont.render('Lets you change your settings', True, self.colourLight), (120, 115))  # noqa

        # Make test file
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 140, 120, 30])
        self.screen.blit(self.smallfont.render('Test file', True, self.colourLight), (30, 150))  # noqa
        self.screen.blit(self.smallfont.render('Makes a file without printing it', True, self.colourLight), (120, 145))  # noqa
        self.screen.blit(self.smallfont.render('Usefull for testing.', True, self.colourLight), (120, 155))  # noqa

        # Print file
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 175, 120, 30])
        self.screen.blit(self.smallfont.render('Print file', True, self.colourLight), (30, 180))  # noqa
        self.screen.blit(self.smallfont.render('Makes a file and prints it', True, self.colourLight), (120, 180))  # noqa

        # Move Files
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 210, 120, 30])
        self.screen.blit(self.smallfont.render('Moves Files', True, self.colourLight), (20, 250))  # noqa
        self.screen.blit(self.smallfont.render('Moves files on google drive', True, self.colourLight), (120, 250))  # noqa
        self.screen.blit(self.smallfont.render('(shold be automatic)', True, self.colourLight), (120, 260))  # noqa

        # Move Files back
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 245, 120, 30])
        self.screen.blit(self.smallfont.render('Moves Files Back', True, self.colourLight), (20, 285))  # noqa
        self.screen.blit(self.smallfont.render('Moves files on google drive', True, self.colourLight), (120, 285))  # noqa
        self.screen.blit(self.smallfont.render('ONLY WORKS WITH RECENT FILES MOVED (and in memory)', True, self.colourLight), (120, 295))  # noqa

        # Test file
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 280, 120, 30])
        self.screen.blit(self.smallfont.render('Test File', True, self.colourLight), (20, 320))  # noqa
        self.screen.blit(self.smallfont.render('Prints an 8 page blank pdf', True, self.colourLight), (120, 320))  # noqa

    def DrawObjectsToDisplay(self):
        pygame.display.update()

    def Main(self):
        print("Program ready")
        while True:
            # This HAS to go before anything else.(otherwise we can't see that)
            self.screen.fill((128, 128, 128))

            self.mouse = pygame.mouse.get_pos()
            # print(f"mouse Pos:{self.mouse}")
            self.EventChecks(pygame.event.get())
            self.DrawButtons()
            self.DrawObjectsToDisplay()


# TODO: add more settings for ui?
ui = pygameUI(
    [(0, 0, 0), (255, 255, 255), (50, 50, 50)],
    'Corbel',
    20)

ui.Main()
