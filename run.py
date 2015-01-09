import subprocess as sp
from os import devnull
from os import system
from sys import argv

if __name__ == '__main__':
    nRuns = int(argv[1]) if len(argv) >= 2 else 1

    FNULL = open(devnull, 'w')
    pops = [sp.Popen(("java", "-jar", "engine_1.0.jar"), stdout=FNULL)
            for _ in xrange(nRuns)]
    [pop.wait() for pop in pops]
    system("mv match_*.txt output")
    system("python plot.py %d" % nRuns)

    clear = raw_input("wipe output?\n")
    if clear.strip() == "yes":
        print "wiping output"
        system("rm output/match_*")

