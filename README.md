# Pytomaton
## Summary
A library/desktop/console application for working with finite state automatons. Pytomaton is a project for passing Python programming course in FMI. It contains virtually all the main operations of (non-)deterministic finite automatons learned in *Languages, automata and computability* course in FMI. All the algorithms are a straight-forward implementations of standard automatons construction definitions. 

# How to run

1. Install [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) on your system
2. Install tkinter
    - On Windows: it comes by default with Python
    - On Mac:
      ```
      brew install python-tk
      ```
    - On Linux: refer to your distribution. Some information [here](https://stackoverflow.com/a/25905642/12036073)
3. Clone repository
    ```
    git clone https://github.com/kristian3551/Pytomaton.git
    ```
4. Install Python dependencies
    ```
    pip install -r requirements.txt
    ```
5. Run from **root of repository**
    ```
    python3 main.py
    ```
*The GUI app is runned by default. If you want to run the console app, you have to modify `main.py` file a bit. Just uncomment the row with the import from `engine.py`, initialize **app** with an instance of **ConsoleApp** and run `python3 main.py`*

## Functionality

### Automaton
The class *Automaton* in module `automation/automaton` provides all the logic for working with automatons themselves.

*Basic automaton functionality:*
1. Adding/removing automaton states
2. Managing transitions
3. Managing starting and final states
4. Checking if a word is in automaton language  

*Constructions preserving language regularity: all of the methods return a new automaton (not nessecarrily deterministic)*
1. Union (crating a new non-deterministic automaton)
2. Concatenation (crating a new non-deterministic automaton)
3. Kleene star (crating a new non-deterministic automaton)
4. Intersection: only working with deterministic automatons.
5. Complement: only working with deterministic automatons.
6. Reverse: returns a new automaton with language L(A)^rev

*More constructions:*  
1. Determinization of automatons
2. Minimization of automatons (relies on Bzozowski's theorem)

*Working with files*  
1. Saving/loading an automaton from file in right format (the format implemented in `stream-format` method in the *Automaton* class)

### RegExpr
The class *RegExpr* in module `automation/regexpr` provides all the logic for working with regular expressions in the context of the formal definition (not the built-in RegEx).
Supported functionalities are:  
1. Validating regular expression (follows the inductive definition of a regular expression)
2. Processing regular expression and building an automaton (instance of *Automaton* class) with the same language: the regular expression is converted to reverse polish notation and then parsed to an automaton in the `compile` method

## Application

### Controller
The class *Controller* in module `automation/controller` represents the application itself. An instance if the *Controller* class is used in both `automation/engine.py` and `automation/app.py` and holds all of the application's supported functionality (not necessarily all of the implemented functionality in *Automaton* and *RegExpr* classes). It holds the logic for creating a .png file from an automaton using `Graphviz` library. The .png is saved in *database* folder. All the automatons in *Controller* are saved by default in `database/automatons.txt` in right format. If you want, you can change it by modifying `DEFAULT_DATABASE_PATH` constant in *Controller*.

### Engine
The class *Engine* in module `automation` holds all the logic of the console app. If you run the command `help` after starting the console app, you can find instructions for working with the automaton repository.

### App
The classes in `automation/app.py` implement the GUI in the application. Tkinter is used for creating the graphical interface.

## Tests
You can run all the tests in `tests/` by typing `python -m pytest -s` in terminal.

## Future improvements
1. Make GUI more beautiful
2. Implementing algorithm for building a regex for an automaton using Kleene's theorem
3. Adding more advanced automaton constructions
