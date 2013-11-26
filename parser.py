# -*- coding: utf-8 -*-

"""
Parser module which is relevant to parse a rawtext-file into a specific
XML - Format
Author: Robert R.
Version: 0.4

This file is the main-file and should be called as main in order to parse
a certain document

The project can be altered to fit for different needs

format convention of the raw-text:
    - name should be always in the first line of a new entry
    - no headers
    - no frontpages or other text besides the entries
    - birth needs to be indicated with *
    - father needs to be listed first with V:
    - mother needs to be listed with M:
    - daughter needs to be listed with T. and a son with S.
    - ordination needs to be adressed with ord.
    - the core information of each entry should never contain a blank line
    - a whole entry needs to have one blank line before the source

current bugs:
    - encoding in output file
    - misc is not properly parsed
    - education is not implemented
    - offspring does not work properly
"""

from segmentAnalyzer import SegmentAnalyzer
from vicar import Vicar
import codecs


class Parser:

    def __init__(self, fileName):
        self.filename = fileName

    def readInputFile(self):              # reads the input file
        f = open(self.filename, 'r')
        text = []
        for line in f:
            text.append(line)
        f.close()
        return text

    def segmentation(self, text):         # creates segments from the text
        segments = []
        segment = []
        count = 0
        for line in text:
            if count == 1 and line == "\n":
                segment.append(line)
                count = 5
            elif count == 5 and line == "\n":
                segment.append(line)
                count = 0
                segments.append(segment[:])
                segment[:] = []
            elif count == 5 and line != "\n":
                segments.append(segment[:])
                segment[:] = []
                segment.append(line)
                count = 0
            elif count == 0 and line == "\n":
                segment.append(line)
                count = count + 1
            else:
                segment.append(line)
        return segments


def main():
    """
    main method for this project which creates the outputfile
    """
    output = open('outputTex.txt', 'w+')
    parser = Parser('inputText.txt')
    output.write('<file>\n')
    for segment in parser.segmentation(parser.readInputFile()):
        vicar = Vicar('k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.',
                      'k.A.', 'k.A.')
        analyzer = SegmentAnalyzer(segment, vicar)
        output.write(analyzer.createEntry())
    output.write('</file>')
    output.close

if __name__ == '__main__':                # call if module is called as main
    main()