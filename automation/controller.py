"""Module for managing automatons."""

from typing import Dict, List, Set, Tuple
from automation import Automaton
from reg_expr import RegExpr
import os
import graphviz

NOT_FOUND_ERROR_MSG: str = "Automaton is not found!"
AUTOMATON_ALREADY_EXISTS_MSG: str = "Automaton already exists!"
DEFAULT_DATABASE_PATH: List[str] = ['database', 'automatons.txt']
INVALID_NAME_MSG: str = "Name is invalid!"

class Controller:
    def __init__(self) -> None:
        self.automatons: Dict[str, Automaton] = {}
    def add_automaton(self, name: str, automaton: Automaton) -> bool:
        if name in self.automatons:
            raise KeyError(AUTOMATON_ALREADY_EXISTS_MSG)
        if not name:
            raise KeyError(INVALID_NAME_MSG)
        self.automatons[name] = automaton
        return True
    def remove_automaton(self, name: str) -> bool:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        del self.automatons[name]
        return True
    def get_automaton(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(AUTOMATON_ALREADY_EXISTS_MSG)
        return self.automatons[name]
    def add_state(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        self.automatons[name].add_state(label)
        return True
    def remove_start(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        self.automatons[name].remove_start(label)
        return True
    def print_automaton(self, name: str) -> None:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        print(self.automatons[name])
    def remove_state(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        self.automatons[name].remove_state(label)
        return True
    def make_state_final(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].make_state_final(label)
    def make_state_unfinal(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].make_state_unfinal(label)
    def set_start(self, name: str, label: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].set_start(label)
    def add_transition(self, name: str, label1: str, letter: str, label2: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].add_transition(label1, letter, label2)
    def remove_transition(self, name: str, label1: str, letter: str, label2: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].remove_transition(label1, letter, label2)
    def accepts_word(self, name: str, word: str) -> bool:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].accepts_word(word)
    def make_total(self, name: str) -> None:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        self.automatons[name].make_total()
    def total(self, name: str) -> Automaton:
        if not name in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].total()
    def union(self, name1: str, name2: str) -> Automaton:
        if name1 not in self.automatons or name2 not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name1].union(self.automatons[name2])
    def concat(self, name1: str, name2: str) -> Automaton:
        if name1 not in self.automatons or name2 not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name1].concat(self.automatons[name2])
    def star(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].star()
    def complement(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].complement()
    def intersection(self, name1: str, name2: str) -> Automaton:
        if name1 not in self.automatons or name2 not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name1].intersection(self.automatons[name2])
    def determinize(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].determinize()
    def minimize(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].minimize()
    def reverse(self, name: str) -> Automaton:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        return self.automatons[name].reverse()
    def from_regex(self, regex: str) -> Automaton:
        return RegExpr(regex).compile()
    def empty_automaton(self) -> Automaton:
        return Automaton()
    def save_in_file(self) -> None:
        fd = open(os.path.join(*DEFAULT_DATABASE_PATH), 'w')
        fd.writelines(''.join([f"{name}\n" + self.automatons[name].stream_format()\
             for name in self.automatons]))
        fd.close()
    def load_from_file(self) -> None:
        self.automatons = {}
        fd = open(os.path.join(*DEFAULT_DATABASE_PATH))
        line = fd.readline()
        while line:
            name: str = line[0:-1]
            self.add_automaton(name, Automaton())
            line = fd.readline()
            states_labels: List[str] = line[0:-1].split(' ')
            for label in states_labels:
                self.automatons[name].add_state(label)
            line = fd.readline()
            starts_labels: List[str] = line[0:-1].split(' ')
            for label in starts_labels:
                self.automatons[name].set_start(label)
            while line[0] != 'f':
                line = fd.readline()
                start, letter, *targets = line[0:-1].split(' ')
                for target in targets:
                    self.automatons[name].add_transition(start, letter, target)
            dummy, *finals = line[0:-1].split(' ')
            for final in finals:
                self.automatons[name].make_state_final(final)
            line = fd.readline()
        fd.close() 
    def show_automaton(self, name: str) -> None:
        if name not in self.automatons:
            raise KeyError(NOT_FOUND_ERROR_MSG)
        dot = graphviz.Digraph()
        auto: Automaton = self.automatons[name]
        for state in auto.states:
            if state in auto.finals:
                if state in auto.starts:
                    dot.node(state.label, shape="doublecircle", style="filled", fillcolor="green")
                else:
                    dot.node(state.label, shape="doublecircle")
            elif state in auto.starts:
                dot.node(state.label, shape="circle", style="filled", fillcolor="green")
            else:
                dot.node(state.label, shape="circle")
        for state in auto.transitions:
            added_edges: Set[Tuple[str, str]] = set()
            for letter in auto.transitions[state]:
                for target in auto.transitions[state][letter]:
                    letters: List[str] = []
                    for letter in auto.transitions[state]:
                        if target in auto.transitions[state][letter]:
                            letters.append(letter)
                    if (state.label, target.label) not in added_edges:
                        dot.edge(state.label, target.label, label=f" {', '.join(letters)}")
                        added_edges.add((state.label, target.label))
        dot.render('automaton.gv', view=True)
    def clear(self) -> None:
        os.system('cls')
    def print(self) -> None:
        for name in self.automatons:
            print('-------------------------')
            print("Name: ", name, '\n')
            print(self.automatons[name])
    def contains(self, name: str) -> bool:
        return name in self.automatons
