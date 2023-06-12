This is a front end for a compiler writen in python. It uses pycparser to lex then tokenize c code. Then
the syntax tree is formated into an abstract syntax tree. Symantic analysis is then preformed on the code.
This system returns an Abstract syntax tree to be used for an IR in latter stages of the compalation procsess.