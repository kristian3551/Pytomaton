"""Module providing the crusial functionality for the project."""
from __future__ import annotations
from typing import Set, Tuple, Dict, List
import copy

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
        self.transitions = {el: self.transitions[el] for el in self.transitions if el[0]\
        is not self.states[index]}
        self.states.pop(index)
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

    def __add_transition_by_index(self, idx1: int, letter: str, idx2: int) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        if idx1 < 0 or idx1 >= len(self.states):
            return False
        if idx2 < 0 or idx2 >= len(self.states):
            return False
        if not letter in self.alphabet:
            self.alphabet.append(letter)
        if (self.states[idx1], letter) not in self.transitions:
            self.transitions[(self.states[idx1], letter)] = [self.states[idx2]]
        if self.states[idx2] in self.transitions[(self.states[idx1], letter)]:
            return False
        self.transitions[(self.states[idx1], letter)].append(self.states[idx2])
        return True

    def add_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        idx1: int = self.states_dict[label1] if label1 in self.states_dict else -1
        idx2: int = self.states_dict[label2] if label2 in self.states_dict else -1
        return self.__add_transition_by_index(idx1, letter, idx2)

    def __get_state_transitions_by_index(self, index: int) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        if index < 0 or index >= len(self.states):
            return {}
        transtitions_tuples: List[Tuple[State, str]] = \
        [el for el in self.transitions if el[0] is self.states[index]]
        result: Dict[str, List[State]] = {}
        for pair in transtitions_tuples:
            result[pair[1]] = self.transitions[pair]
        return result

    def get_state_transitions(self, state: State) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        return self.__get_state_transitions_by_index(self.states_dict[state.label]\
            if state.label in self.states_dict else -1)

    def accepts_word(self, word: str) -> bool:
        """Checks if word is in the automaton language."""
        states: Set[State] = set(self.starts)
        for element in word:
            new_states: set[State] = set()
            for state in states:
                transitions: Dict[str, List[State]] = self.get_state_transitions(state)
                if element in transitions:
                    new_states = new_states | set(transitions[element])
            states = new_states
        for state in states:
            if state in self.finals:
                return True
        return False

    def copy(self) -> Automaton:
        """Returns a deep copy of the automation"""
        return copy.deepcopy(self)

    def is_deterministic(self) -> bool:
        """Checks if automaton is deterministic."""
        for state in self.states:
            state_transitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if letter in state_transitions and len(state_transitions[letter]) > 1:
                    return False
        return True

    def is_total(self) -> bool:
        """Checks if automaton is total (for each state for each
         letter exists transition from state with letter)"""
        for state in self.states:
            state_transitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in state_transitions:
                    return False
        return True

    def make_total(self) -> None:
        """Makes automaton total."""
        if self.is_total():
            return
        self.add_state("t")
        trash_state_idx = len(self.states) - 1
        for letter in self.alphabet:
            self.__add_transition_by_index(trash_state_idx, letter, trash_state_idx)
        for state in self.states:
            state_transitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in state_transitions:
                    self.add_transition(state.label, letter, "t")

    def get_state(self, label: str) -> State:
        """Returns state by label."""
        return self.states[self.states_dict[label]] if label in self.states_dict else State()

    def union(self, auto: Automaton) -> Automaton:
        """Unites automatons"""
        if self is auto:
            return self
        result: Automaton = self.copy()
        other_auto: Automaton = auto.copy()
        for state in other_auto.states:
            if state.label in result.states_dict:
                state.label = str(len(result.states))
            result.add_state(state.label)
        for transition_tuple in other_auto.transitions:
            for state in other_auto.transitions[transition_tuple]:
                result.add_transition(transition_tuple[0].label, transition_tuple[1], state.label)
        for final in other_auto.finals:
            result.make_state_final(final.label)
        for start in other_auto.starts:
            result.set_start(start.label)
        return result

    def concat(self, auto) -> Automaton:
        """Concatenates automatons"""
        result: Automaton = self.copy()
        other_auto: Automaton = auto.copy()
        for state in other_auto.states:
            if state.label in result.states_dict:
                state.label = str(len(result.states))
            result.add_state(state.label)
        for final in result.finals:
            for letter in result.alphabet:
                for start in other_auto.starts:
                    if (start, letter) in other_auto.transitions:
                        for element in other_auto.transitions[(start, letter)]:
                            result.add_transition(final.label, letter, element.label)
        for state, letter in other_auto.transitions:
            for element in other_auto.transitions[(state, letter)]:
                result.add_transition(state.label, letter, element.label)
        if not set(result.starts).intersection(set(result.finals)):
            result.finals = []
        for final in other_auto.finals:
            result.make_state_final(final.label)
        return result

    def complement(self) -> Automaton:
        """Returns automaton with complement language."""
        if not self.is_deterministic():
            print("Automaton is not deterministic.")
            return Automaton()
        result: Automaton = self.copy()
        if not result.is_total():
            result.make_total()
        finals: Set[State] = set([final for final in result.finals])
        result.finals = []
        for state in result.states:
            if not state in finals:
                result.make_state_final(state.label)
        return result

    def star(self) -> Automaton:
        """Returns automaton with language L(self)*"""
        result: Automaton = self.copy()
        for final in result.finals:
            for start in result.starts:
                transitions: List[Tuple[State, str]] =\
                    [element for element in result.transitions if element[0] is start]
                for state, letter in transitions:
                    if (final, letter) not in result.transitions:
                        result.transitions[(final, letter)] = []
                    result.transitions[(final, letter)] += result.transitions[(state, letter)]
        start_label = "s" if "s" not in result.states_dict else str(len(result.states))
        result.add_state(start_label)
        for start in result.starts:
            start_transitions: List[Tuple[State, str]] =\
                [element for element in result.transitions if element[0] is start]
            for state, letter in start_transitions:
                if (result.get_state(start_label), letter) not in result.transitions:
                    result.transitions[(result.get_state(start_label), letter)] = []
                    result.transitions[(result.get_state(start_label), letter)] +=\
                        result.transitions[(state, letter)]
        result.starts = [result.get_state(start_label)]
        result.make_state_final(start_label)
        return result

    def intersection(self, other_auto: Automaton) -> Automaton:
        """Returns an automaton with language L(self) ^ L(other_auto)."""
        if len(set(self.alphabet).intersection(set(other_auto.alphabet))) != len(self.alphabet):
            print("Automations don't have same alphabet.")
            return Automaton()
        if not self.is_deterministic() or not other_auto.is_deterministic():
            print("Automations are not deterministic.")
            return Automaton()
        result: Automaton = Automaton()
        result.alphabet = [el for el in self.alphabet]
        for state_1 in self.states:
            for state_2 in other_auto.states:
                result.add_state(f"{state_1.label}x{state_2.label}")
        for state_1 in self.starts:
            for state_2 in other_auto.starts:
                result.set_start(f"{state_1.label}x{state_2.label}")
        for state in result.states:
            tokens: List[str] = state.label.split("x")
            label1: str = tokens[0]
            label2: str = tokens[1]
            for letter in result.alphabet:
                tuple1: Tuple[State, str] = (self.states[self.states_dict[label1]], letter)
                transitions1: List[State]= self.transitions[tuple1] \
                    if tuple1 in self.transitions else []
                tuple2: Tuple[State, str] = (other_auto.states\
                [other_auto.states_dict[label2]], letter)
                transitions2: List[State]= other_auto.transitions[tuple2] \
                    if tuple2 in other_auto.transitions else []
                for state_1 in transitions1:
                    for state_2 in transitions2:
                        result.add_transition(f"{label1}x{label2}",\
                            letter, f"{state_1.label}x{state_2.label}")
        for state_1 in self.starts:
            for state_2 in other_auto.starts:
                result.set_start(f"{state_1.label}x{state_2.label}")
        for final_1 in self.finals:
            for final_2 in other_auto.finals:
                result.make_state_final(f"{final_1.label}x{final_2.label}")
        result.rename()
        return result

    def rename(self) -> None:
        """Renames states."""
        count: int = 0
        for state in self.states:
            state.label = str(count)
            count += 1

    def determinize(self) -> Automaton:
        """Returns a determinized version of self"""
        if self.is_deterministic():
            return self
        result: Automaton = Automaton()
        result.alphabet = [letter for letter in self.alphabet]
        queue: List[List[State]] = []
        queue.append(self.starts)
        start_label: str = str(sorted([state.label for state in self.starts]))
        result.add_state(start_label)
        result.set_start(start_label)
        while queue:
            current: List[State] = queue.pop(0)
            for letter in self.alphabet:
                states_set: List[State] = []
                for state in current:
                    states_set += self.transitions[(state, letter)]\
                        if (state, letter) in self.transitions else []
                set_label: str = str(sorted([state.label for state in states_set]))
                if set_label not in result.states_dict:
                    queue.append(states_set)
                    result.add_state(set_label)
                    if len([state for state in states_set if state in self.finals]) > 0:
                        result.make_state_final(set_label)
                result.add_transition(str(sorted(\
                    [state.label for state in current])), letter, set_label)
        result.rename()
        return result

    def minimize(self) -> Automaton:
        """Return a minimized automaton with same language."""
        result: Automaton = Automaton()
        return result

    def __repr__(self) -> str:
        return "--- Automaton:\n" + "States = " + str([el for el in self.states]) + \
        "\nStarting states: " + str([el for el in self.starts]) \
            + "\nTransition function:\n" + "\n".join([f"--- {el} -> {self.transitions[el]}"\
                 for el in self.transitions]) + \
                "\nFinal states: " + str(self.finals)
# a: Automaton = Automaton()
# a.add_state('0')
# a.add_state('1')
# a.add_transition('0', 'a', '1')
# a.add_transition('0', 'b', '0')
# a.add_transition('1', 'a', '0')
# a.add_transition('1', 'b', '1')
# a.make_state_final('1')
# a.set_start('0')
# other: Automaton = Automaton()
# other.add_state()
# other.add_state()
# other.add_state()
# other.add_transition('0', 'b', '1')
# other.add_transition('0', 'a', '0')
# other.add_transition('1', 'b', '2')
# other.add_transition('1', 'a', '1')
# other.add_transition('2', 'a', '2')
# other.add_transition('2', 'b', '2')
# other.make_state_final('2')
# other.set_start('0')
a: Automaton = Automaton()
a.add_state()
a.add_state()
a.add_state()
a.add_transition('0', 'a', '1')
a.add_transition('0', 'a', '2')
a.add_transition('0', 'b', '2')
a.add_transition('2', 'a', '2')
a.add_transition('2', 'b', '2')
a.make_state_final('2')
a.set_start('0')
print(a.determinize())
