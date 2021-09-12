import pygame
import sys
import Main as ProgramMa


class pygameUI:

    def __init__(self, colour):
        self.Program = ProgramMa.main()
        pygame.init()
        self.res = (400, 350)

        self.screen = pygame.display.set_mode(self.res)

        self.colour = colour[0]
        self.colourLight = colour[1]
        self.colourDark = colour[2]

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.smallfont = pygame.font.SysFont('Corbel', 20)

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
                if 0 <= self.mouse[0] <= 120 and 105 <= self.mouse[1] <= 140:
                    self.Program.Input(1)

                # Test File
                if 0 <= self.mouse[0] <= 120 and 140 <= self.mouse[1] <= 170:
                    self.Program.Input(5)

                # Print File
                if 0 <= self.mouse[0] <= 120 and 175 <= self.mouse[1] <= 210:
                    self.Program.Input(2)

                # Timer
                if 0 <= self.mouse[0] <= 120 and 215 <= self.mouse[1] <= 250:
                    self.Program.Input(6)

            if ev.type == pygame.QUIT:
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

        # Timer
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 210, 120, 30])
        self.screen.blit(self.smallfont.render('Timer', True, self.colourLight), (30, 215))  # noqa
        self.screen.blit(self.smallfont.render('Runs the program at a certain time', True, self.colourLight), (120, 215))  # noqa
        self.screen.blit(self.smallfont.render('and prints the file', True, self.colourLight), (120, 225))  # noqa

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


# TODO: add more settings for ui
ui = pygameUI([(0, 0, 0), (255, 255, 255), (50, 50, 50)])

Choice = None
while Choice is None:
    Choice = input("Do you want to use text based iterface (1) or UI based interface (with a bit of text based) (2)?: ")  # noqa
    if not Choice.isdigit():
        print("A number is required")
        Choice = None
    else:
        Choice = int(Choice)
        if 0 > Choice > 3:  # Choice is not 1 or 2
            print("Only 1 or 2 is allowed")
            Choice = None

if Choice == 2:
    ui.Main()
elif Choice == 1:
    while True:
        choice = input("What do you want to do? (0 = exit, 1 = change settings, 2 = print, 3 = List (list files in that directory), 4 = Cleanup (clean up files that did not get deleted), 5 = GenFile (makes the file, doesn't print it), 6 = Automate (runs the program at XX:XX:XX time per day, also prints the file)): ")  # noqa
        if choice.isdigit():
            ui.Program.Input(int(choice))
        else:
            print("Please enter a number")
else:
    print("WARNING: Invalid choice")
