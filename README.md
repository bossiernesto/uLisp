#uLisp

A small Scheme Interpreter done in Python

##Objectives

  Create a Scheme language from Python, by first creating an interpreter based on a Python implementation.


## Working examples

  We can interpret simple expresions like the one below:

  ```python
    evaluator = SyntacticEvaluator()
    global_env = add_globals(Environment())
    parser = uLispParser()

    parser.parse(('(begin '
                  '(car (list 3 2))'
                  ')'))
    evaluator.evaluate(parsed) #returns 3
  ```

  Another simple example

  ```python
    evaluator.evaluate(parser.parse("(equal 5 3)"))
  ```

## What's missing

 - A File parser that takes a file with .scm, that will parse and interpret the results
 - A console that will support functions similar to REPL
 - Add more primitives and support for global, local functions
 - Bootstrap part of the langauage to Scheme
