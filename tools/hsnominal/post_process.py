# coding=utf8
import os
import sys
import re
import io

# Find and repair text

# Find pattern with at leat three characters
# separated by a space,where the first char is capital A-Ö or 4.
# and the consecutive chars are lowercase a-ö or 4 or 1.
#
regex = r"([A-Ö4] ([a-ö41] ){2,}[a-ö41])"

def clean(path):

    with open(path, 'r') as f:
        filedata = f.read()

        # Find spaced words
        matches = re.finditer(regex, filedata)

        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1

            filedata = fixup(filedata, match.group())

        with io.open(f"{path}.clean.txt", 'w', encoding='utf8') as rf:
            rf.write(filedata)



def fixup(ocr_text, pattern):
    """Fix spacing and numerics in ocr text"""
    cleaned_pattern = pattern.replace("4", "A").replace("1","l").replace(" ","")

    #print(f"{pattern}\t\t{cleaned_pattern}")
    #print("{0:<30} {1:<10}".format(pattern, cleaned_pattern))

    return ocr_text.replace(pattern, cleaned_pattern)



if __name__ == "__main__":
    path = sys.argv[1] + ".txt"
    clean(path)
