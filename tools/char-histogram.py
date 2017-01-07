#
# output an aggregated histogram of characters for all text files in a folder
import glob, os, sys
from collections import Counter


def load_files(folder):
    """Load all text files in folder and return character histogram data and
    files contaning blocked characters."""

    print("Working on %s" % folder)

    # List files containing these chars
    blockchars = "©£€»þ"

    blockfiles = {}
    for char in blockchars:
        blockfiles[char] = []


    # count chars in txt files
    c = Counter()

    for file in glob.glob(folder + "/*/*.txt"):
        with open(file) as f:
            for line in f:
                c += Counter(line)
                for char in line:
                    if char in blockchars:
                        blockfiles[char].append(file)

    return c, blockfiles


if __name__ == "__main__":
    c, blockfiles = load_files(sys.argv[1])
    print("Total chars %s" % sum(c.values()))

    for char, count in c.most_common():
        print(char, count)

    for item in blockfiles:
        print(item)
