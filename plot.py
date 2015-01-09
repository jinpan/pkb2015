from os import listdir
from os.path import join
from re import match
from sys import argv

from matplotlib import pyplot as plt


MYNAME = "SOCKETBOT"

def process(line):
    m = match(r'^Hand #(\d+),.*%s \((\d+)\).*$' % MYNAME, line)
    if m:
        return m.group(1), m.group(2)
    else:
        return None

if __name__ == '__main__':
    nRuns = int(argv[1])

    filenames = filter(lambda x: x.startswith('match_'), listdir('output/'))
    for filename in sorted(filenames)[-6*nRuns:]:
        xs, ys = [], []
        with open(join('output', filename)) as f:
            for line in f.readlines():
                if process(line) is not None:
                    x, y = process(line)
                    xs.append(x)
                    ys.append(y)
        plt.plot(xs, ys)

    plt.xlim(xmax=200)
    plt.show()
