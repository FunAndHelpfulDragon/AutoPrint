# This program communicates with other files, basically the Master program.
Choice = None
while Choice is None:
    Choice = input("Do you want to use text based iterface (Recommended for low end computers) (1) or UI based interface (with a bit of text based) (2)?: ")  # noqa
    if not Choice.isdigit():
        print("A number is required")
        Choice = None
    else:
        Choice = int(Choice)
        if Choice == 1:
            import Main
            m = Main.main()
            while True:
                choice = input("What do you want to do?\n" +
                               "0 = exit,\n" +
                               "1 = change settings,\n" +
                               "2 = print,\n" +
                               "3 = List (list files in that directory),\n" +
                               "4 = Cleanup (clean up files that did not get deleted),\n" +  # noqa
                               "5 = GenFile (makes the file, doesn't print it),\n" +  # noqa
                               "6 = Automate (runs the program at XX:XX:XX time per day, also prints the file),\n" +  # noqa
                               "7 = Move files (on google drive)),\n" +
                               "8 = Move files back (on google drive)"
                               "option:")  # noqa
                if choice.isdigit():
                    m.Input(int(choice))
                else:
                    print("Please enter a number")
        elif Choice == 2:
            import UI  # noqa
            # UI IS used here, that file has it own way of doing something. that doesn't include this file.  # noqa
