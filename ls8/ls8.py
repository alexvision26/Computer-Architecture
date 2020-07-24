#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# print(sys.argv[1])

if len(sys.argv) < 2:
    print('Please pass a second filename: python3 ls8.py second_filename.py')
    sys.exit()

file_name = sys.argv[1]

cpu.load(file_name)
cpu.run()