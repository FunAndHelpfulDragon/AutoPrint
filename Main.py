import AutoPrint as Ap
import sys
import time


class main:

    def __init__(self, Aprint):
        self.Activeprint = Aprint

        # check for settings
        try:
            with open("APSettings.txt", 'r') as settings:

                items = settings.read()  # gets items

                if items != "":
                    ite = []
                    for it in items.split("\n"):
                        if it != "":
                            ite.append(it.split(":")[1])

                    # sets variables for later
                    self.Download = ite[0]
                    self.Move = ite[1]
                    self.Print = ite[2]
                    self.Clean = ite[3]

                    # Refrence needed api's
                    self.CApi = Ap.ComputerApi()
                    self.GApi = Ap.GoogleApi(self.Download[1:], self.Move[1:], self.CApi.Path)  # noqa
                else:
                    self.MakeSetting()
                    self.__init__()

        except FileNotFoundError:
            self.MakeSetting()
            time.sleep(1)  # make sure the file can be made
            self.__init__()

    def MakeSetting(self):
        with open("APSettings.txt", 'w') as settings:
            Download = input("Google drive folder id for download files (please make sure you have access to this): ")  # noqa
            Move = input("Google drive folder id for files to move to after printing (please make sure you have access to this): ")  # noqa
            printer = input("Printer name (leave blank for none): ")
            Clean = input("(RECOMMENDED) Clean up files after finished (delete downloaded files and made pdf's) (y = yes, n = no)?: ")  # noqa
            settings.write(f"Download: {Download}\n" +
                           f" Move: {Move}\n" +
                           f" Printer: {printer}\n" +
                           f" Clean: {Clean}\n")

    def Input(self, input):
        if input == 1:
            self.MakeSetting()
        elif input == 0:
            self.Activeprint = False
            sys.exit("Program finished")
        elif input == 2:
            self.GenFile = False
            self.PrintFiles()
        elif input == 3:
            self.GApi.List()
        elif input == 4:
            self.CApi.CleanUp()
        elif input == 5:
            self.GenFile = True
            self.PrintFiles()
        else:
            print("Please enter a valid number")

    def PrintFiles(self):
        self.GApi.DownloadFiles()
        self.CApi.GenerateFile()
        time.sleep(1)
        if not self.GenFile:
            self.CApi.PrintFiles(self.Print, "yourfile.pdf")
            time.sleep(60)  # wait for print
            if self.Clean.lower().replace(" ", "") == "y":
                self.CApi.CleanUp()
                self.GApi.MoveFiles()


m = main(True)

while m.Activeprint:
    choice = input("What do you want to do? (0 = exit, 1 = change settings, 2 = print, 3 = List (list files in that directory), 4 = Cleanup (clean up files that did not get deleted), 5 = GenFile (makes the file, doesn't print it)): ")  # noqa
    if choice.isdigit():
        m.Input(int(choice))
    else:
        print("Please enter a number")
