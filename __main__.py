#!/usr/bin/python

import readline
import sys
import interpreter

if len(sys.argv) > 1:
    i = interpreter.Interpreter()
    
    for line in open(sys.argv[1], 'r'):
        i._eval(line)
else:
    interpreter.repl()
