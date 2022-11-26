from __future__ import annotations
from typing import Set, Tuple, Dict, List
import copy

"""Module providing the crusial functionality for the project."""



class State:
    """State in a nutshell"""
    def __init__(self, label: str = '') -> None:
        self.label = label
    def __repr__(self) -> str:
        return self.label

class Automaton:
    """The main class in the project. It holds the functionality an automaton should have:
        1. Managing internal properties: removing/adding/changing states.
        2. Saving automaton in file.
        3. Basic operations: concatenation, union, Kleene star, complement
        4. Making automaton deterministic
        5. Minifying automaton
        6. etc"""
    def __init__(self) -> None:
        self.alphabet: List[str] = []
        self.starts: List[State] = []
        self.states: List[State] = []
        self.states_dict: Dict[str, int] = {}
        self.transitions: Dict[Tuple[State, str], List[State]] = {}
        self.finals: List[State] = []
        self.reg_expr = ""
    def add_state(self, label: str = '') -> None:
        """Function for adding state"""
        label = str(len(self.states)) if not label or label in self.states_dict else label
        self.states.append(State(label))
        self.states_dict[label] = len(self.states) - 1
    def remove_state(self, index: int) -> bool:
        """Removes state"""
        if index >= len(self.states) or index < 0:
            return False
        self.finals = [state for state in self.finals if state is not self.states[index]]
        self.starts = [state for state in self.starts if state is not self.states[index]]
        self.transitions = {el: self.transitions[el] for el in self.transitions if el[0] is not self.states[index]}
        self.states.pop(index)
        return True
    def make_state_final_by_index(self, index: int) -> bool:
        """State becomes final"""
        if index < 0 or index >= len(self.states) or self.states[index] in self.finals:
            return False
        self.finals.append(self.states[index])
        return True
    def make_state_final(self, label: str) -> bool:
        """State becomes final"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or index >= len(self.states) or self.states[index] in self.finals:
            return False
        self.finals.append(self.states[index])
        return True
    def make_state_unfinal(self, label: str) -> bool:
        """State becomes final"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or index >= len(self.states) or not self.states[index] in self.finals:
            return False
        self.finals.remove(self.states[index])
        return True
    def set_start(self, label: str) -> bool:
        """Setting start state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or self.states[index] in self.starts:
            return False
        self.starts.append(self.states[index])
        return True
    def add_transition_by_index(self, idx1: int, letter: str, idx2: int) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        if idx1 < 0 or idx1 >= len(self.states):
            return False
        if idx2 < 0 or idx2 >= len(self.states):
            return False
        if not letter in self.alphabet: self.alphabet.append(letter)
        if not (self.states[idx1], letter) in self.transitions: self.transitions[(self.states[idx1], letter)] = [self.states[idx2]]
        if self.states[idx2] in self.transitions[(self.states[idx1], letter)]: return False
        self.transitions[(self.states[idx1], letter)].append(self.states[idx2])
        return True
    def add_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        idx1: int = self.states_dict[label1] if label1 in self.states_dict else -1
        idx2: int = self.states_dict[label2] if label2 in self.states_dict else -1
        if idx1 < 0 or idx2 < 0:
            return False
        if not letter in self.alphabet: self.alphabet.append(letter)
        if not (self.states[idx1], letter) in self.transitions: self.transitions[(self.states[idx1], letter)] = [self.states[idx2]]
        if self.states[idx2] in self.transitions[(self.states[idx1], letter)]: return False
        self.transitions[(self.states[idx1], letter)].append(self.states[idx2])
        return True
    
    def get_state_transitions_by_index(self, index: int) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        if index < 0 or index >= len(self.states):
            return {}
        transtitions_tuples: List[Tuple[State, str]] = [el for el in self.transitions if el[0] is self.states[index]]
        result: Dict[str, List[State]] = {}
        for tuple in transtitions_tuples:
            result[tuple[1]] = self.transitions[tuple]
        return result

    def get_state_transitions(self, state: State) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        if not state in self.states:
            return {}
        transtitions_tuples: List[Tuple[State, str]] = [el for el in self.transitions if el[0] is state]
        result: Dict[str, List[State]] = {}
        for tuple in transtitions_tuples:
            result[tuple[1]] = self.transitions[tuple]
        return result

    def accepts_word(self, word: str) -> bool:
        """Checks if word is in the automaton language."""
        states: Set[State] = set(self.starts)
        for el in word:
            newStates: set[State] = set()
            for s in states:
                transitions: Dict[str, List[State]] = self.get_state_transitions(s)
                if el in transitions: newStates = newStates | set(transitions[el])
            states = newStates
        for state in states:
            if state in self.finals: return True
        return False

    def copy(self) -> Automaton:
        """Returns a deep copy of the automation"""
        return copy.deepcopy(self)
    
    def is_deterministic(self) -> bool:
        for state in self.states:
            stateTransitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if letter in stateTransitions and len(stateTransitions[letter]) > 1: 
                    return False
        return True

    def is_total(self) -> bool:
        """Checks if automaton is total (for each state for each letter exists transition from state with letter)"""
        for state in self.states:
            stateTransitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in stateTransitions: 
                    return False
        return True
    
    def make_total(self) -> None:
        """Makes automaton total."""
        if self.is_total(): return
        self.add_state("trash")
        trash_state_idx = len(self.states) - 1
        for letter in self.alphabet:
            self.add_transition_by_index(trash_state_idx, letter, trash_state_idx)
        for i in range(len(self.states)):
            stateTransitions: Dict[str, List[State]] = self.get_state_transitions(self.states[i])
            for letter in self.alphabet:
                if not letter in stateTransitions: 
                    self.add_transition_by_index(i, letter, trash_state_idx)

    def get_state(self, label: str) -> State:
        return self.states[self.states_dict[label]] if label in self.states_dict else State()

    def union(self, auto: Automaton) -> Automaton:
        """Unites automatons"""
        if self is other: return self
        result: Automaton = self.copy()
        other: Automaton = auto.copy()
        for i in range(len(other.states)):
            if other.states[i].label in result.states_dict: other.states[i].label = str(len(result.states))
            result.add_state(other.states[i].label)
        for transition_tuple in other.transitions:
            for state in other.transitions[transition_tuple]:
                result.add_transition(transition_tuple[0].label, transition_tuple[1], state.label)
        for final in other.finals:
            result.make_state_final(final.label)
        for start in other.starts:
            result.set_start(start.label)
        return result

    def concat(self, auto) -> Automaton:
        """Concatenates automatons"""
        result: Automaton = self.copy()
        other: Automaton = auto.copy()
        for i in range(len(other.states)):
            if other.states[i].label in result.states_dict: other.states[i].label = str(len(result.states))
            result.add_state(other.states[i].label)
        for final in result.finals:
            for letter in result.alphabet:
                for start in other.starts:
                    if (start, letter) in other.transitions:
                        for el in other.transitions[(start, letter)]:
                            result.add_transition(final.label, letter, el.label)
        for state, letter in other.transitions:
            for el in other.transitions[(state, letter)]:
                result.add_transition(state.label, letter, el.label)
        if not set(result.starts).intersection(set(result.finals)):
            result.finals = []
        for final in other.finals:
            result.make_state_final(final.label)
        return result

    def complement(self) -> Automaton:
        if not self.is_deterministic(): return Automaton()
        result: Automaton = self.copy()
        if not result.is_total(): result.make_total()
        finals: Set[State] = set([final for final in result.finals])
        result.finals = []
        for state in result.states:
            if not state in finals:
                result.make_state_final(state.label)
        return result

    def __repr__(self) -> str:
        return "--- Automaton:\n" + "States = " + str([el for el in self.states]) + "\nStarting states: " + str([el for el in self.starts]) \
            + "\nTransition function:\n" + "\n".join([f"--- {el} -> {self.transitions[el]}" for el in self.transitions]) + \
                "\nFinal states: " + str(self.finals)

a: Automaton = Automaton()
a.add_state()
a.add_state()
a.add_transition('0', 'a', '1')
a.add_transition('0', 'b', '0')
a.add_transition('1', 'a', '0')
a.add_transition('1', 'b', '1')
a.make_state_final('1')
a.set_start('0')
other: Automaton = Automaton()
other.add_state()
other.add_state()
other.add_transition('0', 'b', '1')
other.add_transition('0', 'a', '0')
other.add_transition('1', 'b', '0')
other.add_transition('1', 'a', '1')
other.make_state_final('1')
other.set_start('0')
print(a.complement().accepts_word("aabba"))