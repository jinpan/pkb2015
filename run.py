from os import system

if __name__ == '__main__':
    system("java -jar engine_1.0.jar > /dev/null")
    system("mv match_*.txt output")
    system("python plot.py")

    clear = raw_input("wipe output?\n")
    if clear.strip() == "yes":
        print "wiping output"
        system("rm output/match_*")

