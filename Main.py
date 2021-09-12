import AutoPrint as Ap
import sys
import time
import datetime
import os


class main:

    def __init__(self):
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
        print("-------------------------SETTINGS-----------------------")
        with open("APSettings.txt", 'w') as settings:
            Download = input("Google drive folder id for download files (please make sure you have access to this): ")  # noqa
            Move = input("Google drive folder id for files to move to after printing (please make sure you have access to this): ")  # noqa
            printer = input("Printer name (leave blank for none): ")
            settings.write(f"Download: {Download}\n" +
                           f" Move: {Move}\n" +
                           f" Printer: {printer}\n")
        print("----------------------------END---------------------------")

    def Input(self, choice):
        if choice == 0:  # quit
            self.Activeprint = False
            sys.exit("Program finished")
        elif choice == 1:  # settings
            self.MakeSetting()
        elif choice == 2:  # print
            self.GenFile = False
            self.PrintFiles()
        elif choice == 3:  # list
            self.GApi.List()
        elif choice == 4:  # clean up
            self.CApi.CleanUp()
        elif choice == 5:  # download no print
            self.GenFile = True
            self.PrintFiles()
        elif choice == 6:  # automate
            print("----------------------------TIMER--------------------------")  # noqa
            Time = input("Please enter a time (FORMAT: (HH:MM:SS), (24h time required)): ")  # noqa
            self.Autotime = datetime.datetime.strptime(Time, "%H:%M:%S").time()
            self.Activeprint = True
            self.AutoPrint()
            print("----------------------------END---------------------------")
        elif choice == 7:  # move Files
            self.GApi.MoveFiles()
        else:
            print("Please enter a valid number")

    def PrintFiles(self):
        if not os.path.exists("yourfile.pdf"):
            self.GApi.DownloadFiles()
            self.CApi.GenerateFile()
            time.sleep(1)
            if not self.GenFile:
                self.ActualyPrintFile()
        else:
            print("File already exists")

            if not self.GenFile:
                print("Printing file")
                self.ActualyPrintFile()
            else:
                print(f"Location to file: {os.path.dirname(__file__)}/yourfile.pdf")  # noqa

    def ActualyPrintFile(self):
        self.CApi.PrintFiles(self.Print, "yourfile.pdf")
        time.sleep(60)  # wait for print
        self.CApi.CleanUp()
        self.GApi.MoveFiles()

    def AutoPrint(self):
        try:
            while self.Activeprint:  # Stop without using ctrl + c
                if datetime.datetime.now().time() == self.Autotime:
                    print("Attempting to print file")
                    self.Input(5)
        except KeyboardInterrupt:
            print("Press 1 to quit")
        return


m = main()
