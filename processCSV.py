#!/usr/bin/python3
#pipes.py

"""
NYC OPEN DATA dataset comes with some rows not properly delimited by commas. 
This reads the original files and spits out a csv where the errant rows have
been properly re-formatted
"""


import csv
import pandas as pd
import numpy as np

class PipeColumns:
    def __init__(self,infile,outfile):
        self.infile = infile
        self.outfile = outfile
        
    def fixLine(self,line):
        newline = []
        for i in line:
            if len(i) != 0:
                newline.append(i)
        newline = (''.join(newline)).split('|')
        return newline

    def process_file(self):
        file = open(self.infile,'r')
        csv_object = csv.reader(file)
        unprocessed_lines = []
        processed_lines = []
        outfile = open(self.outfile, 'w')
        outfile_object = csv.writer(outfile,lineterminator='\n')    
        for line in csv_object:
            if '|' in line[0]:
                print('piper!:',line)
                line = (self.fixLine(line))
                print('Fixed result:',line)
                outfile_object.writerow(line)
            else:
                print(line)
                outfile_object.writerow(line) 
        outfile.close()