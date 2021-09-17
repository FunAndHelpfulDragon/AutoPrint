# File for running in crontab
print("a")
import Main
print("b")
m = Main.main()
print("c")
m.Activeprint = True
print("Started")
m.Input(2)
print("e")
