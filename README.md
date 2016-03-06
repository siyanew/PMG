# PMG
Plus Minus Goto - Programming language interpreter. 
It is compatible with Python 2.

## Introduction

There is a Programming language that provided in the second section of `Computability,Complexity, and Languages Fundamentals of Theoretical Computer Science` book by `Martin D. Davis, Ron Sigal and Elaine J. Weyuker`

This programming language has 3 statements.

```
L : V = V + 1     # Increase by I the value of the variable V with label L.
V = V - 1         # If the value of V is 0, leave it unchanged; otherwise decrease by I the value of V.
if V != 0 goto L  # If the value of V is nonzero, perform the instruction with label L next;otherwise proceed to the next instruction in the list.
```

## Usage

```
from pmg import PMG

pmg_interpreter = PMG("test.pmg")
pmg_interpreter.read()

```

## Copyright

I use this [goto](http://entrian.com/goto/) module for goto in this project. Never use it.
