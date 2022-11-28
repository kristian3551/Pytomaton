"""Module providing the crusial functionality for the project."""
from __future__ import annotations
from typing import Set, Dict, List
import copy
import os

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
        self.transitions: Dict[State, Dict[str, List[State]]] = {}
        self.finals: List[State] = []
        self.reg_expr = ""

    def add_state(self, label: str = '') -> None:
        """Function for adding state"""
        label = str(len(self.states)) if not label or label in self.states_dict else label
        self.states.append(State(label))
        self.states_dict[label] = len(self.states) - 1

    def remove_state(self, label: str) -> bool:
        """Removes state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index >= len(self.states) or index < 0:
            return False
        self.finals = [state for state in self.finals if state is not self.states[index]]
        self.starts = [state for state in self.starts if state is not self.states[index]]
        if self.states[index] in self.transitions:
            del self.transitions[self.states[index]]
        for state in self.transitions:
            for letter in self.transitions[state]:
                self.transitions[state][letter].remove(self.states[index])
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

    def remove_start(self, label: str) -> bool:
        """Removing start state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or self.states[index] not in self.starts:
            return False
        self.starts.remove(self.states[index])
        return True

    def __add_transition_by_index(self, idx1: int, letter: str, idx2: int) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        if idx1 < 0 or idx1 >= len(self.states):
            return False
        if idx2 < 0 or idx2 >= len(self.states):
            return False
        if letter not in self.alphabet:
            self.alphabet.append(letter)
        state_1: State = self.states[idx1]
        state_2: State = self.states[idx2]
        if state_1 not in self.transitions:
            self.transitions[state_1] = {letter: [state_2]}
        elif letter not in self.transitions[state_1]:
            self.transitions[state_1][letter] = [state_2]
        elif state_2 in self.transitions[state_1][letter]:
            return False
        else:
            self.transitions[state_1][letter].append(state_2)
        return True

    def add_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        idx1: int = self.states_dict[label1] if label1 in self.states_dict else -1
        idx2: int = self.states_dict[label2] if label2 in self.states_dict else -1
        return self.__add_transition_by_index(idx1, letter, idx2)

    def __add_transitions(self, label1: str, letter, states: List[State]) -> bool:
        """Adds many transitions at a time."""
        states_labels: List[str] = [state.label for state in states]
        for state_label in states_labels:
            res: bool = self.add_transition(label1, letter, state_label)
            if not res:
                return False
        return True

    def remove_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Removes transition."""
        if self.get_state(label1) not in self.transitions\
             or letter not in self.transitions[self.get_state(label1)]\
            or label2 not in self.states_dict or self.get_state(label2)\
                 not in self.transitions[self.get_state(label1)][letter]:
            return False
        self.transitions[self.get_state(label1)][letter].remove(self.get_state(label2))
        return True

    def __get_state_transitions_by_index(self, index: int) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        if index < 0 or index >= len(self.states):
            return {}
        state: State = self.states[index]
        return self.transitions[state] if state in self.transitions else {}

    def get_state_transitions(self, state: State) -> Dict[str, List[State]]:
        """Get transitions of state with index 'index'."""
        return self.__get_state_transitions_by_index(self.states_dict[state.label]\
            if state.label in self.states_dict else -1)

    def accepts_word(self, word: str) -> bool:
        """Checks if word is in the automaton language."""
        states: Set[State] = set(self.starts)
        for letter in word:
            new_states: Set[State] = set()
            for state in states:
                transitions: Dict[str, List[State]] = self.get_state_transitions(state)
                if letter in transitions:
                    new_states = new_states | set(transitions[letter])
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
        trash_label = "t" if "t" not in self.states_dict else str(len(self.states))
        self.add_state(trash_label)
        trash_state_idx = len(self.states) - 1
        for letter in self.alphabet:
            self.__add_transition_by_index(trash_state_idx, letter, trash_state_idx)
        for state in self.states:
            state_transitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in state_transitions:
                    self.add_transition(state.label, letter, trash_label)

    def total(self) -> Automaton:
        """Returns a totalized copy of the automaton."""
        result: Automaton = self.copy()
        result.make_total()
        return result

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
                del other_auto.states_dict[state.label]
                state.label = str(len(result.states))
                other_auto.states_dict[state.label] = len(result.states)
            result.add_state(state.label)
        for state in other_auto.transitions:
            for letter in other_auto.transitions[state]:
                result.__add_transitions(state.label, letter, other_auto.transitions[state][letter])
        for final in other_auto.finals:
            result.make_state_final(final.label)
        for start in other_auto.starts:
            result.set_start(start.label)
        return result

    def concat(self, auto) -> Automaton:
        """Concatenates automatons"""
        result: Automaton = self.copy()
        other_auto: Automaton = auto.copy()
        for i in range(len(other_auto.states)):
            state: State = other_auto.states[i]
            if state.label in result.states_dict:
                del other_auto.states_dict[state.label]
                state.label = str(len(result.states))
                other_auto.states_dict[state.label] = len(result.states)
            result.add_state(state.label)
        for final in result.finals:
            for start in other_auto.starts:
                start_transitions: Dict[str, List[State]] = other_auto.transitions[start]\
                     if start in other_auto.transitions else {}
                for letter in start_transitions:
                    result.__add_transitions(final.label, letter, start_transitions[letter])
        for state in other_auto.transitions:
            for letter in other_auto.transitions[state]:
                result.__add_transitions(state.label, letter, other_auto.transitions[state][letter])

        if not set(other_auto.starts).intersection(set(other_auto.finals)):
            result.finals = []
        for final in other_auto.finals:
            result.make_state_final(final.label)
        return result

    def complement(self) -> Automaton:
        """Returns automaton with complement language."""
        if not self.is_deterministic():
            raise ValueError("Automaton is not deterministic.")
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
                transitions: Dict[str, List[State]] = self.get_state_transitions(start)
                for letter in transitions:
                    result.__add_transitions(final.label, letter, transitions[letter])
        start_label = str(len(result.states))
        result.add_state(start_label)
        result.starts.append(result.get_state(start_label))
        result.make_state_final(start_label)
        return result

    def intersection(self, other_auto: Automaton) -> Automaton:
        """Returns an automaton with language L(self) ^ L(other_auto)."""
        if len(set(self.alphabet).intersection(set(other_auto.alphabet))) != len(self.alphabet):
            raise ValueError("Automations don't have same alphabet.")
        if not self.is_deterministic() or not other_auto.is_deterministic():
            raise ValueError("Automaton is not deterministic.")
        result: Automaton = Automaton()
        result.alphabet = list(self.alphabet)
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
            transitions_1: Dict[str, List[State]] =\
                 self.get_state_transitions(self.get_state(label1))
            transitions_2: Dict[str, List[State]] =\
                 other_auto.get_state_transitions(other_auto.get_state(label2))
            for letter in transitions_1:
                if letter in transitions_2:
                    for s_1 in transitions_1[letter]:
                        for s_2 in transitions_2[letter]:
                            result.add_transition(state.label, letter, f"{s_1.label}x{s_2.label}")
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
        self.states_dict = {}
        for state in self.states:
            state.label = str(count)
            self.states_dict[state.label] = count
            count += 1

    def determinize(self) -> Automaton:
        """Returns a determinized version of self"""
        if self.is_deterministic():
            return self
        result: Automaton = Automaton()
        result.alphabet = [letter for letter in self.alphabet]
        queue: List[List[State]] = []
        queue.append(self.starts)
        start_label: str = str(sorted(set([state.label for state in self.starts])))
        result.add_state(start_label)
        result.set_start(start_label)
        if len([state for state in self.starts if state in self.finals]) > 0:
            result.make_state_final(start_label)
        while queue:
            current: List[State] = queue.pop(0)
            for letter in result.alphabet:
                states_set: List[State] = []
                for state in current:
                    states_set += self.transitions[state][letter] if state in self.transitions\
                         and letter in self.transitions[state] else []
                set_label: str = str(sorted(set([state.label for state in states_set])))
                if set_label not in result.states_dict:
                    queue.append(states_set)
                    result.add_state(set_label)
                    if len([state for state in states_set if state in self.finals]) > 0:
                        result.make_state_final(set_label)
                result.add_transition(str(sorted(\
                    set([state.label for state in current]))), letter, set_label)
        result.rename()
        return result

    def minimize(self) -> Automaton:
        """Return a minimized automaton with same language."""
        return self.copy().determinize().reverse().determinize().reverse().determinize()

    def reverse(self) -> Automaton:
        """Returns an automaton with language L(self)^rev"""
        result: Automaton = Automaton()
        for state in self.states:
            result.add_state(state.label)
        for start in self.starts:
            result.make_state_final(start.label)
        for final in self.finals:
            result.set_start(final.label)
        for state in result.states:
            transitions: Dict[str, List[State]] = self.get_state_transitions(state)
            for letter in transitions:
                for res in transitions[letter]:
                    result.add_transition(res.label, letter, state.label)
        return result

    @staticmethod
    def by_letter(letter: str) -> Automaton:
        """Creates an automaton with language L = {letter}."""
        auto: Automaton = Automaton()
        auto.add_state()
        auto.add_state()
        auto.set_start('0')
        auto.make_state_final('1')
        auto.add_transition('0', letter, '1')
        return auto

    @staticmethod
    def singleton_epsilon() -> Automaton:
        """Creates an automaton with language L = {letter}."""
        auto: Automaton = Automaton()
        auto.add_state()
        auto.set_start('0')
        auto.make_state_final('0')
        return auto

    def __repr__(self) -> str:
        return "--- Automaton:\n" + "States = " + str([el for el in self.states]) + \
        "\nStarting states: " + str([el for el in self.starts]) \
            + "\nTransition function:\n" + "\n".join([f"--- {el} -> {self.transitions[el]}"\
                 for el in self.transitions]) + \
                "\nFinal states: " + str(self.finals)

    def save_in_file(self, path: List[str]) -> None:
        fd = open(os.path.join(*path), 'w')
        fd.writelines(self.stream_format())
        fd.close()
    
    def load_from_file(self, path: List[str]) -> None:
        fd = open(os.path.join(*path))
        states_labels: List[str] = fd.readline().split(" ")
        for label in states_labels:
            self.add_state(label.replace('\n', ''))
        starts_labels: List[str] = fd.readline().split(" ")
        for label in starts_labels:
            self.set_start(label.replace('\n', ''))
        rest: List[str] = fd.read().split('\n')
        for i in range(len(rest) - 2):
            transitions_raw = rest[i].split(" ")
            start, letter, *targets = transitions_raw
            for target in targets:
                self.add_transition(start, letter, target)
        final_labels: List[str] = rest[-2].split(" ")
        for label in final_labels:
            self.make_state_final(label)
        fd.close()

    def stream_format(self) -> str:
        dict_to_list: List[str] = []
        for state in self.transitions:
            for letter in self.transitions[state]:
                dict_to_list.append(f"{state.label} {letter} " + " ".join(\
                    [st.label for st in self.transitions[state][letter]]))
        return "".join([" ".join(self.states_dict.keys()) + '\n',
                " ".join([start.label for start in self.starts]) + '\n',
                "\n".join(dict_to_list) + '\n', 
                "f " + " ".join([final.label for final in self.finals]) + '\n'])
