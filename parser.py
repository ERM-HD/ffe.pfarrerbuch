#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parser module which is relevant to parse a rawtext-file into a specific
XML - Format
Author: Robert R.
Version: 1.0

This file is the main-file and should be called as main in order to parse
a certain document

The project can be altered to fit for different needs

format convention of the raw-text:
    - name should be always in the first line of a new entry
    - no headers
    - no frontpages or other text besides the entries
    - first line should be the name / entry of the first vicar
    - each entry need to be seperated with a new line

bugs:
    list if any are found

to-do:
    add date inaccuracy in analyzeDate in segmentAnalyzer
"""

import sys
import getopt
from writer import Writer


class Parser:

    def __init__(self, fileName):
        self.filename = fileName

    def readInputFile(self):              # reads the input file
        f = open(self.filename, 'r', encoding="utf8")
        text = []
        for line in f:
            text.append(line)
        f.close()
        return text

    def segmentation(self, text):         # creates segments from the text
        #print("segmentation")
        segments = []
        segment = []
        ws = True
        for line in text:
            if ws and len(line.strip()) > 0:
                segment.append(line)
                ws = False
            elif not ws and len(line.strip()) > 0:
                segment.append(line)
            elif not ws and len(line.strip()) == 0:
                # check if last segment matches pattern
                if checkSegmentPattern(segment):
                    segments.append(segment)
                segment = []
                ws = True
        if checkSegmentPattern(segment):
             segments.append(segment)
        print(len(segments))
        return segments

def checkSegmentPattern(segment):
    count = 0
    o = 0 # offset
    if len(segment) < 15:
        return False
    if segment[o].strip().endswith("."):
        if segment[o].strip()[:-1].isdigit():
            segment[o:o+1] = []
    if segment[o].strip().isdigit():
        segment[o:o+1] = []
    if segment[o+1].startswith("NB!"):
        o = o + 1
    if not segment[o+1].strip().startswith("Ord.:"):
        print("ord")
        return False
    if not segment[o+2].startswith("*"):
        print("birth")
        return False
    if not segment[o+3].startswith("†"):
        print("death")
        return False
    if not segment[o+4].startswith("8") and not segment[o+4].startswith("∞"):
        print("mary")
        return False
    while not segment[o+5].startswith("P:"):
        segment[o+4] = segment[o+4] + "; " + segment[o+5]
        segment[o+5:o+6] = []
        if segment[o+6].startswith("M:"):
            break
    if not segment[o+6].startswith("M:"):
        print("m")
        return False
    if not segment[o+7].startswith("Fr:"):
        print("fr")
        return False
    if not segment[o+8].startswith("Fi:"):
        print("fi")
        return False
    if not segment[o+9].startswith("St:"):
        print("st")
        return False
    if segment[o+10].startswith("V:"):
        o = o + 1
    if not segment[o+10].startswith("LM:"):
        print("lm")
        print(segment)
        return False
    if segment[o+11].startswith("V:") or segment[o+11].startswith("V."):
        o = o + 1
    if segment[o+11].startswith("KL:"):
        o = o + 1
    if not segment[o+11].startswith("VDM:"):
        print("vdm")
        print(segment)
        return False
    if not segment[o+12].startswith("S:"):
        print("s")
        return False
    if not segment[o+13].startswith("N:"):
        print("n")
        return False
    if not segment[o+14].startswith("A:"):
        o = o - 1
    if not segment[o+15].startswith("Lit:"):
        print("lit")
        return False
    return True


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["input", "output"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-i", "--input"):
            inputFile = a
        elif o in ("-o", "--output"):
            outputFile = a

    parser = Parser(inputFile)
    writer = Writer()
    writer.fromParser(parser)
    # TODO implement dumping to stdout
    writer.dumpToFile(outputFile)


def usage():
    print("""
Please use the following options:
    -i  --input     The input file
    -o  --output    The output file (optional). If not present, the output is written to stdout
""")

if __name__ == '__main__':                # call if module is called as main
    main(sys.argv[1:])
