# PyPython: writing a basic python interpreter in python

## Prerequisites

Python 3.9 (the CPython implementation of bytecodes, code objects, etc, is an "
implementation detail" that regularly changes between versions).

## Objective

Starting from python code objects (byte code, value stack? etc), write an
interpreter able to run basic python programs.

## Concepts

A *code object* is obtained after:

* reading and parsing source code -> AST
* compiled using the compiler and assembler (?) -> bytecode

*Bytecode instructions* are represented as a list of bytes, used by the
interpreter:

* some represent the instruction number (e.g. STORE_FAST, etc)
* between instruction bytes, there can be 0 or a couple bytes as an argument to
  the instruction (e.g. which variable on the value stack is it referring to)

The execution is done by the interpreter:

* inside one thread (there can be multiple in parallel)
* using the thread state, the value stack and the frame stack

The *thread state* contains, among other things:

* a unique id
* a linked list to other thread states (why?)
* the interpreter state it was spawned by (containing what?)
* the currently executing frame, the current recursion depth
* the exception currently being handled
* a GIL counter

The *frame stack* is a data type:

* made of *frame objects* (one for each function), stacked together
  during execution
* that allows variables to be returned by functions
* that contains the code objects + runtime data required to execute the code:
  arguments, local variables, global variables, built-in modules (and other
  info?)

The *value stack* is used to store variables (how?)

A function's *closure* (`f.__closure__`):

* seems to be the list of variables defined in an outer function and used by an
  inner function
* does not include globals? ex: builtins, module-level variables
* is set to None when it is empty (e.g. always the case for module-level
  functions)

## References

* https://docs.python.org/3.9/reference/datamodel.html
* https://docs.python.org/3.9/library/dis.html