#!/usr/bin/python3

import csv
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from overlap import *
from random import randint
import numpy as np


overlaps_file = sys.argv[1]
coverages_file = sys.argv[2]
layout_file = sys.argv[3]

overlaps = {}
coverages = {}
ignored_dots = 0
dots = []
split = 91816

with open(overlaps_file) as f:
  for line in f:
    line = line.split("\t")
    a = int(line[0])
    av = (int(line[3]) - int(line[2])) #* 100.0 / int(line[1])
    b = int(line[5])
    bv = (int(line[8]) - int(line[7])) #* 100.0 / int(line[6])

    if a < b:
      overlaps[(a, b)] = (av, bv)
    else:
      overlaps[(b, a)] = (bv, av)

print("read overlaps")

with open(coverages_file) as f:
  for line in f:
    line = line.split(' ')
    coverages[int(line[0])] = int(line[1])

print("read coverages")

with open(layout_file) as f:
  for line in f:
    if line.startswith('>'):
      print("------------------------------")
      reads = [int(id) for id in line[line.find("Seqs") + 5:].split(",")]
      for read_a, read_b in zip(reads, reads[1:]):
        olp_av, olp_bv = overlaps[(min(read_a, read_b) + 1, max(read_a, read_b) + 1)]

        if coverages[read_a] != 0 and coverages[read_b] != 0:
          dot_a = (
            # olp_av,
            abs(coverages[read_a] - coverages[read_b]), #* 100.0 / coverages[read_a],
            'g' if (read_a < split) != (read_b < split) else 'r' if read_a <= split else 'b' #if olp_av > olp_bv else 'b'
          )
          # dot_b = (
          #   olp_bv,
          #   abs(coverages[read_b] - coverages[read_a]), #* 100.0 / coverages[read_b],
          #   'g' if (read_a < split) != (read_b < split) else 'r' if read_b <= split else 'b' #if olp_bv > olp_av else 'b'
          # )
          # if dot_a[1] > 1000.0 or dot_b[1] > 1000.0:
          #   ignored_dots += 2
          #   continue

          # dots.append(dot_a)
          print(dot_a)
          # dots.append(dot_b)

