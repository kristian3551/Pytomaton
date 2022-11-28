"""The console app with console UI/UX."""

from typing import List
from controller import Controller
from automation import Automaton

class Engine:
    """The console app itself."""
    def __init__(self) -> None:
        self.controller: Controller = Controller()
        self.has_changes = False
    def __tokenize(self, line: str) -> List[str]:
        return line.split(' ')
    def help(self) -> None:
        """Prints user support."""
        print("""
        Supported functionalities are:

        1. add <name> from regex <regex>|empty                 -> Adds an automaton <name> with with language L(<regex>)|{\}.
        2. remove <name>                                       -> Removes automaton <name>.
        3. addstate <name> <label>                             -> Adds state with label <label> to automaton <name>.
        4. remstate <name> <label>                             -> Removes state with label <label> to automaton <name>.
        5. makefinal <name> <label>                            -> Makes state with label <label> final to automaton <name>.
        6. makeunfinal <name> <label>                          -> Removes state with label <label> from automaton <name>'s finals.
        7. setstart <name> <label>                             -> Self explanatory.
        8. addtransition <name> <label1> <letter> <label2>     -> -----||-----
        8'. removetransition <name> <label1> <letter> <label2> -> -----||-----
        9. acceptsword <name> <word>                           -> Checks if <word> is in the language of <name>. If you don't write a word,
                                                                  program will interpret it as empty word.
        10. maketotal <name>                                   -> Modifies automaton <name>.
        11. total <name>                                       -> Prints the automaton <name>, but made total.
        12. union <name1> <name2>                              -> Prints the automaton with language L(<name1>) U L(<name2>).
        13. concat <name1> <name2>                             -> Self explanatory.
        14. star <name>                                        -> Prints the automaton with language L(<name>)*.
        15. complement <name>                                  -> Prints the automaton with language sigma* \ L(<name>).
        16. intersect <name1> <name2>                          -> Prints the automaton with language L(<name1>) ^ L(<name2>).
        17. determinize <name>                                 -> Prints the determinized version of automaton <name>.
        18. minimize <name>                                    -> Prints the minimized (and determinized) version of automaton <name>.
        19. reverse <name>                                     -> Prints the automaton with language L(<name>)^rev.
        20. save                                               -> Saves all automatons in text file.
        21. exit                                               -> Exit from the app.
        """)
    def run(self) -> None:
        """Actual console app."""
        self.controller.load_from_file()
        print("Hello to my application! Please choose a command or type 'help' for more info!")
        line: str = 'default_noempty_line'
        while line:
            print('----------------------------------------')
            line = input("> ")
            tokens: List[str] = self.__tokenize(line)
            command: str = tokens[0]
            try:
                if command == 'add':
                    if tokens[2] == 'from' and tokens[3] == 'regex':
                        if self.controller.add_automaton(tokens[1],\
                             self.controller.from_regex(tokens[4])):
                            self.has_changes = True
                            print(f'Automaton {tokens[1]} added successfully')
                        else:
                            print("Automaton added unsuccessfully!")
                    elif tokens[2] == 'empty':
                        if self.controller.add_automaton(tokens[1], Automaton()):
                            self.has_changes = True
                            print(f'Automaton {tokens[1]} added successfully')
                        else:
                            print("Automaton added unsuccessfully!")
                    else:
                        print("Automaton added unsuccessfully!")
                elif command == 'addstate':
                    if self.controller.add_state(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'remove':
                    if self.controller.remove_automaton(tokens[1]):
                        print(f'Automaton {tokens[1]} successfully removed!')
                elif command == 'print':
                    self.controller.print_automaton(tokens[1])
                elif command == 'printall':
                    self.controller.print()
                elif command == 'remstate':
                    if self.controller.remove_state(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'makefinal':
                    if self.controller.make_state_final(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'makeunfinal':
                    if self.controller.make_state_unfinal(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'setstart':
                    if self.controller.set_start(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'removestart':
                    if self.controller.remove_start(tokens[1], tokens[2]):
                        self.has_changes = True
                elif command == 'addtransition':
                    if self.controller.add_transition(tokens[1], tokens[2], tokens[3], tokens[4]):
                        self.has_changes = True
                elif command == 'removetransition':
                    if self.controller.remove_transition(tokens[1], tokens[2], tokens[3], tokens[4]):
                        self.has_changes = True
                elif command == 'acceptsword':
                    word: str = tokens[2] if len(tokens) > 2 else ''
                    print(f"'{word}' is", "ACCEPTED" if self.controller.accepts_word(\
                        tokens[1], word) else "REJECTED.")
                elif command == 'maketotal':
                    self.controller.make_total(tokens[1])
                elif command == 'total':
                    print(self.controller.total(tokens[1]))
                elif command == 'union':
                    print(self.controller.union(tokens[1], tokens[2]))
                elif command == 'concat':
                    print(self.controller.concat(tokens[1], tokens[2]))
                elif command == 'star':
                    print(self.controller.star(tokens[1]))
                elif command == 'complement':
                    print(self.controller.complement(tokens[1]))
                elif command == 'intersect':
                    print(self.controller.intersection(tokens[1], tokens[2]))
                elif command == 'determinize':
                    print(self.controller.determinize(tokens[1]))
                elif command == 'minimize':
                    print(self.controller.minimize(tokens[1]))
                elif command == 'reverse':
                    print(self.controller.reverse(tokens[1]))
                elif command == 'save':
                    self.controller.save_in_file()
                    print('Automatons successfully saved.')
                    self.has_changes = False
                elif command == 'help':
                    self.help()
                elif command == 'show':
                    self.controller.show_automaton(tokens[1])
                elif command == 'exit':
                    if self.has_changes:
                        print('Changes have been made. Save it first or type exit again!')
                        line = input("> ")
                        if line == 'exit':
                            line = ''
                            print("Goodbye!")
                        else:
                            self.controller.save_in_file()
                            self.has_changes = False
                    else:
                        line = ''
                        print("Goodbye!")
                elif command == 'clear':
                    self.controller.clear()
                elif tokens[1] == '=':
                    if self.controller.contains(tokens[0]):
                        self.controller.remove_automaton(tokens[0])
                    if tokens[2] == 'from' and tokens[3] == 'regex':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.from_regex(tokens[4]))
                    elif tokens[2] == 'empty':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.empty_automaton())
                    elif tokens[2] == 'concat':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.concat(tokens[3], tokens[4]))
                    elif tokens[2] == 'union':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.union(tokens[3], tokens[4]))
                    elif tokens[2] == 'star':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.star(tokens[3]))
                    elif tokens[2] == 'minimize':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.minimize(tokens[3]))
                    elif tokens[2] == 'determinize':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.determinize(tokens[3]))
                    elif tokens[2] == 'reverse':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.reverse(tokens[3]))
                    elif tokens[2] == 'total':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.total(tokens[3]))
                    elif tokens[2] == 'complement':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.complement(tokens[3]))
                    elif tokens[2] == 'intersect':
                        self.controller.add_automaton(tokens[0],\
                            self.controller.intersection(tokens[3], tokens[4]))
                    else:
                        if self.controller.contains(tokens[0]):
                            self.controller.remove_automaton(tokens[0])
                        self.controller.add_automaton(tokens[0],\
                             self.controller.get_automaton(tokens[2]))
                    self.has_changes = True
                else:
                    print("Invalid command! Type 'help' for more info!")
            except KeyError as error:
                print(error.args[0])
            except IndexError as error:
                print(f"{error.args[0]} Type 'help' for more info!")
            except ValueError as error:
                print(error.args[0])
