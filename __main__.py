#!/usr/bin/python

import readline
import sys
import nali_interpreter

if len(sys.argv) > 1:
    i = interpreter.Interpreter()
    
    for line in open(sys.argv[1], 'r'):
        i.eval(line)
else:
    nali_interpreter.repl()
