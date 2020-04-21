# Make python file executable
#/usr/bin/env python

# import Model-Free Learning module
import ModelFree

# import Model-Based Learning module
import ModelBased

# Open and read input file
f = open("input.txt", "r")
input_string = f.read()

# split lines in order to more easily handle input
input_string_split = input_string.splitlines()
